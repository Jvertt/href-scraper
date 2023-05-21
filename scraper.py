import requests
from bs4 import BeautifulSoup
import pyperclip
from urllib.parse import urljoin

def is_social_media_url(url):
    # Define a list of social media domains
    social_media_domains = ["twitter.com", "facebook.com", "instagram.com", "linkedin.com"]

    # Check if the URL's domain matches any social media domain
    for domain in social_media_domains:
        if domain in url:
            return True

    return False

def get_links_from_page(url, limit=100):
    # Send a GET request to the specified URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all <a> tags in the parsed HTML
    links = soup.find_all('a')

    # Extract the href attribute from each <a> tag
    href_links = []
    scraped_urls = set()  # Keep track of scraped URLs

    for link in links:
        href = link.get('href')
        if href:
            full_url = urljoin(url, href)
            if not is_social_media_url(full_url) and "betalist.com/startups/" in full_url:
                if full_url not in scraped_urls:  # Check if URL has already been scraped
                    href_links.append(full_url)
                    scraped_urls.add(full_url)
                    if len(href_links) >= limit:
                        break

    # Return the list of href links
    return href_links

# Prompt the user to enter a root URL
root_url = input("Enter the root URL: ")

# Call the function to retrieve the href links from the page with a limit of 100
href_links = get_links_from_page(root_url, limit=100)

# Copy the extracted href links to the clipboard
links_text = '\n'.join(href_links)
pyperclip.copy(links_text)

# Print a message to indicate the links have been copied
print("Href links have been copied to the clipboard.")
