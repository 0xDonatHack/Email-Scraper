# import pandas as pd
# import folium
# from folium.plugins import MarkerCluster

# # Load the CSV file with latitude and longitude columns
# df = pd.read_csv("output.csv")  # Replace with your CSV file name

# # Remove rows where 'latitude' or 'longitude' are NaN
# df = df.dropna(subset=['latitude', 'longitude'])

# # Print to check if coordinates are loaded correctly
# print("Coordinates Loaded:")
# print(df[['latitude', 'longitude', 'Address']].head())

# # Define the initial map center based on average location
# avg_lat = df['latitude'].mean()
# avg_lon = df['longitude'].mean()

# # Create the map centered on the average location
# m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12, max_bounds=True)   # Adjusted zoom level for visibility
# # s = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)   # Adjusted zoom level for visibility
# marker_cluster = MarkerCluster().add_to(m)

# # Add markers to the map
# for _, row in df.iterrows():
#     # print(f"Adding marker at: {row['latitude']}, {row['longitude']}")  # Diagnostic print
#     folium.Marker(
#         location=[row['latitude'], row['longitude']],
#         popup=row['Address'],  # Show address in popup
#         icon=folium.Icon(color="blue", icon="info-sign"),  # Customize marker
#         max_bounds=True,
#         min_lat=-85, max_lat=85, min_lon=-180, max_lon=180
#     ).add_to(marker_cluster)

# # Save the map as an HTML file
# m.save("templates/map.html")


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

# Select a random row from the DataFrame
random_row = df.sample(n=1)

# Get the latitude and longitude from the random row
avg_lat = random_row['latitude'].values[0]
avg_lon = random_row['longitude'].values[0]

# Create the map centered on the random location
m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12, max_bounds=True)
marker_cluster = MarkerCluster().add_to(m)

# Add markers to the map
for _, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=row['Address'],  # Show address in popup
        icon=folium.Icon(color="blue", icon="info-sign"),  # Customize marker
        max_bounds=True,
        min_lat=-85, max_lat=85, min_lon=-180, max_lon=180
    ).add_to(marker_cluster)

# Save the map as an HTML file
m.save("templates/map.html")