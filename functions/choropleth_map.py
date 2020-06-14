import numpy as np
import pandas as pd
import json
import folium
import csv
import glob

path_to_data = "./data"
postal_to_neighbourhood = {}
neighbourhoods = []

def prepare_map_data(data_path, year):
    global postal_to_neighbourhood, path_to_data, neighbourhoods
    # Need to calculate average density per year and later group up the locations
    plot_data = pd.read_csv(data_path, index_col = 0).fillna(0)
    occupied = {}

    # Group data and swap in shelter data
    for index, row in plot_data.iterrows():
        neighbourhood = postal_to_neighbourhood.get(row.SHELTER_POSTAL_CODE, False)
        if not neighbourhood:
            continue
        occupied[neighbourhood] = occupied.get(neighbourhood, 0) + row.OCCUPANCY

    with open("{}/neighbourhood-average-{}.csv".format(path_to_data, year), "w") as f:
        neighbourhood_writer = csv.writer(f, delimiter=',')
        neighbourhood_writer.writerow(['location', 'density'])
        for neighbourhood in neighbourhoods:
            neighbourhood_writer.writerow([neighbourhood, occupied.get(neighbourhood, 0)/365])
    

def create_choropleth_map(neighbourhood_geo, year):
    global path_to_data
    # Get neighbourhood density data
    with open("{}/neighbourhood-average-{}.csv".format(path_to_data, year)) as f:
        neighbourhood_data = pd.read_csv(f)

    # Initialize the map:
    m = folium.Map(location=[43.68, -79.4], zoom_start=11)
    
    # Add the color for the chloropleth:
    m.choropleth(
    geo_data=neighbourhood_geo,
    name='Toronto Average shelter dependency',
    data=neighbourhood_data,
    columns=['location', 'density'],
    key_on='feature.properties.location',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Daily Shelter Dependency'
    )
    folium.LayerControl().add_to(m)

    # Save to html
    m.save('./plots/#Neighbourhood_Shetlers-{}.html'.format(year))

def generate_choropleth_maps():
    global postal_to_neighbourhood, path_to_data, neighbourhoods
    # Load postal and neighbourhood data
    locations_data = pd.read_csv("{}/locations.csv".format(path_to_data))
    for inidex, row in locations_data.iterrows():
        postal_to_neighbourhood[row.postal_code] = row.neighbourhood
        
    # CleanNeighbourhood()
    
    # Get neighbourhood geo data
    with open("{}/Neighbourhoods.geojson".format(path_to_data)) as f:
        neighbourhood_geo = json.load(f)    
    
    for neighbourhood in neighbourhood_geo["features"]:
        neighbourhoods.append(neighbourhood["properties"]["location"])

    paths = glob.glob("{}/shelter-*.csv".format(path_to_data))
    for path in paths:
        prepare_map_data(path, path[-8:-4])
        # Call Create Choropleth Map
        create_choropleth_map(neighbourhood_geo, path[-8:-4])
        
def clean_neighbourhood():
    # Create location column for each shelter
    global path_to_data
    neighbourhood_file = "{}/Neighbourhoods.geojson".format(path_to_data)
    with open(neighbourhood_file) as f:
        neighbourhood_data = json.load(f)
        
    for neighbourhood in neighbourhood_data["features"]:
        excess_info_index = neighbourhood["properties"]["AREA_NAME"].find("(")
        neighbourhood["properties"]["location"] = neighbourhood["properties"]["AREA_NAME"][:excess_info_index-1]

    with open(neighbourhood_file, 'w') as f:
        f.write(json.dumps(neighbourhood_data))

if __name__ == "__main__":
   generate_choropleth_maps()