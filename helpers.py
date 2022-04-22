import pickle
import crawler_globals

def save_globals():  
    with open("webpages.pkl", "wb") as file:
        pickle.dump(crawler_globals.webpages, file)
    with open("common_words.pkl", "wb") as file:
        pickle.dump(crawler_globals.common_words, file)
    with open("ics_subdomains.pkl", "wb") as file:
        pickle.dump(crawler_globals.ics_subdomains, file)
    with open("hash_val.pkl", "wb") as file:
        pickle.dump(crawler_globals.hash_val, file)
        
def load_globals():
    with open("webpages.pkl", "rb") as file:
        crawler_globals.webpages = pickle.load(file)
    with open("common_words.pkl", "rb") as file:
        crawler_globals.common_words = pickle.load(file)
    with open("ics_subdomains.pkl", "rb") as file:
        crawler_globals.ics_subdomains = pickle.load(file)
    with open("hash_val.pkl", "rb") as file:
        crawler_globals.hash_val = pickle.load(file)
    print(">>>webpages: ", len(crawler_globals.webpages))