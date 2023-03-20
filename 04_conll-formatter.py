import os 
import json

OUTPUT_REF_PATH = '/Users/rahulmehta/Desktop/IndicNER/datasets/conll-data-formatted/'
INPUT_PATH = '/Users/rahulmehta/Desktop/IndicNER/datasets/conll-data/'
#language_list = ['hi']

#language = 
language_list = ['gu','hi','kn','te','ta','ml','mr','or','pa','as','bn']

# train_count = 0 
# test_count = 0 
# dev_count = 0 

# Create train,test,dev split 
sent_dict = {}

for lang in language_list:
    print(lang)
    langcount = 0

    if not os.path.exists(OUTPUT_REF_PATH  + lang):
        os.makedirs(OUTPUT_REF_PATH  + lang)

    with open(INPUT_PATH + f'{lang}-conll.txt') as f,open(OUTPUT_REF_PATH  + lang + '/' + f'{lang}-full.conll','a') as f1:
        for line in f:
            #print(line)
            if ("id") not in line: 
                new_line = line.replace("__"," _ _ ")
            else:
                if("id") in line:
                    langcount+=1
                    new_line = line[0:4] + ' ' + str(langcount)  + '\n' # ' ' + line[10:]
                else:
                    new_line = line 

           

            #print(new_line)
            #with open(OUTPUT_REF_PATH  + lang + '/' + f'{lang}-full.conll','a') as fp:
                #json.dump(d,fp,ensure_ascii=False)
            f1.write(new_line)
                #fp.write('\n')
        sent_dict[lang] = langcount
        print("file written")


with open(OUTPUT_REF_PATH  + "sent-count.txt",'w') as fp:
    fp.write(json.dumps(sent_dict))



