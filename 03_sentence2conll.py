import pandas as pd
import re
from tqdm import tqdm


a=['as','bn','gu','hi','kn','ml','mr','or','pa','ta','te']
# a=['as']


def processor(code):
    df = pd.read_csv('master-data-conll/'+code+'-entity-master-final.csv')
    all_strings = ''
    count=0
    for index,row in tqdm(df.iterrows(),total=df.shape[0]):
        text = row['sentence'].rstrip()

        splits = re.split('[\s\n\t\-\(\)\"\"\;\.\-]+',text )#[\s\n\t\,\(\)\.\"\"]

        all_splits=[]
        pos = 0
        index =0 

        while pos<len(text):
            if index<len(splits) and text[pos:].startswith(splits[index]):
                all_splits.append([splits[index],pos,pos+len(splits[index])])
                pos+=len(splits[index])
                index+=1
            else:
                all_splits.append([text[pos],pos,pos+1])
                pos+=1

        string = '# id pa'+str(index)+' domain=pa'
        nes=[]
        for i in eval(row['entity']):
            ne=[]
            for j in all_splits:
                if not ((j[-2]< i[1] and j[-1] <=i[1] ) or (j[-2] >=i[2] and j[-1]>i[2])):
                    try: ne.append([j[-2],j[0],'B-'+i[-1] if len(ne)==0 else 'I-'+i[-1]])
                    except: pass
            nes.extend(ne)
        if len(nes)==0: continue
        ne_starts =[i[0] for i in nes]
        for j in all_splits:
            if j[-2] not in ne_starts:
                nes.append([j[-2],j[0],'O'])
        nes = sorted(nes,key =lambda x:x[0])
        for i in nes:
            if i[1]!=' ': string+='\n'+i[1]+'__'+i[2]

        count+=1
        all_strings+= string
        all_strings+='\n \n'
    print(count,' documents for language ',code)
    with open('conll-data/'+code+'-conll.txt','w') as f:
        f.write(all_strings)
[processor(code) for code in a]
