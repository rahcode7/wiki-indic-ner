import csv
import pandas as pd 
from collections import defaultdict
import json
import ast
from wikimedia import get_wikimedia_ids

language = 'pa'
filepath = f"/Users/rahulmehta/Desktop/IndicNER/data-wikidumps/clean-dumps/sentence_data_ent_{language}.csv"

df  = pd.read_csv(filepath)
# print(df.head(50))
# print(df.shape)


master_ent = set()
master_ent_ids = defaultdict()

def get_master_entity(entity):
    entity_list = ast.literal_eval(entity)
    for e in entity_list:
        #print(e)
        master_ent.add(e[0])

df['entity'].apply(lambda x: get_master_entity(x))

#print(list(master_ent))

master_ent = list(master_ent)
print(len(master_ent))


# In batch of 50, crawl mediawiki
for i in range(0,len(master_ent),50):
    print(i)
    master_ent_ids.update(get_wikimedia_ids(master_ent[i:i+49],'pa'))

print(len(master_ent_ids))
print(master_ent_ids)


with open(f'/Users/rahulmehta/Desktop/IndicNER/data-wikidumps/entity-master-ids/{language}-entity-qids.json',"w") as outfile:
    json.dump(master_ent_ids,outfile,ensure_ascii=False)
