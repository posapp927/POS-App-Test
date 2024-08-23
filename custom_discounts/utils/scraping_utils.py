# custom_discounts/utils/scraping_utils.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
import time
import re
import os
import hashlib
import pickle
from collections import defaultdict
from datetime import datetime, timedelta
from custom_discounts.utils.logging_utils import setup_logger

# Setup logger for the module
logger = setup_logger('custom_discounts.utils.scraping_utils', 'scraping.log')

class ScrapingUtils:
    def __init__(self, base_url, headers=None, cache_dir='cache', cache_expiry_hours=24):
        self.base_url = base_url
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.cache_dir = cache_dir
        self.cache_expiry_hours = cache_expiry_hours
        os.makedirs(cache_dir, exist_ok=True)

    def fetch_page(self, url, use_cache=True):
        """Fetch a page with optional caching."""
        logger.info(f"Fetching URL: {url}")
        cache_path = self._get_cache_path(url)

        if use_cache and self._is_cache_valid(cache_path):
            logger.info(f"Loading page from cache: {cache_path}")
            with open(cache_path, 'rb') as f:
                return pickle.load(f)

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Cache the response
            with open(cache_path, 'wb') as f:
                pickle.dump(soup, f)

            return soup
        except requests.RequestException as e:
            logger.error(f"Error fetching URL: {url} - {e}")
            return None

    def parse_html(self, soup, selector):
        """Parse HTML using BeautifulSoup with the given CSS selector."""
        logger.info(f"Parsing HTML with selector: {selector}")
        elements = soup.select(selector)
        return elements

    def find_links(self, soup, base_url=None):
        """Extract and return all links from the given BeautifulSoup object."""
        base_url = base_url or self.base_url
        logger.info(f"Finding links in the page with base URL: {base_url}")
        links = set()
        for link in soup.find_all('a', href=True):
            full_url = urljoin(base_url, link['href'])
            if self._is_valid_url(full_url):
                links.add(full_url)
        return links

    def extract_data(self, soup, selectors):
        """Extract data based on a dictionary of CSS selectors."""
        logger.info(f"Extracting data with selectors: {selectors}")
        data = defaultdict(list)
        for key, selector in selectors.items():
            elements = soup.select(selector)
            data[key] = [element.get_text(strip=True) for element in elements]
        return dict(data)

    def handle_dynamic_content(self, url, render_wait=5):
        """Handle dynamic content using Selenium."""
        logger.info(f"Handling dynamic content for URL: {url}")
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By

        options = Options()
        options.headless = True
        service = Service(executable_path='/path/to/chromedriver')  # Update with the correct path
        driver = webdriver.Chrome(service=service, options=options)
        
        try:
            driver.get(url)
            time.sleep(render_wait)  # Wait for dynamic content to load
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            return soup
        except Exception as e:
            logger.error(f"Error handling dynamic content for URL: {url} - {e}")
            return None
        finally:
            driver.quit()

    def _get_cache_path(self, url):
        """Generate a file path for caching based on the URL."""
        url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        return os.path.join(self.cache_dir, f'{url_hash}.pkl')

    def _is_cache_valid(self, cache_path):
        """Check if the cached file is still valid based on the expiry."""
        if not os.path.exists(cache_path):
            return False
        cache_time = datetime.fromtimestamp(os.path.getmtime(cache_path))
        return datetime.now() - cache_time < timedelta(hours=self.cache_expiry_hours)

    def _is_valid_url(self, url):
        """Check if the URL is valid and should be included in scraping."""
        valid = bool(re.match(r'^https?://', url))
        logger.debug(f"URL {url} is {'valid' if valid else 'invalid'} for scraping.")
        return valid

    def respect_robots_txt(self):
        """Parse and respect the robots.txt rules for the site."""
        robots_url = urljoin(self.base_url, '/robots.txt')
        try:
            response = self.session.get(robots_url)
            if response.status_code == 200:
                logger.info(f"Fetched robots.txt from {robots_url}")
                lines = response.text.splitlines()
                for line in lines:
                    if line.strip().lower().startswith('disallow'):
                        # Implement disallow rules as needed
                        pass
            else:
                logger.warning(f"No robots.txt found at {robots_url}")
        except requests.RequestException as e:
            logger.error(f"Error fetching robots.txt: {e}")

    def save_data_to_file(self, data, file_path):
        """Save extracted data to a file."""
        logger.info(f"Saving data to {file_path}")
        with open(file_path, 'w', encoding='utf-8') as f:
            for key, values in data.items():
                f.write(f"{key}:\n")
                for value in values:
                    f.write(f"  - {value}\n")

    def encrypt_sensitive_data(self, data, key):
        """Encrypt sensitive data."""
        from cryptography.fernet import Fernet
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data.encode('utf-8'))
        logger.debug("Data encrypted successfully.")
        return encrypted_data

    def decrypt_sensitive_data(self, encrypted_data, key):
        """Decrypt sensitive data."""
        from cryptography.fernet import Fernet
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data).decode('utf-8')
        logger.debug("Data decrypted successfully.")
        return decrypted_data

    def anonymize_data(self, data):
        """Anonymize sensitive data for compliance purposes."""
        logger.debug("Anonymizing data.")
        anonymized_data = re.sub(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', '***@***.***', data)
        return anonymized_data

    def close_session(self):
        """Close the requests session."""
        logger.info("Closing session.")
        self.session.close()
