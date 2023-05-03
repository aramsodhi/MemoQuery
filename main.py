"""
Objective: To identify premium and luxury online retailers, 
generally, and specifically those utilizing the Shopify ecommerce platform

Information about companies (in descending order of importance):
	1) Number of monthly unique visitors OR monthly/annual sales
	2) Ecommerce platform (Shopify, custom, or other)
	3) Key executives
	4) Location
	5) Product type (apparel, jewelry, etc.)
	6) ASPs (average selling prices?)
	7) Other (in-stock, shipping policies, etc.)
"""

from googleapiclient.discovery import build
import requests
from bs4 import BeautifulSoup

API_KEY = "AIzaSyBEMmPaOon7OVz19KnPgoYTdSvBThPAFv8"
SEARCH_ENGINE_ID = "833e399f990974ae0"

def search_on_domain(topic, domain):
	# Build the service object
    service = build('customsearch', 'v1', developerKey=API_KEY)

    # Define the search query with domain restriction
    query = f'site:{domain} {topic} "jewelry" OR "luxury goods" OR "luxury retailers"'

    # Execute the search using Google Custom Search API
    response = requests.get(f'https://www.googleapis.com/customsearch/v1?q={query}&cx=YOUR_SEARCH_ENGINE_ID&key={API_KEY}')
    search_results = []
    for item in response.json().get('items', []):
        title = item['title']
        link = item['link']
        snippet = item['snippet']

        # Make a request to the SimilarWeb API and extract additional information
        headers = {'c5f0bba28c864a68afe1624ec961b763': API_KEY}
        response = requests.get(f'https://api.similarweb.com/v1/website/{domain}/traffic-and-engagement/visits?api_key={API_KEY}')
        if response.status_code == 200:
            data = response.json()['visits']
            monthly_visitors = data['monthly']
            location = data['country']
            ecommerce_platform = data['category']
        else:
            monthly_visitors = None
            location = None
            ecommerce_platform = None

        search_results.append({
            'title': title,
            'link': link,
            'snippet': snippet,
            'monthly_visitors': monthly_visitors,
            'ecommerce_platform': ecommerce_platform,
            'location': location
        })

    return search_results

print("\n\n")
results = search_on_domain('jewelry and luxury goods retailers', 'similarweb.com')
for result in results:
    print(result['title'])
    print(result['link'])
    print(result['snippet'])
    print(f"Monthly visitors: {result['monthly_visitors']}")
    print(f"Ecommerce platform: {result['ecommerce_platform']}")
    print(f"Location: {result['location']}")
    print('--------------------')