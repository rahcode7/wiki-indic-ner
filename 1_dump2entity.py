import _pickle as cPickle

filepath = "/Users/rahulmehta/Desktop/IndicNER/data-wikidumps/clean-dumps/clean_pawiki-20230301-pages-articles-multistream.pkl"


with open(filepath, "rb") as input_file:
    e = cPickle.load(input_file)

print(len(e))


# from itertools import islice

# def take(n, iterable):
#     """Return the first n items of the iterable as a list."""
#     return list(islice(iterable, n))

# n_items = take(2, e.items())
# print(n_items)

# for i in range(10):
#     print("Title",title)
#     print(articles[])
    


# # For each article, for each entity
# article_dict = {}
# for i,val in enumerate(articles):
#     # entity list format = "बम्बई"|"दिल्ली"
#     article_dict[titles[i]] = get_wikimedia_id(val['entity_list']) 




