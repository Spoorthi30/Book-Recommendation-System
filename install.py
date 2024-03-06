import csv
import requests
from bs4 import BeautifulSoup

def scrape_flipkart_books(title, max_price, num_pages):
    # Prepare the search URL
    search_title = title.replace(' ', '+')
    base_url = "https://www.flipkart.com/books/pr?sid=bks"

    # Create a list to store book details
    book_data = []

    for page in range(1, num_pages+1):
        url = f"{base_url}&page={page}"

        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if request was unsuccessful

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the book items on the page
        book_items = soup.find_all('div', {'class': '_4ddWXP'})

        # Iterate over each book item and extract the details
        for book_item in book_items:
            # Extract the book title
            title_element = book_item.find('a', {'class': 's1Q9rs'})
            book_title = title_element.text.strip() if title_element else ''

            # Extract the book price
            price_element = book_item.find('div', {'class': '_30jeq3'})
            book_price = price_element.text.strip() if price_element else ''

            # Extract the book rating
            rating_element = book_item.find('div', {'class': '_3LWZlK'})
            book_rating = rating_element.text.strip() if rating_element else ''

            # Convert the book price to a numeric value
            book_price = book_price.replace('₹', '').replace(',', '')
            book_price = float(book_price) if book_price else 0.0

            # Check if the book meets the desired criteria
            if book_title and book_price <= max_price:
                # Append book details to the list
                book_data.append({
                    'Title': book_title,
                    'Price': book_price,
                    'Rating': book_rating
                })

    # Save the book details to a CSV file
    with open('book_details.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Price', 'Rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write each book's details as a row
        for book in book_data:
            writer.writerow(book)

# Example usage
scrape_flipkart_books('Python Programming', 500, num_pages=2097)







import csv

def read_book_details_csv(filename):
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        # Iterate over each row in the CSV file
        for row in reader:
            title = row['Title']
            price = float(row['Price'])
            rating = row['Rating']

            # Process the data as needed
            print(f"Title: {title}")
            print(f"Price: ₹{price}")
            print(f"Rating: {rating}")
            print('-' * 50)

# Example usage
read_book_details_csv('book_details.csv')
