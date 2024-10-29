import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Load the CSV file with latitude and longitude columns
df = pd.read_csv("output.csv")  # Replace with your CSV file name

# Remove rows where 'latitude' or 'longitude' are NaN
df = df.dropna(subset=['latitude', 'longitude'])

# Print to check if coordinates are loaded correctly
print("Coordinates Loaded:")
print(df[['latitude', 'longitude', 'Address']].head())

# Define the initial map center based on average location
avg_lat = df['latitude'].mean()
avg_lon = df['longitude'].mean()

# Create the map centered on the average location
m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)   # Adjusted zoom level for visibility
s = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)   # Adjusted zoom level for visibility
marker_cluster = MarkerCluster().add_to(m)

# Add markers to the map
for _, row in df.iterrows():
    # print(f"Adding marker at: {row['latitude']}, {row['longitude']}")  # Diagnostic print
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=row['Address'],  # Show address in popup
        icon=folium.Icon(color="blue", icon="info-sign")  # Customize marker
    ).add_to(marker_cluster)

# Save the map as an HTML file
m.save("map.html")
