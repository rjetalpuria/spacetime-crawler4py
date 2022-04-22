import pickle


def initialize():
    # {url : [words]}
    # can be use for report questions after crawling finished
    # nb: may need to switch to creating files to hold webpage content if not enough ram?
    #       Alternatively, come up with a more adhoc solution to report
    global webpages 
    webpages = dict()

    # {word : freq}
    # running total of all words/freq found across all 'is_valid' pages
    global common_words 
    common_words = dict()

    # {subdomain : count}
    # running total of ics.uci.edu subdomains found
    global ics_subdomains 
    ics_subdomains = dict()

    global hash_val 
    hash_val = {}  # to store the urls and its respective hash values

# def save_globals():  
#     with open("webpages.pkl", "wb") as file:
#         pickle.dump(webpages, file)
#     with open("common_words.pkl", "wb") as file:
#         pickle.dump(common_words, file)
#     with open("ics_subdomains.pkl", "wb") as file:
#         pickle.dump(ics_subdomains, file)
#     with open("hash_val.pkl", "wb") as file:
#         pickle.dump(hash_val, file)
        
# def load_globals():
#     with open("webpages.pkl", "rb") as file:
#         webpages = pickle.load(file)
#     with open("common_words.pkl", "rb") as file:
#         common_words = pickle.load(file)
#     with open("ics_subdomains.pkl", "rb") as file:
#         ics_subdomains = pickle.load(file)
#     with open("hash_val.pkl", "rb") as file:
#         hash_val = pickle.load(file)
#     print(">>>webpages: ", len(webpages))