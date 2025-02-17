import requests
from bs4 import BeautifulSoup
import csv
import time

#URL of the website
base_url = "https://books.toscrape.com/catalogue/page-{}.html"

# browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

# List to store book data
books = []

# Loop through multiple pages 
for page in range(1, 6):  
    print(f"Scraping page {page}...")
    url = base_url.format(page)
    
    # Send request
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Parse content
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all book containers
        book_containers = soup.find_all("article", class_="product_pod")
        
        for book in book_containers:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").get_text(strip=True)
            rating = book.find("p")["class"][1]  

            books.append([title, price, rating])
        
        time.sleep(2)  # Respectful delay to avoid overwhelming the server

    else:
        print(f"Failed to fetch page {page}. Status Code: {response.status_code}")
        break

# Save data to CSV
with open("books_scraped.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price", "Rating"])
    writer.writerows(books)

print("Data successfully saved to books_scraped.csv")