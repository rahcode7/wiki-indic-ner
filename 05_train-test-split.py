import os 
import json
import random
import pandas as pd

OUTPUT_REF_PATH = '/Users/rahulmehta/Desktop/IndicNER/datasets/conll-train-test/'
INPUT_PATH = '/Users/rahulmehta/Desktop/IndicNER/datasets/conll-data-formatted/'
#language_list = ['gu']

language_list = ['hi','gu','kn','te','ta','ml','mr','or','pa','as','bn']

# Create train,test,dev split 
f = open(INPUT_PATH + 'sent-count.txt') 
sent_count = json.load(f)



df = pd.DataFrame(columns=['language','train_count','dev_count','test_count'])

for lang in language_list:
    print(lang)
    cnt = 0 
    train_size = int(round(sent_count[lang] * 0.7,0))
    dev_size = int(round(sent_count[lang] * 0.2,0))
    print(sent_count[lang],train_size,dev_size, sent_count[lang]-(train_size+dev_size))
    test_size = sent_count[lang]-(train_size+dev_size)
    # df1.append({'language' : lang, 'train_count' :train_size , 'dev_count' : dev_size,'test_count': sent_count[lang]-(train_size+dev_size)},
    #     ignore_index = True)

    dict = {'language' : lang, 'train_count' :train_size , 'dev_count' : dev_size,'test_count': test_size}
    df1 = pd.DataFrame([dict])
    df = pd.concat([df, df1], ignore_index = True)
    print(df)

    if not os.path.exists(OUTPUT_REF_PATH  + lang):
            os.makedirs(OUTPUT_REF_PATH  + lang)

    with open(INPUT_PATH + lang + '/' + f'{lang}-full.conll') as f, open(OUTPUT_REF_PATH  + lang + '/' + f'{lang}-train.conll','w') as f1,open(OUTPUT_REF_PATH  + lang + '/' + f'{lang}-dev.conll','w') as f2,open(OUTPUT_REF_PATH  + lang + '/' + f'{lang}-test.conll','w') as f3:
        for line in f:
            if " id " in line :
                #print(line)
                new_line = line
                #print(new_line)
                #print(line[5:])
                cnt = int(line[5:])
                #print(cnt)      
            else:
                new_line = line 
            
            if cnt <= train_size:
                # Write in train 
                #with open(OUTPUT_REF_PATH  + lang + '/' + f'{lang}-train.conll','a') as f1:
                f1.write(new_line)

            elif cnt >= train_size and cnt <= train_size + dev_size:
                # Write in train 
                #with open(OUTPUT_REF_PATH  + lang + '/' + f'{lang}-dev.conll','a') as f2:
                    #json.dump(d,fp,ensure_ascii=False)
                f2.write(new_line)
                    #fp.write('\n')
            
            elif cnt > train_size + dev_size and cnt <= sent_count[lang]:
                # Write in train 
                #with open(OUTPUT_REF_PATH  + lang + '/' + f'{lang}-test.conll','a') as f3:
                    #json.dump(d,fp,ensure_ascii=False)
                f3.write(new_line)
                    #fp.write('\n')
            else:
                continue

        

df.to_csv(OUTPUT_REF_PATH+'dataset-sizes.csv',index=None)



