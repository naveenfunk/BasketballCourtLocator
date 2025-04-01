import folium

class LocationMapper:
    def __init__(self, locations, file_name, map_center=None):
        """
        Initialize map with location data
        
        :param locations: List of location dictionaries
        :param map_center: Optional center coordinates [lat, lon]
        """
        
        self.locations = locations
        self.file_name = file_name
        

        # If no center provided, use average of locations
        if not map_center and locations:
            map_center = [
                sum(loc['latitude'] for loc in locations) / len(locations),
                sum(loc['longitude'] for loc in locations) / len(locations)
            ]

        # Create base map
        self.map = folium.Map(
            location=map_center or [0, 0], 
            zoom_start=10
        )
    
    def add_markers(self):
        """
        Add markers for each location
        """
        
        for location in self.locations:
            
            folium.Marker(
                location=[location['latitude'], location['longitude']],
                popup=f"{location['title']}\n{location['address']}",
                tooltip=location['title']
            ).add_to(self.map)
    
    def save_map(self):
        """
        Save map to HTML file
        
        :param filename: Output filename
        """
        filename = f"{self.file_name}_map.html"
        self.map.save(filename)
        print(f"Map saved to {filename}")