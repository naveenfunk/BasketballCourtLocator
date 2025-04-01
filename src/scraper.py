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

            page_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@id='listView']/div/div/p"))
            )
            total_pages = int(page_element[0].text.split()[3])
            current_page = int(page_element[0].text.split()[1])
            park_items = []

            print(f"Page: {current_page}/{total_pages}")
            while current_page <= total_pages:
                print(f"Scrape {current_page}")
                list_items = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#resultToFocus"))
                )

                parks = list_items[0].find_elements(By.CSS_SELECTOR, "div.card.card-shadow")

                # Extract detail page URLs
                
                for park in parks:
                    try:
                        a_element = park.find_element(By.TAG_NAME, "a")
                        detail_link = a_element.get_attribute("href")
                        park_type = a_element.find_element(By.CSS_SELECTOR, "div > span").text.splitlines()[0]
                        park_items.append({'link':detail_link, 'type': park_type})
                    except Exception as e:
                        print(e)
                        pass
            
                print(f"Detail URls found: {len(park_items)}")

                pagination_buttons = self.driver.find_elements(
                    By.XPATH, "//div[@id='listView']/div/div/nav/ul/li"
                )

                if current_page == total_pages:
                    break

                page_index = 0
                while page_index < len(pagination_buttons):
                    if "page-item active" in pagination_buttons[page_index].get_attribute("class"):
                        next_button = pagination_buttons[page_index+1]
                        next_button_anchor = next_button.find_element(By.TAG_NAME, "a")
                        print(f"Next button onclick :{next_button_anchor.get_attribute("id")}")
                        self.driver.execute_script("arguments[0].click();", next_button_anchor)
                
                        WebDriverWait(self.driver, 10).until(
                            EC.text_to_be_present_in_element((By.XPATH, "//div[@id='listView']/div/div/p/span"), f"Page {current_page+1} of {total_pages}")
                        )
                        print(f"Next page activated")
                        break
                    page_index += 1
                current_page += 1
            return park_items
        
        except Exception as e:
            print(f"Error scraping list items: {e}")
            return []
    
    def close(self):
        """
        Close the WebDriver
        """
        if self.driver:
            self.driver.quit()