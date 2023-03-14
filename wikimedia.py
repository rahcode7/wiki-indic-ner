import requests
from collections import defaultdict

# Get list of entities and produced entity:qid pairs
def get_wikimedia_ids(entity,language):  

    #subject = "बम्बई|दिल्ली|बम्बई|महेंद्र सिंह ठाकुर"
    piped = ""
    #print(len(entity))
    for item in entity:
        piped += item + "|"
    #print(piped)

    #language = "hi"
    url = f'https://{language}.wikipedia.org/w/api.php'
    print(url)
    params = {
            'action': 'query',
            'format': 'json',
            'titles': piped,
            'prop': 'pageprops',
            'ppprop' :'wikibase_item',
            'exintro': True,
            #'explaintext': True,
            'redirects' :1   
        }
    
    d = defaultdict()
    #print(d)

    # for i in range(3):
    #     print(i)
    response = requests.get(url, params=params)
    data = response.json()
    #print(data)
    
    p = dict(data['query']['pages'])
    for i in p.keys():
        if int(i) < 0:
            d[p[i]['title']] = -1
        else:
            try:
                d[p[i]['title']] = p[i]['pageprops']['wikibase_item']
            except:
                pass

    #print(d)
    return(d)
