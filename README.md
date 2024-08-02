# Email-Scraper

## Overview
The Email-Scraper is a Python-based tool designed to extract Name, Rating, Reviews, Category, Address,city,country ,Website, Phone, Url , email addresses from Google Maps listings. This tool can be useful for collecting contact information for businesses or other entities listed on Google Maps.
#### Note:- Email's extract after running Gemailfinder.py 

## Features
- **Scrapes Email Addresses:** Extracts email addresses from Google Maps search results.
- **CSV Output:** Saves the scraped data into a CSV file for easy access and analysis.
- **Configurable:** Allows users to specify search parameters and locations.

## Requirements
To use this tool, you need to have the following installed:
- Python 3.x
- Required Python libraries listed in `requirements.txt`

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/0xDonatHack/Email-Scraper.git
    ```
2. Navigate to the project directory:
    ```sh
    cd Email-Scraper
    ```
3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Open `GoogleMap.py` and configure the search parameters as needed.
2. Run the script:
    ```sh
    python GoogleMap.py & python Gemailfinder.py
    ```
3. The scraped emails will be saved in `output.csv`.

## File Structure
- `GoogleMap.py`: Main script to scraping Detail like : Name, Rating, Reviews, Category, Address,city,country ,Website, Phone, Url.
- `requirements.txt`: Lists the dependencies needed for the project.
- `output.csv`: File where the scraped emails are stored.

## License
This project is licensed under the MIT License.

## Contact
For any inquiries or issues, please open an issue in the repository.