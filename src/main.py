from src.scraper import WebScraper
from src.data_collector import DataCollector
from src.mapper import LocationMapper

def main():
    # Configuration (replace with your target website)
    BASE_URL = "https://www.aucklandcouncil.govt.nz/parks-recreation/get-outdoors/ball-racquet-disc-activities/Pages/basketball.aspx?area=All"
    
    try:
        # Initialize web scraper
        scraper = WebScraper(BASE_URL)
        
        # Get list of detail page URLs
        park_items = scraper.get_list_items()
        scraper.close()
        
        # Collect location data
        data_collector = DataCollector()
        locations = []
        
        for index, park_item in enumerate(park_items):
            location_data = data_collector.get_location_data(park_item, index)
            if location_data:
                locations.append(location_data)
        
        data_collector.close()
        
        print("Starting to create map")
        # Create and save map
        if locations:
            mapper = LocationMapper(locations, BASE_URL.split("=")[-1])
            mapper.add_markers()
            mapper.save_map()
            print(f"Mapped {len(locations)} locations successfully!")
        else:
            print("No locations found.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()