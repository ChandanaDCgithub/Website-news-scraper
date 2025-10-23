"""
News Headline Scraper

A simple tool to scrape headlines from news websites.

Requirements:
- Python 3.x
- requests
- beautifulsoup4

Usage:
    python news_headline_scraper.py [url] [output_file]

Example:
    python news_headline_scraper.py https://news.ycombinator.com headlines.txt
"""

import sys
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone

def fetch_headlines(url, max_headlines=30):
    """
    Fetch headlines from a news website.
    
    Args:
        url (str): The URL of the news website
        max_headlines (int): Maximum number of headlines to fetch
        
    Returns:
        list: A list of headline strings
    """
    # Set a user agent to avoid being blocked
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        # Send HTTP request to the URL
        response = requests.get(url, headers=headers, timeout=10)
        
        # Raise an exception for bad status codes
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # List to store headlines
        headlines = []
        
        # Different websites have different HTML structures
        # Here are some common patterns to look for headlines
        
        # 1. Check for Hacker News (a common and accessible news site)
        if "ycombinator.com" in url or "news.ycombinator.com" in url:
            for title in soup.select(".titleline > a"):
                headlines.append(title.get_text(strip=True))
        
        # 2. Look for headlines in article tags with heading elements
        if not headlines:
            for article in soup.find_all("article"):
                for heading in article.find_all(["h1", "h2", "h3", "h4"]):
                    text = heading.get_text(strip=True)
                    if text and len(text) > 5:  # Avoid very short texts
                        headlines.append(text)
        
        # 3. Look for common headline class names
        if not headlines:
            headline_selectors = [
                ".headline", ".title", ".article-title", ".story-title",
                ".entry-title", ".post-title", ".news-title"
            ]
            for selector in headline_selectors:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text(strip=True)
                    if text and len(text) > 5:
                        headlines.append(text)
        
        # 4. Look for heading elements with title-related classes
        if not headlines:
            for heading in soup.find_all(["h1", "h2", "h3"]):
                classes = heading.get("class", [])
                if any(c for c in classes if "title" in c.lower() or "headline" in c.lower()):
                    text = heading.get_text(strip=True)
                    if text and len(text) > 5:
                        headlines.append(text)
        
        # 5. As a last resort, just get all headings
        if not headlines:
            for heading in soup.find_all(["h1", "h2"]):
                text = heading.get_text(strip=True)
                if text and len(text) > 5:
                    headlines.append(text)
        
        # Remove duplicates while preserving order
        unique_headlines = []
        seen = set()
        for headline in headlines:
            if headline not in seen:
                seen.add(headline)
                unique_headlines.append(headline)
        
        # Limit to max_headlines
        return unique_headlines[:max_headlines]
        
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

def save_headlines(headlines, output_file):
    """
    Save headlines to a text file.
    
    Args:
        headlines (list): List of headline strings
        output_file (str): Path to the output file
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            # Add a timestamp header
            timestamp = datetime.now(timezone.utc).isoformat()
            file.write(f"# Headlines scraped on {timestamp}\n\n")
            
            # Write each headline with a number
            for i, headline in enumerate(headlines, 1):
                file.write(f"{i}. {headline}\n")
                
        print(f"Successfully saved {len(headlines)} headlines to {output_file}")
        return True
    except IOError as e:
        print(f"Error saving headlines to file: {e}")
        return False

def main():
    # Default values
    url = "https://news.ycombinator.com"  # Hacker News is a good default
    output_file = "headlines.txt"
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        url = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    print(f"Fetching headlines from: {url}")
    headlines = fetch_headlines(url)
    
    if not headlines:
        print("No headlines found. The website might have a different structure or blocked the request.")
        return 1
    
    print(f"Found {len(headlines)} headlines.")
    if save_headlines(headlines, output_file):
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())