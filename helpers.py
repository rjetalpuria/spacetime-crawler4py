import pickle
import crawler_globals
import analyze
from urllib.parse import urlparse, urlunparse, urldefrag
from bs4 import BeautifulSoup

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

# use soup parser to get textual content
# saves textual content as list of words and associate it with url in webpages dict
def acquire_text(url, tokens):
    # bsoup stipped_strings gives all strings on page without tags
    # added space keeps words separated after joining
    # anaylzer = TextAnalyzer()
    crawler_globals.webpages[url] = tokens

def update_common_words(url, commons):
    analyze.addFreq(commons, crawler_globals.common_words)

# checks if domain is subdomain of ics.uci.edu
def is_ics_sub(dom):
    return dom.endswith('.ics.uci.edu')

# if the domain is a subdomain, updates the running total
def update_ics_sub(url):
    dom = urlparse(url).netloc
    if is_ics_sub(dom):
        if dom not in crawler_globals.ics_subdomains:
            crawler_globals.ics_subdomains[dom] = 1
        else:
            crawler_globals.ics_subdomains[dom] += 1