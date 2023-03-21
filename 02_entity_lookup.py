import json
import pandas as pd
from tqdm import tqdm

#data_path = 'WikidataNE_20170320_NECKAR_1_0.json_/WikidataNE_20170320_NECKAR_1_0.json'
qid_dict={}

#with open(data_path,'r') as f:
#    for i in f.readlines():
#        d = json.loads(i)
#        qid_dict[d['id']]=d['neClass']
qid_dict = json.load(open('qid_dict.json','r'))
print(len(qid_dict))
print(len(set(qid_dict.values())))

#json.dump(qid_dict,open('qid_dict.json','w'))

lang_dict=['as','bn','kn','gu','hi','ml','mr','or','ta','te','pa']
for code in tqdm(lang_dict):
    filename='master-data/'+code+'-entity-master.csv'
    df = pd.read_csv('pa-entity-master.csv')
#    print(df.columns)
    df['entity']=df['entity'].map(lambda x:[i+[qid_dict.get(i[2],-1)] for i in eval(x)])
    df.to_csv('master-data-conll/'+code+'-entity-master-final.csv',index=False)
#data = json.load(f)
#import pdb;pdb.set_trace()
