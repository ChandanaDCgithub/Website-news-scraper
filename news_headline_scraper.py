import requests
from bs4 import BeautifulSoup

def fetch_headlines():
    # Website URL (you can change it to any other)
    url = "https://www.bbc.com/news"

    # Fetch webpage content
    response = requests.get(url)
    response.raise_for_status()  # Throws error if site not reachable

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all <h2> tags (BBC headlines are usually in these)
    headlines = soup.find_all("h2")

    # Extract clean text
    cleaned_headlines = [h.get_text(strip=True) for h in headlines if h.get_text(strip=True)]

    # Save to .txt file
    with open("headlines.txt", "w", encoding="utf-8") as f:
        for line in cleaned_headlines:
            f.write(line + "\n")

    print(f"✅ {len(cleaned_headlines)} headlines saved to 'headlines.txt'")

if __name__ == "_main_":
    fetch_headlines()
