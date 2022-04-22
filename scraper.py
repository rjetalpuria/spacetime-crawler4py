import re
from urllib.parse import urlparse, urlunparse
from urllib.parse import urldefrag # used to remove the fragment part from url
from bs4 import BeautifulSoup
import urllib.robotparser
from analyze import tokenizeText, computeWordFrequencies, addFreq, printTopNFreq, similarity_detection
from utils import get_urlhash

valid_domains = ('.ics.uci.edu', '.cs.uci.edu', '.informatics.uci.edu', '.stat.uci.edu')

# {url : [words]}
# can be use for report questions after crawling finished
# nb: may need to switch to creating files to hold webpage content if not enough ram?
#       Alternatively, come up with a more adhoc solution to report
webpages = dict()

# {word : freq}
# running total of all words/freq found across all 'is_valid' pages
common_words = dict()

# {subdomain : count}
# running total of ics.uci.edu subdomains found
ics_subdomains = dict()

def write_report():
    try:
        with open('report.txt', 'w') as report:
            # num of webpages found
            report.write('Num Unique Pages: ' + str(len(webpages)) + '\n\n')

            # longest webpage in num words
            # stopwords do not count toward length
            longest_len = -1
            longest_url = ''
            for url, words in webpages.items():
                if len(words) > longest_len:
                    longest_url = url
                    longest_len = len(words)
            report.write('Longest Webpage: ' + longest_url + '\n\n')

            # find 50 top words
            report.write('50 Common Words:\n')
            printTopNFreq(common_words, 50, report)
            report.write('\n')

            # list ics.uci.edu subdomains
            report.write('Num ics subdomains: ' + str(len(ics_subdomains)) + '\n')
            for sub,cnt in sorted(ics_subdomains.items()):
                report.write(sub + ', ' + str(cnt) + '\n')
    finally:
        pass


def scraper(url, resp):
    links = extract_next_links(url, resp)

    # could find better place for this, but leaving it here for now
    write_report() # update report statistics as we go
    
    return links

# use soup parser to get textual content
# saves textual content as list of words and associate it with url in webpages dict
def aquire_text(url, soup):
    # bsoup stipped_strings gives all strings on page without tags
    # added space keeps words separated after joining
    # anaylzer = TextAnalyzer()
    webpages[url] = tokenizeText(''.join((s + ' ' for s in soup.stripped_strings)))

def update_common_words(url):
    addFreq(computeWordFrequencies(webpages[url]), common_words)

# checks if domain is subdomain of ics.uci.edu
def is_ics_sub(dom):
    return dom.endswith('.ics.uci.edu')

# if the domain is a subdomain, updates the running total
def update_ics_sub(url):
    dom = urlparse(url).netloc
    if is_ics_sub(dom):
        if dom not in ics_subdomains:
            ics_subdomains[dom] = 1
        else:
            ics_subdomains[dom] += 1

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

        uhash = get_urlhash(url)
        #  we are checkin the similar detection in this because after this we will add the url to our tbd list
        # so to prevent the duplicate urls, we are validating in this function.
        if not similarity_detection(uhash, soup):
            aquire_text(url, soup)
            # print(webpages[url][:100]) #debug

            # after making sure page is not a dup, update common words tally
            update_common_words(url)

            # update count of ics subdomains
            update_ics_sub(url)
            
            parsed_url = urlparse(url) # get the scheme and domain incase links are relative
            # loop through all links
            for link in soup.find_all('a'):
                href = urldefrag(link.get('href'))[0]
                if isinstance(href, bytes):
                    href = href.decode("ascii")
                print('processing next url: ' + href) #debug
                
                # parse the url
                next_url_parsed = urlparse(href)

                # check how the url is given
                # make adjustments to get full, absolute url
                # print(href) 
                # print(next_url_parsed)
                if(not next_url_parsed.path.startswith('/')): # relative to current page
                    print('adding current path') #debug
                    next_url_parsed = next_url_parsed._replace(path = parsed_url.path + next_url_parsed.path) # add the current path
                if(next_url_parsed.netloc == ''): # relative to root
                    print('adding domain') #debug
                    next_url_parsed = next_url_parsed._replace(netloc = parsed_url.netloc) # add the domain
                if(next_url_parsed.scheme == ''): # no scheme
                    print('adding scheme') #debug
                    next_url_parsed = next_url_parsed._replace(scheme = parsed_url.scheme) # add the current page's scheme

                # reconstruct the url
                next_url = urlunparse(next_url_parsed)

                if(is_valid(next_url)): # check if we want to add url to frontier
                    print('adding url to frontier: ' + next_url) #debug
                    links.append(next_url) #defragment the url before appending
    
    return links

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        print('checking is valid: ' + url) #debug
        parsed = urlparse(url)

        if url in webpages: # simple 'have we been here before' check
            return False
        if parsed.scheme not in set(["http", "https"]):
            return False
        if not(parsed.netloc.endswith(valid_domains)): #check if a url falls within our domains
            if parsed.netloc != "today.uci.edu" or not parsed.path.startswith('/department/information_computer_sciences'):
                return False
        # print(urlparse(url)) #debug
        dom = urlparse(url).netloc  # getting the domain of the url
        sch = urlparse(url).scheme  # getting the scheme of the url
        rop = urllib.robotparser.RobotFileParser() # using robotparser
        rfile = f'{sch}://{dom}/robots.txt'  # now r is the path of the robots.txt file of the url
        
        ## Check if the url is ASCII
        if not (len(rfile) == len(rfile.encode())): 
            rfile.decode('ascii') # convert the path into ascii if is not in ascii format 
            # print("Conver to ASCII\n")
            
        rop.set_url(rfile)  # reading the robots.txt file
        rop.read()
        if not rop.can_fetch("*", url):  # checking if we are permitted to read the url
            return False
        # print('robots passed') #debug

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
