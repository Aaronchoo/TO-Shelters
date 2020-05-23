import glob
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def PreparePlotData(dataPath):
    data = pd.read_csv(dataPath, index_col = 0).fillna(0)
    occupied, capacity = {}, {}
    # Group data based on occupancy date
    for index, row in data.iterrows():
        occupied[row.OCCUPANCY_DATE] = occupied.get(row.OCCUPANCY_DATE, 0) + row.OCCUPANCY
        capacity[row.OCCUPANCY_DATE] = capacity.get(row.OCCUPANCY_DATE, 0) + row.CAPACITY
    
    # Sort the dates to be in proper order
    days = sorted(data.OCCUPANCY_DATE.unique())
    return [occupied[day] for day in days], [capacity[day] - occupied[day] for day in days], [day[4:10] for day in days]

def CreatedStackPlot(occupied, capacity, labels, year):
    # Axis data and removes the year from label
    x = [label[5:] for label in labels] 
    y = [occupiedCreatedStackPlot, capacity]

    # Set up graph data
    pal = sns.color_palette("Set1")
    plt.stackplot(x,y, labels=['Occupied', 'Avaliable'], colors=pal, alpha=0.7)
    plt.legend(loc='lower right')
    plt.margins(0,0)
    plt.title('Shelter Occupied vs Avaliable')

    # Save the graph (can use plt.show() to display graph instead)
    plt.savefig("Shelter-{}.pdf".format(year))
    
    # Clear all configurations
    plt.clf()


def GenerateStackPlots():
    paths = glob.glob("../data/shelter-*.csv")
    for path in paths:
        occupied, capacity, labels = PreparePlotData(path)
        if len(occupied):
            CreatedStackPlot(occupied, capacity, labels, path[-8:-4])
    
if __name__ == "__main__":
   GenerateStackPlots()