# This code gives illustration density on the map.

"""
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import cartopy.feature as cfeature
import matplotlib.colors as mcolors

# Load the dataset
file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/filtered_holy_bible_illustrations.tsv'
data = pd.read_csv(file_path, delimiter='\t')

# Ensure relevant columns are present
required_columns = ['ecco_id', 'pages_ecco_id_proportion', 'publication_place']
for col in required_columns:
    if col not in data.columns:
        raise ValueError(f"The column '{col}' is not found in the dataset.")

# Group by ecco_id to get unique ecco_id rows with the maximum pages_ecco_id_proportion
ecco_grouped = data.groupby('ecco_id').agg({
    'pages_ecco_id_proportion': 'max', 
    'publication_place': 'first'
}).reset_index()

# Define predefined coordinates for the cities
coordinates = {
    'Bath': (51.3758, -2.3599),
    'Belfast': (54.5973, -5.9301),
    'Birmingham': (52.4862, -1.8904),
    'Cambridge': (52.2053, 0.1218),
    'Dublin': (53.3498, -6.2603),
    'Edinburgh': (55.9533, -3.1883),
    'Glasgow': (55.8642, -4.2518),
    'Helston': (50.1038, -5.2760),
    'London': (51.5074, -0.1278),
    'Newcastle': (54.9783, -1.6174),
    'Oxford': (51.7520, -1.2577)
}

# Add latitude and longitude to the DataFrame
ecco_grouped['latitude'] = ecco_grouped['publication_place'].map(lambda x: coordinates.get(x, (None, None))[0])
ecco_grouped['longitude'] = ecco_grouped['publication_place'].map(lambda x: coordinates.get(x, (None, None))[1])

# Filter out places with missing coordinates
ecco_grouped = ecco_grouped.dropna(subset=['latitude', 'longitude'])

# Convert the DataFrame to a GeoDataFrame
geometry = [Point(xy) for xy in zip(ecco_grouped['longitude'], ecco_grouped['latitude'])]
gdf = gpd.GeoDataFrame(ecco_grouped, geometry=geometry)

# Load high-resolution UK map from Natural Earth
shapefile_path = shpreader.natural_earth(resolution='10m', category='cultural', name='admin_0_countries')
uk = gpd.read_file(shapefile_path)
uk = uk[(uk['NAME'] == 'United Kingdom') | (uk['NAME'] == 'Ireland')]

# Define a colormap
colormap = plt.cm.get_cmap('tab20', len(coordinates))

# Create a color dictionary for the cities
color_dict = {city: colormap(i) for i, city in enumerate(coordinates.keys())}

# Plotting
fig, ax = plt.subplots(figsize=(12, 18), subplot_kw={'projection': ccrs.Mercator()})
ax.set_extent([-10, 2, 49, 61], crs=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black', facecolor='whitesmoke')
ax.add_feature(cfeature.BORDERS, zorder=0)
ax.coastlines(resolution='10m')

# Plot points with different colors for each city
for place in gdf['publication_place'].unique():
    subset = gdf[gdf['publication_place'] == place]
    subset.plot(
        ax=ax, markersize=(subset['pages_ecco_id_proportion'] + 1) * 10, 
        color=color_dict[place], alpha=0.6, edgecolor='black', 
        label=place, transform=ccrs.PlateCarree()
    )

# Add legend with fixed marker size
handles, labels = ax.get_legend_handles_labels()
legend_markers = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_dict[label], markersize=10) for label in labels]
plt.legend(legend_markers, labels, title="Publication Place", title_fontsize='13', fontsize='11')

plt.title('Density of Illustration Proportion in Bible by Publication Place', fontsize=15, fontweight='bold')
plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.show()

# Calculate mean and median values for different publication places
place_stats = ecco_grouped.groupby('publication_place').agg({
    'pages_ecco_id_proportion': ['mean', 'median'],
    'ecco_id': 'count'
}).reset_index()

# Rename columns for clarity
place_stats.columns = ['publication_place', 'mean_pages_ecco_id_proportion', 'median_pages_ecco_id_proportion', 'ecco_id_count']

# Print the results
print(place_stats)
"""


# I forgot its function but I used the code below to make a new table for analysis.
"""
import pandas as pd

# Load the dataset
file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/filtered_holy_bible_illustrations.tsv'
data = pd.read_csv(file_path, delimiter='\t')

# Ensure relevant columns are present
required_columns = ['ecco_id', 'pages_ecco_id_proportion']
for col in required_columns:
    if col not in data.columns:
        raise ValueError(f"The column '{col}' is not found in the dataset.")

# Group by ecco_id to get unique ecco_id rows with the maximum pages_ecco_id_proportion
ecco_grouped = data.loc[data.groupby('ecco_id')['pages_ecco_id_proportion'].idxmax()].reset_index(drop=True)

# Save the new DataFrame to a new TSV file
output_file_path = '/Users/enesyilandiloglu/Documents/GitHub/Kakule_1/ffiltered_holy_bible_illustrations_aggregated.tsv'
ecco_grouped.to_csv(output_file_path, sep='\t', index=False)

print(f"The new aggregated TSV file has been saved to {output_file_path}")
"""