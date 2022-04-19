import re
from urllib.parse import urlparse
from urllib.parse import urldefrag # used to remove the fragment part from url
from bs4 import BeautifulSoup

from analyze import TextAnalyzer

valid_domains = ('.ics.uci.edu', '.cs.uci.edu', '.informatics.uci.edu', '.stat.uci.edu')

# {url : text}
# can be use for report questions after crawling finished
# nb: may need to switch to creating files to hold webpage content if not enough ram?
#       Alternatively, come up with a more adhoc solution to report
webpages = dict()

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

# use soup parser to get textual content
# saves textual content as one big string and associate it with url in webpages dict
def aquire_text(soup):
    # bsoup stipped_strings gives all strings on page without tags
    # added space keeps words separated after joining
    webpages[url] = ''.join((s + ' ' for s in soup.stripped_strings))

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    links = list()
    print('url: ', url)
    print('resp.url: ', resp.url)
    if(resp.status >= 200 and resp.status < 300):
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')

        aquire_text(url, soup)
        
        for link in soup.find_all('a'):
            if(is_valid(link.get('href'))):
                links.append(urldefrag(link.get('href'))[0]) #defragment the url before appending
    
    return links

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if not(parsed.netloc.endswith(valid_domains)): #check if a url falls within our domains
            return False
        print(urlparse(url))
        
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
