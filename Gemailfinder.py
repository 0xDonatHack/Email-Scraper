# # # 

# # import asyncio
# # import pandas as pd
# # from playwright.async_api import async_playwright
# # from bs4 import BeautifulSoup

# # async def scrape_email_from_url(url, page):
# #     try:
# #         await page.goto(url)
# #         await page.wait_for_load_state("networkidle")
# #         html = await page.content()
# #         soup = BeautifulSoup(html, 'html.parser')
# #         emails = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('mailto:')]
# #         return emails
# #     except Exception as e:
# #         print(f"Error scraping email from {url}: {e}")
# #         return []

# # async def main():
# #     # Load CSV file
# #     df = pd.read_csv('hamburg.csv')

# #     # Get list of URLs from CSV file
# #     urls = df['Url'].tolist()

# #     async with async_playwright() as p:
# #         browser = await p.chromium.launch()
# #         context = await browser.new_context()
# #         page = await context.new_page()

# #         # Scrape email from each URL
# #         tasks = [scrape_email_from_url(url, page) for url in urls]
# #         results = await asyncio.gather(*tasks)

# #         # Create a new column in the DataFrame with the scraped emails
# #         df['Email'] = [' '.join(emails) for emails in results]

# #         # Save the updated DataFrame to a new CSV file
# #         df.to_csv('output.csv', index=False)

# #         await browser.close()

# # if __name__ == "__main__":
# #     asyncio.run(main())

# import asyncio
# import pandas as pd
# from playwright.async_api import async_playwright
# from bs4 import BeautifulSoup
# import urllib.parse

# async def scrape_email_from_url(url, page):
#     try:
#         # URL encode the URL
#         encoded_url = urllib.parse.quote(url, safe=':/?&=')
        
#         # Remove the quotes from the URL
#         encoded_url = encoded_url.replace('%22', '')
        
#         await page.goto(encoded_url)
#         await page.wait_for_load_state("networkidle")
#         html = await page.content()
#         soup = BeautifulSoup(html, 'html.parser')
#         emails = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('mailto:')]
#         return emails
#     except Exception as e:
#         print(f"Error scraping email from {url}: {e}")
#         return []

# async def main():
#     # Load CSV file
#     df = pd.read_csv('hamburg.csv')

#     # Get list of URLs from CSV file
#     urls = df['Url'].tolist()

#     async with async_playwright() as p:
#         browser = await p.chromium.launch()
#         context = await browser.new_context()
#         page = await context.new_page()

#         # Scrape email from each URL
#         tasks = [scrape_email_from_url(url, page) for url in urls]
#         results = await asyncio.gather(*tasks)

#         # Create a new column in the DataFrame with the scraped emails
#         df['Email'] = [' '.join(emails) for emails in results]

#         # Save the updated DataFrame to a new CSV file
#         df.to_csv('output.csv', index=False)

#         await browser.close()

# if __name__ == "__main__":
#     asyncio.run(main())


#------------------------------------------------------------------------------------------#

# from playwright.async_api import Playwright, async_playwright
# import asyncio
# import re
# import csv

# urls = []
# rows = []

# # Read the existing CSV file
# with open("hamburg.csv", "r", encoding='utf-8') as file:
#     reader = csv.reader(file)
#     headers = next(reader)  # Save the headers
#     for row in reader:
#         urls.append(row[5].replace('"', '').replace('"', ''))
#         rows.append(row)
#     print(f"Loaded {len(urls)} URLs")


# async def scrape_emails_from_url(playwright: Playwright, url: str, max_retries=2):
#     for attempt in range(max_retries + 1):
#         try:
#             browser = await playwright.chromium.launch(headless=False)
#             context = await browser.new_context()
#             page = await context.new_page()
#             await page.goto(url, timeout=30000)  #30 seconds timeout
#             await page.wait_for_load_state('networkidle', timeout=60000)
#             html = await page.content()
#             email_addresses = re.findall(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', html)
#             await browser.close()
#             print(email_addresses)
#             return set(email_addresses)
#         except Exception as e:
#             await browser.close()
#             if attempt < max_retries:
#                 print(f"Error scraping {url}: {str(e)}. Retrying... (Attempt {attempt + 1} of {max_retries})")
#                 await asyncio.sleep(5)  # Wait for 5 seconds before retrying
#             else:
#                 print(f"Failed to scrape {url} after {max_retries + 1} attempts: {str(e)}")
#                 return []

# async def scrape_emails_from_urls(urls, batch_size=5):
#     all_emails = []
#     async with async_playwright() as playwright:
#         for i in range(0, len(urls), batch_size):
#             batch = urls[i:i+batch_size]
#             tasks = [scrape_emails_from_url(playwright, url) for url in batch]
#             results = await asyncio.gather(*tasks)
#             all_emails.extend(results)
#             print(f"Batch {i // batch_size + 1} completed out Of {int((len(urls)/5) + 1)}")
#     return all_emails

# async def main():
#     emails = await scrape_emails_from_urls(urls)
#     set(emails)
#     # Add the new column header
#     headers.append("Emails")
    
#     # Append emails to rows
#     for row, email_list in zip(rows, emails):
#         row.append(", ".join(email_list))
    
#     # Write the updated data back to the CSV file
#     with open("hamburg_updated.csv", "w", newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(headers)
#         writer.writerows(rows)
    
#     print("Updated CSV file has been created as 'hamburg_updated.csv'")

# asyncio.run(main())

#------------------------------------------------------------------------------------------#


import pandas as pd
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from playwright.async_api import Playwright, async_playwright
import aiohttp, asyncio, csv, re , subprocess , sys

# Initialize variables
urls = []
rows = []

# Define Nominatim URL
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

# Load URLs and rows from CSV
with open("output.csv", "r", encoding='utf-8') as file:
    reader = csv.reader(file)
    headers = next(reader)  # Save the headers
    for row in reader:
        urls.append(row[7].replace('"', '').replace('"', ''))
        rows.append(row)
    print(f"Loaded {len(urls)} URLs")

# Function to get coordinates with retry logic
async def get_coordinates(address, session, retries=3):
    for attempt in range(retries):
        try:
            async with session.get(NOMINATIM_URL, params={"q": address, "format": "json", "limit": 1}, timeout=7) as response:
                if response.status == 200:
                    data = await response.json()
                    if data:
                        return float(data[0]["lat"]), float(data[0]["lon"])
                return None, None
        except (asyncio.TimeoutError, aiohttp.ClientError, GeocoderTimedOut, GeocoderUnavailable):
            await asyncio.sleep(1)  # Wait 1 second before retrying
    return "NA", "NA"  # Return "NA" if all retries fail

# Asynchronous function to process all addresses
async def geocode_addresses(df):
    async with aiohttp.ClientSession() as session:
        tasks = [get_coordinates(address, session) for address in df['Address']]
        return await asyncio.gather(*tasks)

# Function to scrape emails from URLs
async def scrape_emails_from_url(playwright: Playwright, url: str, max_retries=1):
    for attempt in range(max_retries + 1):
        try:
            browser = await playwright.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            if url != "NA":
                await page.goto(url, timeout=30000)
            await page.wait_for_load_state('networkidle', timeout=60000)
            html = await page.content()
            email_addresses = re.findall(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', html)
            await browser.close()
            return set(email_addresses)
        except Exception as e:
            await browser.close()
            if attempt < max_retries:
                print(f"Error scraping {url}: {str(e)}. Retrying... (Attempt {attempt + 1} of {max_retries})")
                await asyncio.sleep(5)
            else:
                print(f"Failed to scrape {url} after {max_retries + 1} attempts: {str(e)}")
                return set()

# Function to process email scraping in batches
async def scrape_emails_from_urls(urls, batch_size=5):
    all_emails = []
    async with async_playwright() as playwright:
        for i in range(0, len(urls), batch_size):
            batch = urls[i:i+batch_size]
            tasks = [scrape_emails_from_url(playwright, url) for url in batch]
            results = await asyncio.gather(*tasks)
            all_emails.extend(results)
            print(f"Batch {i // batch_size + 1} completed out of {int((len(urls) / batch_size) + 1)}")
    return [", ".join(emails) if emails else "NA" for emails in all_emails]

# Main function to perform both scraping and geocoding
async def main():
    # Start email scraping
    emails = await scrape_emails_from_urls(urls)

    # Prepare DataFrame for geocoding
    df = pd.DataFrame(rows, columns=headers)
    
    # Start geocoding addresses
    coordinates = await geocode_addresses(df)
    latitudes, longitudes = zip(*coordinates)
    df['latitude'], df['longitude'] = latitudes, longitudes

    # Update rows with emails, latitude, and longitude separately
    headers.extend(["emails", "latitude", "longitude"])
    for row, email, (lat, lon) in zip(rows, emails, coordinates):
        row.extend([email, lat if lat != "NA" else "NA", lon if lon != "NA" else "NA"])

    # Write the updated data back to the CSV file
    with open("output.csv", "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)
    
    print("Updated CSV file has been created as 'output.csv'")
    subprocess.run([sys.executable, "analysis.py"])

# Run the main function
asyncio.run(main())
