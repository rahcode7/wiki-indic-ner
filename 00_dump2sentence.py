from tqdm import tqdm
from copy import deepcopy
from xml.etree import ElementTree as ET
import re
import pandas as pd 
import os 
from indicnlp.tokenize import sentence_tokenize


def get_unpiped_text(art_text):
    matches = re.finditer(r'\[\[(.*?)\]\]',art_text)
    for match in matches:
        match_text = match.group(1)
        if '|' in match_text:
            clean_match_text = match_text.split('|')[1]
            match_text = match_text.replace('|','\|')
            match_text = match_text.replace('[','\[')
            match_text = match_text.replace(']','\]')
            match_text = match_text.replace('(','\(')
            match_text = match_text.replace(')','\)')
            art_text = re.sub(match_text,clean_match_text,art_text)
    return art_text

def get_clean_text(art_text):
    
    try:
        art_text = re.sub("<ref>.*?</ref>", "", art_text)
        art_text = re.sub("<ref name.*?/(ref)*?>", "", art_text)
        art_text = re.sub("<ref(.|\n)*?<\/ref>", "", art_text)
        
    except:
        pass
    
    try:
        art_text = re.sub("{{.*?}}", "", art_text)
        art_text = re.sub("{{[^}]*}}", "", art_text)
        art_text = re.sub("\([Ss]ource:.*?\)", "", art_text)
        art_text = re.sub("url=.*?}}", "", art_text)
        
        
        
    except:
        pass
    try:
        art_text = re.sub(r"{\|.*?\|}", "", art_text)
        art_text = re.sub(r"{\| class[^}]*}", "", art_text)
        art_text = re.sub("<imagemap[^<]*?</imagemap>", "", art_text)   # remove imagemap template pattern 
        art_text = re.sub(r"{\|[^}]*?}", "", art_text)
        #art_text = re.sub("\*\s\[.*\]", "", art_text)   # to remove reference starts with * []
        #art_text = re.sub("\*\[.*\]", "", art_text)
        
    except:
        pass
    
    
    try:
        art_text = re.sub("\n\|[^}]*?}}", "", art_text)
        art_text = re.sub("\n \|[^}]*?}}", "", art_text)
        art_text = re.sub("\n\|.*?\|}", "", art_text)
        art_text = re.sub("\n\|[^}]*?\|}", "", art_text)
    except:
        pass
    
    try:
        art_text = re.sub("<table.*?</table>", "", art_text)
        art_text = re.sub("<pre>.*?</pre>", "", art_text)
        art_text = re.sub("<tr>.*?</tr>", "", art_text)
        
        art_text = re.sub("<div.*?</div>", "", art_text)
        art_text = re.sub("<syntaxhighlight[^<]*</syntaxhighlight>", "", art_text)
        #art_text = re.sub("<syntaxhighlight.*?</syntaxhighlight>", "", art_text)
        
        
        art_text = re.sub("\[\[File:.*\]\]", "", art_text)
        art_text = re.sub("\[\[चित्र:.*\]\]", "", art_text)
        art_text = re.sub("\[\[బొమ్మ:.*\]\]", "", art_text)
        art_text = re.sub("\[\[Image:.*\]\]", "", art_text)
        art_text = re.sub("\[\[image:.*\]\]", "", art_text)
        art_text = re.sub("\[\[దస్త్రం:.*\]\]", "", art_text)
        art_text = re.sub("\[\[చిత్రం:.*\]\]", "", art_text)
        art_text = re.sub("\[http.*?\]", "", art_text)
        art_text = re.sub("<gallery[^}]*<\/gallery>", "", art_text)
    except:
        pass
    
    try:   
        art_text = re.sub(r"<!--.*?-->", "", art_text)
        art_text = re.sub(r"<!--[^>]*>", "", art_text)
        art_text = re.sub("<ref name.*?</ref>", "", art_text)
        art_text = re.sub("<ref name.*?>", "", art_text)
        
    except:
        pass
    
    # try:
    #     art_text = get_unpiped_text(art_text)
    # except:
    #     pass
        #print(art_text)
    try:
#         art_text = re.sub("\[\[", "", art_text)
#         art_text = re.sub("\]\]", "", art_text)
        art_text = re.sub("\{\{", "", art_text)
        art_text = re.sub("\}\}", "", art_text)
        art_text = re.sub("\(\)", "", art_text)
        art_text = re.sub("<small>", "", art_text)
        art_text = re.sub("</small>", "", art_text)
        art_text = re.sub("&nbsp;", "", art_text)
    except:
        pass 
    
    
    return art_text

def get_add_clean(art_text):
    try:
        art_text = re.sub("<table.*?</table>", "", art_text)
        art_text = re.sub("<pre>.*?</pre>", "", art_text)
        art_text = re.sub("<tr>.*?</tr>", "", art_text)
        art_text = re.sub("<.*?>", "", art_text)
        art_text = art_text.replace("'''", "")
        art_text = art_text.replace("<br>", "")
        art_text = art_text.replace("<br/>", "")
        art_text = art_text.replace("*", "")
        art_text = art_text.replace("<tt>", "")
        art_text = art_text.replace("</tt>", "")
        art_text = art_text.replace("<tr>", "")
        art_text = art_text.replace("</tr>", "")
        art_text = art_text.replace("<td>", "")
        art_text = art_text.replace("</td>", "")
        art_text = art_text.replace("<poem>", "")
        art_text = art_text.replace("</poem>", "")
        art_text = art_text.replace("<code>", "")
        art_text = art_text.replace("</code>", "")
        art_text = art_text.replace("</ref>", "")
        art_text = art_text.replace("<ref>", "")
        art_text = art_text.replace("\\'", "'")
        
    except:
        pass
    return art_text


def remove_headings(text):
    ans=""
    for line in text.split("\n"):
        if line.startswith("="):
            continue
        ans+=line
        ans+="\n"
    return ans

def remove_lists(text):
    ans=""
    for line in text.split("\n"):
        if line.startswith("*"):
            continue
        ans+=line
        ans+="\n"
    return ans

def remove_shorts(text):
    ans=""
    for line in text.split("\n"):
        if len(line)<=50:
            continue
        ans+=line
        ans+="\n"
    return ans

def pipeline(text):
    text =get_clean_text(text)
    if text is None:
        return ''
    text = remove_headings(text)
    text = remove_lists(text)
    text = remove_shorts(text)
    return text

def tokenizer(text,lang_code='te'):
    sentences = sentence_tokenize.sentence_split(text, lang=lang_code)
    return sentences

# file_dict={'pa':'../data-wikidumps/pawiki-20230301-pages-articles-multistream.xml',
#             ''
# }


def read_dump(lang_code,file_dict):
    titles =[]
    articles = []
    tags =[]
    title=''
    buffer=[]
    buffertag=[]
    meta=[]
    filepath = file_dict[lang_code]
    for _, elem in tqdm(ET.iterparse(filepath, events=("end",))):
        if elem.tag.endswith('text'):
            articles.append(elem.text)
        elif elem.tag.endswith('title'):
            meta.append(buffer)
            titles.append(elem.text)
            buffer=[]
        else:
            try:
                buffer.append(elem.tag+' -> '+elem.text)
            except:
                buffer.append(elem.tag+' -> ')
        elem.clear()
    return titles,meta,articles

# print(len(titles))
# print(len(meta))
# print(len(articles))
def remove_links(art_text):
    matches = re.finditer(r'\[\[(.*?)\]\]',art_text)
    clean_text =''
    curren_index = 0
    spans = []
    for match in matches:
        match_text = match.group()
        start = match.start()
        end = match.end()
        
        #Plaint text
        clean_text+=art_text[curren_index:start]
        
        # Title
        title = match_text[2:-2].split('|')[0] if '|' in match_text else match_text[2:-2]
        if ':' in title:
            return None,[]
        surface = match_text[2:-2].split('|')[1] if '|' in match_text else match_text[2:-2]
        spans.append([title,len(clean_text),len(clean_text)+len(surface)])

        clean_text+= surface
        curren_index = end
    clean_text+=art_text[curren_index:]
    if '\n' in clean_text:
        return None,[]
    return clean_text,spans

def clean_article(article,lang_code='te'):
    clean_text = pipeline(article)
    if clean_text=='':
        return None
    sentences = tokenizer(clean_text,lang_code)
    data=[]
    for sentence in sentences:
        text,spans = remove_links(sentence)
        data.append([text,spans] if len(spans)>0 else None)
    return data



delimiter ='\t'
delimiter2 ='\t\t'
clean_dump={}



path = "/Users/rahulmehta/Desktop/IndicNER/data-wikidumps/"

file_dict = {}
file_list = []
for root, dirs, files in os.walk(path + 'raw-dumps/'):
    file_list = [n for n in files]

for f in file_list:
    file_dict[f[0:2]] = path + 'raw-dumps/' + f
print(file_dict)


art_list = []
for i,(lang_code,val) in enumerate(file_dict.items()):
    print(lang_code)
    titles,meta,articles = read_dump(lang_code,file_dict)
    for i,j in tqdm(zip(articles,titles)):
        j = j.lower()
        if 'మీడియావికీ' in j or 'Homepage' in j or 'వికీపీడియా' in j or 'मीडियाविकी' in j or 'ਮੀਡੀਆਵਿਕੀ' in j or ':' in j or 'மீடியாவிக்கி' in j or 'મીડિયાવિકિ' in j or 'mediawiki' in j or 'മീഡിയവിക്കി' in j or 'ಮೀಡಿಯಾವಿಕಿ' in j or 'विकिपीडिया' in j or 'ৱিকিপিডিয়া' in j or 'ਵਿਕੀਪੀਡੀਆ' in j or 'વિકિપીડિયા' in j or 'വിക്കിപീഡിയ' in j or 'ವಿಕಿಪೀಡಿಯ' in j or 'விக்கிபீடியா' in j:
            continue
        try:
            data = clean_article(i)
            #print(data)
            for dat in data:
                d = {}
                if dat is not None:
                    d['lang_code'] = lang_code
                    d['title'] = j
                    d['sentence'] = dat[0]
                    d['entity'] = str(dat[1])
                    
                    if bool(d):
                        art_list.append(d)
        except:
            pass

    art_df = pd.DataFrame.from_dict(art_list)
    art_df.to_csv(path + f"clean-dumps/sentence_data_ent_{lang_code}.csv",index=None)
