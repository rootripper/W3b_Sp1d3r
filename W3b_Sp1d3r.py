import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_links(target_url):
    ## Make an HTTP request to the given URL
    response = requests.get(target_url)
    
    ## Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    ## Extract all links from the page
    links = set()
    for anchor in soup.find_all('a', href=True):
        link = anchor['href']
        full_url = urljoin(target_url, link)  ## Resolve relative URLs
        links.add(full_url)
    
    return links

def web_spider(start_url, depth=2):
    ## Sets to keep track of visited and to-visit URLs
    visited_urls = set()
    to_visit_urls = set([start_url])

    ## Perform a breadth-first search up to the specified depth
    for _ in range(depth):
        current_links = set()
        
        ## Process each URL at the current level
        while to_visit_urls:
            current_url = to_visit_urls.pop()
            
            ## Skip if the URL has already been visited
            if current_url in visited_urls:
                continue
            
            print(f"Visiting: {current_url}")
            visited_urls.add(current_url)

            ## Get links from the current URL
            new_links = get_links(current_url)
            current_links.update(new_links)

        ## Add newly discovered links to the to-visit set
        to_visit_urls.update(current_links - visited_urls)

if __name__ == "__main__":
    initial_url = input("Enter the initial URL: ")
    web_spider(initial_url, depth=2)
