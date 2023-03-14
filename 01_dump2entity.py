import csv
import pandas as pd 
from collections import defaultdict
import json
import ast
from wikimedia import get_wikimedia_ids
from tqdm import tqdm
tqdm.pandas()


language = 'pa'
def get_master_entity(entity):
    entity_list = ast.literal_eval(entity)
    for e in entity_list:
        #print(e)
        master_ent.add(e[0])


master_ent = set()
master_ent_ids = defaultdict()



if __name__ == "__main__":

    filepath = f"/Users/rahulmehta/Desktop/IndicNER/data-wikidumps/clean-dumps/sentence_data_ent_{language}.csv"
    df  = pd.read_csv(filepath)

    #print(len(master_ent_ids))
    #print(sum(value == -1 for value in master_ent_ids.values()))

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


    f =  open(f'/Users/rahulmehta/Desktop/IndicNER/data-wikidumps/entity-master-ids/{language}-entity-qids.json') 
    master_ent_ids = json.load(f)


    #  Look up the entity list
    def entity_lookup(entity):
        entity_list = ast.literal_eval(entity)
        #print(entity_list)

        for e in entity_list:
            # print(type(e))
            #print(e[0])
            try:
                #print(master_ent_ids[e[0]])
                e.append(master_ent_ids[e[0]]) 

            except:
                pass
        
        return entity_list

    print(df.columns)

    df['entity'] = df['entity'].progress_apply(lambda x: entity_lookup(x))
    #df['entity'] = ast.literal_eval(df['entity'])


    df.to_csv(f'/Users/rahulmehta/Desktop/IndicNER/data-wikidumps/master-data/{language}-entity-master.csv',index=None)
