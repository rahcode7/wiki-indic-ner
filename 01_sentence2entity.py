import csv
import pandas as pd 
from collections import defaultdict
import json
import ast
from wikimedia import get_wikimedia_ids
from tqdm import tqdm
tqdm.pandas()


<<<<<<< Updated upstream
MASTER_ENT = set()
=======
#language = 'pa','as','bn'
language_list = ['gu','hi','kn','te','ta','ml','mr','or']

>>>>>>> Stashed changes

def get_master_entity(entity):
    entity_list = list(ast.literal_eval(entity))
    for e in entity_list:
        #print(e)
        MASTER_ENT.add(e[0])

    #return master_ent




dir = "/Users/rahulmehta/Desktop/IndicNER/data-wikidumps/"

if __name__ == "__main__":

    master_ent_ids = defaultdict()
    # 'pa'
    language_list = ['as','bn','gu','hi','kn','te','ta','ml','mr','or']


    for language in language_list:
        print(language)

        filepath =  dir + f"clean-dumps/sentence_data_ent_{language}.csv"
        df  = pd.read_csv(filepath)

        #print(len(master_ent_ids))
        #print(sum(value == -1 for value in master_ent_ids.values()))

        #master_ent = set()
        df['entity'].progress_apply(lambda x: get_master_entity(x))

        #print(list(master_ent))

        master_ent = list(MASTER_ENT)
        print(len(master_ent))

        #print(master_ent[0:5])

        # In batch of 50, crawl mediawiki
<<<<<<< Updated upstream
        for i in tqdm(range(0,len(master_ent),50)):
            #print(master_ent[i:i+49])
            master_ent_ids.update(get_wikimedia_ids(master_ent[i:i+49],language))
=======
        #for i in tqdm(range(0,len(master_ent),50)):
        for i in tqdm(range(0,6000,50)):
        
            print(i)
            master_ent_ids.update(get_wikimedia_ids(master_ent[i:i+49],'pa'))
>>>>>>> Stashed changes

            # save dict every 5000
            if i % 5000 == 0 :
                with open(dir + f'entity-master-ids/{language}-entity-qids.json',"w") as outfile:
                    json.dump(master_ent_ids,outfile,ensure_ascii=False)


                f =  open(dir + f'/entity-master-ids/{language}-entity-qids.json') 
                master_ent_ids = json.load(f)


        print(len(master_ent_ids))
        #print(master_ent_ids)

        with open(dir + f'entity-master-ids/{language}-entity-qids.json',"w") as outfile:
            json.dump(master_ent_ids,outfile,ensure_ascii=False)


        f =  open(dir + f'/entity-master-ids/{language}-entity-qids.json') 
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

        #print(df.columns)

        df['entity'] = df['entity'].progress_apply(lambda x: entity_lookup(x))
        #df['entity'] = ast.literal_eval(df['entity'])


        df.to_csv(dir + f'master-data/{language}-entity-master.csv',index=None)
