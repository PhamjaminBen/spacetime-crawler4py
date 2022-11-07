import re
from urllib.parse import urlparse,urljoin
from bs4 import BeautifulSoup
import textProcess
import nltk
import json

log_dict = dict()
page_bit_lengths = set()

def logUpdate():
    log = open('logs.json', 'w')
    json.dump(log_dict, log)
    log.close()
    
    
def scraper(url, resp):
    #if page has no content or errors
    if not resp or not resp.raw_response or resp.status != 200:
        return list()
    
    #avoid crawling large content
    if len(resp.raw_response.content) > 1_000_000:
        return list()
    
    #skipped because duplicate page
    if len(resp.raw_response.content) in page_bit_lengths:
        return list()
    
    #add to set for duplicate detection
    page_bit_lengths.add(len(resp.raw_response.content))
    
    
    page = BeautifulSoup(resp.raw_response.content, "html.parser")
    page_text = textProcess.tokenize(page.text)
    
    #short stubs
    if len(page_text) < 50:
        return list()
    
    #pages with lots of reptition, not a lot of unique words are considered low information value
    elif len(set(page_text))/len(page_text) < 0.25:
        return list()
    
    #adding page and teext to dictionary to be saved to file
    log_dict[url] = page_text
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


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
    page = BeautifulSoup(resp.raw_response.content, "html.parser")
    urls = list()
    for link in page.findAll('a'):
        new_url = link.get('href')
        urls.append(new_url)
    return urls


def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        if not re.match(r".*(\.ics\.uci\.edu|\.cs\.uci\.edu|\.informatics\.uci\.edu|\.stat\.uci\.edu|today\.uci\.edu\/department\/information_computer_sciences).*", parsed.netloc):
            return False

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
