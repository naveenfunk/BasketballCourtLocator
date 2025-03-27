import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebScraper:
    def __init__(self, base_url):
        """
        Initialize the web scraper with a base URL
        
        :param base_url: The main page URL to scrape list items from
        """
        self.base_url = base_url
        self.driver = self._setup_driver()
    
    def _setup_driver(self):
        """
        Setup headless Chrome WebDriver
        
        :return: Configured WebDriver instance
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    
    def get_list_items(self):
        """
        Scrape list items from the base URL
        
        :return: List of detail page URLs
        """
        try:
            self.driver.get(self.base_url)
            
            # Wait for list items to load (customize selector)
            list_items = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#resultToFocus"))
            )
                    
            parks = list_items[0].find_elements(By.CSS_SELECTOR, "div.card.card-shadow")

            # Extract detail page URLs
            detail_urls = []
            for park in parks:
                try:
                    detail_link = park.find_element(By.TAG_NAME, "a").get_attribute("href")
                    detail_urls.append(detail_link)
                except Exception:
                    pass

        
            print(f"Detail URls found: {len(detail_urls)}")
            return detail_urls
        
        except Exception as e:
            print(f"Error scraping list items: {e}")
            return []
    
    def close(self):
        """
        Close the WebDriver
        """
        if self.driver:
            self.driver.quit()