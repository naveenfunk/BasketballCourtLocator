import re

class LocationExtractor:

    def extract_coordinates(url):
        """
        Extract latitude and longitude from a Google Maps URL.

        Args:
            url (str): The Google Maps URL.

        Returns:
            tuple: A tuple containing latitude and longitude as strings, or (None, None) if not found.
        """
        try:
            # Use regex to search for 'destination=latitude,longitude' in the URL
            match = re.search(r"destination=(-?\d+\.\d+)%2C(-?\d+\.\d+)", url)
            if match:
                latitude = match.group(1)
                longitude = match.group(2)
                return latitude, longitude
            else:
                return None, None
        except Exception as e:
            print(f"Error processing URL: {e}")
            return None, None