from geopy.geocoders import Nominatim
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from src.location_extractor import LocationExtractor as le

class DataCollector:
    def __init__(self):
        """
        Initialize data collector with Nominatim geocoder
        """
        self.geolocator = Nominatim(user_agent="location_mapper_app")
        self.driver = self._setup_driver()
    
    def _setup_driver(self):
        """
        Setup headless Chrome WebDriver
        
        :return: Configured WebDriver instance
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    
    def get_location_data(self, park_item, index):
        """
        Fetch location data from a detail page
        
        :param park_item: URL and Type of the park
        :return: Dictionary with location details
        """
        try:
            self.driver.get(park_item['link'])
            
            # Wait and extract title (customize selector)
            title = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#generalHeading > h1"))
            ).text
            
            # Wait and extract address (customize selector)
            address_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#lblLocation"))
            )
            
            address = address_element.text
            
            show_map_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#showMap"))
            )

            # Geocode the address
            latitude, longitude = le.extract_coordinates(show_map_link.get_attribute("href"))
            
            map_location = {
                'title': title,
                'address': f"{park_item['type']}-{address}",
                'latitude': float(latitude),
                'longitude': float(longitude)
            }
            print(f"{index+1} Location extracted: {map_location}")
            return map_location
        
        except Exception as e:
            print(f"Error collecting data from {park_item}: {e}")
            return None
    
    def close(self):
        """
        Close the WebDriver
        """
        if self.driver:
            self.driver.quit()