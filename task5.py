import requests
from bs4 import BeautifulSoup
import csv

def extract_product_info(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Initialize a list to store product information
        products = []
        
        # Extract product information from the HTML
        for product in soup.find_all('article', class_='product_pod'):
            name = product.h3.a['title']
            price = product.find('p', class_='price_color').get_text(strip=True)
            rating = product.p['class'][1]  # Get the rating class
            
            # Append product information to the list
            products.append({
                'Name': name,
                'Price': price,
                'Rating': rating
            })
        
        return products
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch the webpage: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def save_to_csv(products, filename):
    try:
        # Write product information to a CSV file
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Name', 'Price', 'Rating']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write product information
            for product in products:
                writer.writerow(product)
        print(f"Product information has been saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving to CSV: {e}")

# URL of the e-commerce website to scrape
url = 'http://books.toscrape.com/catalogue/category/books/science_22/index.html'

# Extract product information
products = extract_product_info(url)

if products:
    # Save product information to a CSV file
    save_to_csv(products, 'products.csv')