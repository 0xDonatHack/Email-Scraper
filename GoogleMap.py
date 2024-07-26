# #-------------------------------------------Incase Data_Cleaning Not Working---------------------------------------------#

# import csv

# with open("hamburg_updated.csv", "r", encoding='utf-8') as file:
#     reader = csv.reader(file)
#     data = [row for row in reader]

# for row in data:
#     for i, value in enumerate(row):
#         row[i] = value.replace('"', '').replace('""' , '')
#         if i == 4:
#             row[i] = row[i].replace('', '')
# with open("hamburg.csv", "w", newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerows(data)

#--------------------------------------------------Final Code----------------------------------------------------------#

# import asyncio , csv , os
# from playwright.async_api import async_playwright


# async def scrape_google_maps_data():
#     name_sheet = "hamburg.csv"
#     google_url = "https://www.google.com/maps/search/restaurants+in+Berlin,+Germany/@53.0190216,10.3987354,8z/data=!3m1!4b1?entry=ttu"

#     print("Execution Time:")
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)
#         page = await browser.new_page()
#         await page.goto(google_url)

#         # Wait for the initial selector or increase timeout if necessary
#         try:
#             await page.wait_for_selector('[jstcache="3"]', timeout=30000)
#         except Exception as error:
#             print("Initial selector not found within the specified timeout")
#             await browser.close()
#             return

#         scrollable = await page.query_selector(
#             "xpath=/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]"
#         )

#         if not scrollable:
#             print("Scrollable element not found.")
#             await browser.close()
#             return

#         end_of_list = False
#         while not end_of_list:
#             # Wrap the scrollable.evaluate in a try-catch block to handle navigation errors
#             try:
#                 await scrollable.evaluate("(node) => node.scrollBy(0, 50000)")
#             except Exception as error:
#                 print("Error while scrolling:", error.message)
#                 break  # Exit the loop in case of an error

#             end_of_list = await page.evaluate(
#                 "() => document.body.innerText.includes(\"You've reached the end of the list\")"
#             )

#         urls = await page.eval_on_selector_all("a", "(links) => links.map(link => link.href).filter(href => href.startsWith('https://www.google.com/maps/place/'))")

#         async def scrape_page_data(url):
#             new_page = await browser.new_page()
#             # Wait for the new page to load or increase timeout if necessary
#             try:
#                 await new_page.goto(url, wait_until='load', timeout=60000)
#                 await new_page.wait_for_selector('[jstcache="3"]', timeout=30000)
#             except Exception as error:
#                 print("Error navigating to", url, ":", error.message)
#                 await new_page.close()
#                 return None  # Return null in case of an error

#             name_element = await new_page.query_selector(
#                 "xpath=/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/h1"
#             )
#             name = await name_element.text_content() if name_element else ""
#             name = f'"{name}"'

#             rating_element = await new_page.query_selector(
#                 "xpath=/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[1]/span[1]"
#             )
#             rating = await rating_element.text_content() if rating_element else ""
#             rating = f'"{rating}"'

#             reviews_element = await new_page.query_selector(
#                 "xpath=/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[2]/span/span"
#             )
#             reviews = await reviews_element.text_content() if reviews_element else ""
#             reviews = reviews.replace("(", "").replace(")", "") if reviews else ""
#             reviews = f'"{reviews}"'

#             category_element = await new_page.query_selector(
#                 "xpath=/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/span/span/button"
#             )
#             category = await category_element.text_content() if category_element else ""
#             category = f'"{category}"'

#             address_element = await new_page.query_selector(
#                 'button[data-tooltip="Copy address"]'
#             )
#             address = await address_element.text_content() if address_element else ""
#             address = f'"{address}"'

#             website_element = await new_page.query_selector(
#                 'a[data-tooltip="Open website"]'
#             ) or await new_page.query_selector('a[data-tooltip="Open menu link"]')
#             website = await website_element.get_attribute("href") if website_element else ""
#             website = f'"{website}"'

#             phone_element = await new_page.query_selector(
#                 'button[data-tooltip="Copy phone number"]'
#             )
#             phone = await phone_element.text_content() if phone_element else ""
#             phone = f'"{phone}"'

#             url = f'"{url}"'

#             await new_page.close()
#             print(name, rating, reviews, category, address, website, phone, url)
#             return { "name": name, "rating": rating, "reviews": reviews, "category": category, "address": address, "website": website, "phone": phone, "url": url }

#         batch_size = 5
#         results = []
#         for i in range(0, len(urls), batch_size):
#             batch_urls = urls[i:i + batch_size]
#             batch_results = await asyncio.gather(*[scrape_page_data(url) for url in batch_urls])
#             results.extend([result for result in batch_results if result is not None])
#             print(f"Batch {i // batch_size + 1} completed.")

#         csv_header = ["Name", "Rating", "Reviews", "Category", "Address", "Website", "Phone", "Url"]
#         csv_rows = [[r["name"].replace('"', '').replace('""' , ''),
#                                     r["rating"].replace('"', '').replace('""' , ''),
#                                     r["reviews"].replace('"', '').replace('""' , ''),
#                                     r["category"].replace('"', '').replace('""' , ''),
#                                     r["address"].replace('"', '').replace('', '').replace('""' , ''),
#                                     r["website"].replace('"', '').replace('""' , ''),
#                                     r["phone"].replace('"', '').replace('""' , ''),
#                                     r["url"].replace('"', '').replace('""' , '')] for r in results]

#         # Read existing data
#         existing_data = []
#         if os.path.exists(name_sheet):
#             with open(name_sheet, mode="r", newline='', encoding='utf-8') as file:
#                 reader = csv.reader(file)
#                 existing_data = list(reader)

#         # If file is empty or doesn't exist, add header
#         if not existing_data:
#             existing_data.append(csv_header)

#         # Append new data
#         existing_data.extend(csv_rows)

#         # Write all data back to CSV
#         with open(name_sheet, mode="w", newline='', encoding='utf-8') as file:
#             writer = csv.writer(file)
#             writer.writerows(existing_data)

#         await browser.close()

#     print("Execution Time: Done")

# asyncio.run(scrape_google_maps_data())



#--------------------------------------------------IF YOU WANT TO RUN WITH MULTIPLE URLS----------------------------------------------------------#



import asyncio
from playwright.async_api import async_playwright
import csv
from asyncio import Semaphore

async def scrape_google_maps_data():
    name_sheet = "hamburg.csv"
    german_capital_cities = [
    "Berlin",
    "Bremen",
    "Hamburg",
    "Dresden",
    "Düsseldorf",
    "Erfurt",
    "Hannover",
    "Kiel",
    "Magdeburg",
    "Mainz",
    "Munich",
    "Potsdam",
    "Saarbrücken",
    "Schwerin",
    "Stuttgart",
    "Wiesbaden"
]
    google_urls = [
        f"https://www.google.com/maps/search/restaurants+in+{city},+Germany/@53.0190216,10.3987354,8z/data=!3m1!4b1?entry=ttu" 
        for city in german_capital_cities
    ]
    
    print("Execution Time:")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        
        all_urls = []
        for google_url in google_urls:
            page = await browser.new_page()
            await page.goto(google_url)

            try:
                await page.wait_for_selector('[jstcache="3"]', timeout=30000)
            except Exception as error:
                print(f"Initial selector not found within the specified timeout for {google_url}")
                await page.close()
                continue

            scrollable = await page.query_selector(
                "xpath=/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]"
            )

            if not scrollable:
                print(f"Scrollable element not found for {google_url}")
                await page.close()
                continue

            end_of_list = False
            while not end_of_list:
                try:
                    await scrollable.evaluate("(node) => node.scrollBy(0, 50000)")
                except Exception as error:
                    print(f"Error while scrolling on {google_url}:", str(error))
                    break

                end_of_list = await page.evaluate(
                    "() => document.body.innerText.includes(\"You've reached the end of the list\")"
                )

            urls = await page.eval_on_selector_all("a", "(links) => links.map(link => link.href).filter(href => href.startsWith('https://www.google.com/maps/place/'))")
            all_urls.extend(urls)
            await page.close()

        last_url_data = {"city": "NA", "country": "NA"}

        async def scrape_page_data(url, semaphore ):
            async with semaphore:
                new_page = await browser.new_page()
                try:
                    await new_page.goto(url, wait_until='load', timeout=60000)
                    await new_page.wait_for_selector('[jstcache="3"]', timeout=30000)
                except Exception as error:
                    print("Error navigating to", url, ":", str(error))
                    await new_page.close()
                    return None

                name_element = await new_page.query_selector(
                    "xpath=/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/h1"
                )
                name = await name_element.text_content() if name_element else "NA"
                name = f'"{name}"'

                rating_element = await new_page.query_selector(
                    "xpath=/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[1]/span[1]"
                )
                rating = await rating_element.text_content() if rating_element else "NA"
                rating = f'"{rating}"'

                reviews_element = await new_page.query_selector(
                    "xpath=/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[2]/span/span"
                )
                reviews = await reviews_element.text_content() if reviews_element else "NA"
                reviews = reviews.replace("(", "").replace(")", "") if reviews else "NA"
                reviews = f'"{reviews}"'

                category_element = await new_page.query_selector(
                    "xpath=/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/span/span/button"
                )
                category = await category_element.text_content() if category_element else "NA"
                category = f'"{category}"'

                address_element = await new_page.query_selector(
                    'button[data-tooltip="Copy address"]'
                )
                address = await address_element.text_content() if address_element else "NA"
                address = f'"{address}"'

                
                City_element = await new_page.query_selector(
                    'button[data-tooltip="Copy plus code"]'
                )
                location = await City_element.text_content() if City_element else "NA"
                try:
                    location_list = location.split(" ")
                except:
                    pass
                # try:
                #     city = f'"{location_list[-2]}"'
                # except:
                #     city = default_city
                # try:
                #     cuntry =f'"{location_list[-1]}"'
                # except:
                #     cuntry =default_cuntry
                city = f'"{location_list[-2]}"' if len(location_list) > 1 else last_url_data["city"]
                country = f'"{location_list[-1]}"' if location_list else last_url_data["country"]

                # Update last URL data
                if city != "NA":
                    last_url_data["city"] = city
                else:
                     city = last_url_data["city"]
                if country != "NA":
                    last_url_data["country"] = country
                else:
                    country = last_url_data["country"]

                website_element = await new_page.query_selector(
                    'a[data-tooltip="Open website"]'
                ) or await new_page.query_selector('a[data-tooltip="Open menu link"]')
                website = await website_element.get_attribute("href") if website_element else "NA"
                website = f'"{website}"'

                phone_element = await new_page.query_selector(
                    'button[data-tooltip="Copy phone number"]'
                )
                phone = await phone_element.text_content() if phone_element else "NA"
                phone = f'"{phone}"'

                url = f'"{url}"'
                await new_page.close()
                print(name, rating, reviews, category, address,city,country,website, phone, url)
                return { "name": name, "rating": rating, "reviews": reviews, "category": category, "address": address,"city": city,"cuntry": country, "website": website, "phone": phone, "url": url }

        # Create a semaphore to limit concurrent tasks
        semaphore = Semaphore(5)  # Adjust this number based on your system's capabilities

        # Create tasks for all URLs
        tasks = [scrape_page_data(url, semaphore) for url in all_urls]

        # Run all tasks concurrently
        results = await asyncio.gather(*tasks)

        # Filter out None results (failed scrapes)
        results = [result for result in results if result is not None]

        csv_header = ["Name", "Rating", "Reviews", "Category", "Address","city","cuntry" ,"Website", "Phone", "Url"]
        csv_rows = [csv_header] + [[r["name"].replace('"', '').replace('"' , ''),
                                    r["rating"].replace('"', '').replace('"' , ''),
                                    r["reviews"].replace('"', '').replace('"' , ''),
                                    r["category"].replace('"', '').replace('"' , ''),
                                    r["address"].replace('"', '').replace('', '').replace('"' , ''),
                                    r["city"].replace("," , '').replace('"', '').replace('""' , ''),
                                    r["cuntry"].replace('"', '').replace('""' , '').replace(',' , ''),
                                    r["website"].replace('"', '').replace('""' , ''),
                                    r["phone"].replace('"', '').replace('""' , ''),
                                    r["url"].replace('"', '').replace('""' , '')] for r in results]
        with open(name_sheet, mode="w", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(csv_rows)

        with open("hamburg.csv", "r", encoding='utf-8') as file:
                reader = csv.reader(file)
                data = [row for row in reader]

        for row in data:
                for i, value in enumerate(row):
                    row[i] = value.replace('"', '').replace('""' , '')
                    if i == 4:
                        row[i] = row[i].replace('', '')
        with open("hamburg.csv", "w", newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(data)



        await browser.close()

    print("Execution Time: Done")

asyncio.run(scrape_google_maps_data())