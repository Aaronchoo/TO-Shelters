from palettable.colorbrewer.qualitative import Pastel1_7
import matplotlib.pyplot as plt
import pandas as pd
import glob


def prepare_donut_ingredients(data_path):
    data = pd.read_csv(data_path, index_col = 0).fillna(0)
    # contains the sector's name as key and count
    sectors_shelter_count, sectors_occupancy, sectors_capacity = {}, {}, {}
    
    # Group sectors names
    for index, row in data.iterrows():
        sectors_shelter_count[row.SECTOR] = sectors_shelter_count.get(row.SECTOR, 0) + 1
        sectors_occupancy[row.SECTOR] = sectors_occupancy.get(row.SECTOR, 0) + row["OCCUPANCY"]
        sectors_capacity[row.SECTOR] = sectors_capacity.get(row.SECTOR, 0) + row["CAPACITY"]

    sector_types = list(sectors_shelter_count.keys())
    sector_shetler_count = list(sectors_shelter_count.values())
    sector_occupancy_sum = list(sectors_occupancy.values())
    sector_capacity_sum = list(sectors_capacity.values())

    return sector_types, sector_shetler_count, sector_occupancy_sum, sector_capacity_sum


def create_donut(types, weighting, weighted_on, year):
    # create data
    names=types
    size=weighting
    
    # Create a circle for the center of the plot
    my_circle=plt.Circle( (0,0), 0.7, color='white')

    plt.pie(size, labels=names, colors=Pastel1_7.hex_colors)
    p=plt.gcf()
    p.gca().add_artist(my_circle)
    plt.title("Daily shelter sectors based on total {} counted in {}".format(weighted_on, year))
    # Save the donut (can use plt.show() to display graph instead)
    plt.savefig("./plots/Sectors-donut-{}-{}.pdf".format(weighted_on, year))
    
    # Clear all configurations
    plt.clf()


def donut_make_plots():
    paths = glob.glob("./data/shelter-*.csv")
    for path in paths:
        types, shelter_count, sum_occupancy, sum_capacity = prepare_donut_ingredients(path)
        if len(shelter_count):
            create_donut(types, shelter_count, "shelters", path[-8:-4])
        if len(sum_occupancy):
            create_donut(types, sum_occupancy, "occupancy", path[-8:-4])
        if len(sum_capacity):
            create_donut(types, sum_capacity, "capacity", path[-8:-4])


if __name__ == "__main__":
    donut_make_plots()