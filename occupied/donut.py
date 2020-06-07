from palettable.colorbrewer.qualitative import Pastel1_7
import matplotlib.pyplot as plt
import pandas as pd
import glob


def prepare_donut_ingredients(data_path, column=None):
    data = pd.read_csv(data_path, index_col = 0).fillna(0)
    # contains the sector's name as key and count
    sectors = {}
    
    # Group sectors names
    for index, row in data.iterrows():
        sectors[row.SECTOR] = sectors.get(row.SECTOR, 0) + row[column] if column is not None else 1

    return list(sectors.keys()), list(sectors.values())


def create_donut(types, weighting, weighted_on, year):
    # create data
    names=types
    size=weighting
    
    # Create a circle for the center of the plot
    my_circle=plt.Circle( (0,0), 0.7, color='white')

    plt.pie(size, labels=names, colors=Pastel1_7.hex_colors)
    p=plt.gcf()
    p.gca().add_artist(my_circle)
    plt.title("Sectors based on {} counted in {}".format(weighted_on, year))
    # Save the donut (can use plt.show() to display graph instead)
    plt.savefig("../plots/Sectors-donut-{}-{}.pdf".format(weighted_on, year))
    
    # Clear all configurations
    plt.clf()


def donut_make_plots():
    paths = glob.glob("../data/shelter-*.csv")
    for path in paths:
        types, weighting = prepare_donut_ingredients(path)
        if len(types):
            create_donut(types, weighting, "shelters", path[-8:-4])
        types, weighting = prepare_donut_ingredients(path, "CAPACITY")
        if len(types):
            create_donut(types, weighting, "capacity", path[-8:-4])


if __name__ == "__main__":
    donut_make_plots()