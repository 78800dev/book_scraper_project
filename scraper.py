import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# --- (1) Wrap your existing scraping logic into a function ---
def scrape_single_page(page_url):
    """
    Scrapes book data (Title, Price, Rating) from a single given URL.
    Returns a list of dictionaries, where each dictionary represents a book.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(page_url, headers=headers)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        # Fix the encoding issue
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')

        books_data = [] # Local list for books on this specific page
        books = soup.find_all('article', class_='product_pod')

        for book in books:
            title_tag = book.find('h3').find('a')
            title = title_tag['title'] if title_tag else 'N/A'

            price_tag = book.find('p', class_='price_color')
            price = price_tag.text.strip().replace('£', '') if price_tag else 'N/A'

            rating_tag = book.find('p', class_='star-rating')
            rating = 'N/A'
            if rating_tag:
                rating_word = rating_tag['class'][1] if len(rating_tag['class']) > 1 else 'N/A'
                rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
                rating = rating_map.get(rating_word, 'N/A')

            book_info = {
                'Title': title,
                'Price': price,
                'Rating': rating
            }
            books_data.append(book_info)
        return books_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {page_url}: {e}")
        return [] # Return an empty list if there's a request error
    except Exception as e:
        print(f"An unexpected error occurred while processing {page_url}: {e}")
        return [] # Return an empty list for other errors

# --- (2) Add the scrape_all_pages function and main execution block ---
if __name__ == "__main__":
    base_url = "http://books.toscrape.com/catalogue/"
    # From inspection, we know there are 50 pages for this site.
    total_pages_to_scrape = 50

    all_scraped_books = [] # This list will hold data from ALL pages

    print(f"Starting to scrape {total_pages_to_scrape} pages from {base_url}...")

    for page_num in range(1, total_pages_to_scrape + 1):
        page_url = f"{base_url}page-{page_num}.html"
        print(f"Scraping page {page_num}/{total_pages_to_scrape}: {page_url}")

        # Call the function to scrape data from the current page
        current_page_data = scrape_single_page(page_url)

        # Add the data from the current page to our master list
        all_scraped_books.extend(current_page_data)

        # BE POLITE: Pause for a short while between requests
        # This helps prevent your IP from getting blocked by the website
        time.sleep(1) # Wait 1 second (adjust as needed, 0.5 to 2 seconds is common)

    print(f"\nFinished scraping. Total books found: {len(all_scraped_books)}")

    # --- Next: Convert to DataFrame and Save to CSV (Coming in next step!) ---
    # For now, let's just print a confirmation
   
        # --- Convert to DataFrame and Save to CSV ---
    if all_scraped_books: # Only proceed if some data was actually scraped
        # Convert the list of dictionaries to a Pandas DataFrame
        df = pd.DataFrame(all_scraped_books)

        # Optional: Further Data Cleaning/Type Conversion (Good Practice)
        # Convert 'Price' to numeric (float), coercing errors to NaN
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        # Convert 'Rating' to numeric (integer), coercing errors to NaN, then to nullable integer type
        df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce').astype('Int64')

        print("\nDataFrame created. Data types after cleaning:")
        print(df.dtypes)
        print(f"\nFirst 5 rows of the complete DataFrame:\n{df.head()}")

        # Define the output CSV file name
        output_csv_file = 'books_data.csv'

        # Save the DataFrame to a CSV file
        # index=False prevents pandas from writing the DataFrame index as a column in the CSV
        df.to_csv(output_csv_file, index=False)

        print(f"\nSuccessfully saved all scraped data to '{output_csv_file}' in your project folder.")
    else:
        print("\nNo data was available to save to CSV.")
        print("First 5 entries of the complete dataset:")
        for i, book_data in enumerate(all_scraped_books[:5]):
            print(f"  Book {i+1}: {book_data}")
 