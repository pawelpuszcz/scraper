import urllib.request
from bs4 import BeautifulSoup
import csv

# opening a local file keyword.txt and read keywords to list

with open ('keywords.txt', 'r') as file:
    keywords = file.read().split('\n')

# definition for getting google search data (soup) with a keyword

def get_soup(keyword):
    url = f'https://google.com/search?q=site:https://www.searchenginejournal.com/+{keyword}'
    request = urllib.request.Request(url)                                                 
    request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    raw_response = urllib.request.urlopen(request).read()
    html = raw_response.decode("utf-8")             
    soup = BeautifulSoup(html, 'html.parser')
    return soup

num_links = []
total_links = []

# going through keywords list, going through google search data,
# extracting links and number of search results, putting these in above lists

for keyword in keywords:
    links = []
    divs = get_soup(keyword).select("#search div.g")
    for div in divs:
        results = div.select('a')
        items = str(results).split('"')
        for item in items:
            if item.startswith('http') and 'webcache' not in item and 'translate.google' not in item:
                links.append(item)
    num_links.append(len(links))
    total_links.append(links)
    

# creating text file to write total number of results along with kewords
with open('num-result-keyword.txt', 'w') as file:
    for num_link, keyword in zip(num_links, keywords):
        file.write(f'Total number of results: {num_link}, keyword: {keyword}\n')

# creating a csv file and write search results
data = [list(i) for i in zip(*total_links)]
file = open('links.csv', 'w', newline ='')
with file:    
    write = csv.writer(file)
    write.writerows([keywords])
    write.writerows(data)

'''
Scraping the “site” command.

Algorithm is as follows:
1. The program is looping through a list of keywords in the .txt file (keywords.txt)
2. Then it queries Google.com using the following set of queries:
a. site:https://www.searchenginejournal.com/ {keyword}
3. For every query, the program goes through Google Search Results and extracts all the
links from the first search result pointing to SearchEngineJournal.
4. The total number of results (the number above the first result) to be
extracted.
5. The program saves all the links pointing to SearchEngineJournal to a CSV file.
6. The total numbers of results to be saved in a different file along with the associated
keyword.
'''
        
    

