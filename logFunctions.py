import json
import re
from collections import defaultdict
from urllib.parse import urlparse
import textProcess

def printStats():
    with open('logs.json','r') as log:
        data = json.load(log)
    
    ics_subdomains = defaultdict(int)
    all_urls = set()
    longest_words = 0
    longest_url = ""
    words = defaultdict(int)

    #iterate through json file dict
    for url,tokens in data.items():
        for token in tokens:
            words[token] += 1
        
        #defrag urls for uniqueness
        url = urlparse(url)._replace(fragment="").geturl()
        all_urls.add(url)
        
        #add to ics subdomains if match
        if re.match(r".*\.ics\.uci\.edu.*", url):
            ics_subdomains[urlparse(str(url)).hostname] +=1
            
        #for finding longest page
        if len(tokens) > longest_words:
            longest_words = len(tokens)
            longest_url = url
            
    #sorts words by frequency
    sorted_words = sorted(words, key = lambda x: words[x], reverse = True)
    
    #sorts the ics subdomains by name
    sorted_domains = sorted(ics_subdomains, key = lambda x: (x,ics_subdomains[x]))
        
    # print report
    print()
    print("=========================================STATISTICS==============================")
    print("Number of unique pages:", len(all_urls))
    print()

    print("Longest Page:", longest_url, "with", longest_words, "words.")
    print()

    print("50 most common words:")
    for word in sorted_words[:50]:
        print(word,'->',words[word])
    print()

    print("All ics.uci.edu subdomains:")
    print("Count:", len(ics_subdomains))
    for url in sorted_domains:
        print(url,",", ics_subdomains[url])

#refreshes the log file
def clearLog():
    open("logs.json",'w').close()
    
if __name__ == '__main__':
    printStats()