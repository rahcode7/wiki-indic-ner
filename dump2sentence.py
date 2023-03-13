from tqdm import tqdm
from copy import deepcopy
from xml.etree import ElementTree as ET
import re

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



titles =[]
pattern = re.compile("అయోమయ నివృత్తి")
pattern = re.compile("అయోమయ నివృత్తి")
articles = []
tags =[]
title=''
buffer=[]
buffertag=[]
meta=[]


filepath = 'tewiki-20230301-pages-articles-multistream.xml'
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

print(len(titles))
print(len(meta))
print(len(articles))


def show_article(idx):
    print(titles[idx])
    print('**********************')
    print(meta[idx])
    print('**********************')
    print(articles[idx])
    print(get_clean_text(articles[idx]))

import pdb;pdb.set_trace()
