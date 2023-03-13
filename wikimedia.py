import requests
from collections import defaultdict

# Get list of entities and produced entity:qid pairs
def get_wikimedia_id(subject,language):  

    #subject = "बम्बई|दिल्ली|बम्बई|महेंद्र सिंह ठाकुर"

    url = f'https://{language}.wikipedia.org/w/api.php'
    print(url)
    params = {
            'action': 'query',
            'format': 'json',
            'titles': "बम्बई|दिल्ली",
            'prop': 'pageprops',
            'ppprop' :'wikibase_item',
            'exintro': True,
            #'explaintext': True,
            'redirects' :1
            
        }
    
    d = defaultdict()
    print(d)

    # for i in range(3):
    #     print(i)
    response = requests.get(url, params=params)
    data = response.json()
    #print(data)
    
    p = dict(data['query']['pages'])
    for i in p.keys():
        print(i)
        d[p[i]['title']] = p[i]['pageprops']['wikibase_item']

    print(d)
    return(d)

