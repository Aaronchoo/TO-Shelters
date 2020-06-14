import glob
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def prepare_plot_data(data_path):
    data = pd.read_csv(data_path, index_col = 0).fillna(0)
    occupied, capacity = {}, {}
    # Group data based on occupancy date
    for index, row in data.iterrows():
        occupied[row.OCCUPANCY_DATE] = occupied.get(row.OCCUPANCY_DATE, 0) + row.OCCUPANCY
        capacity[row.OCCUPANCY_DATE] = capacity.get(row.OCCUPANCY_DATE, 0) + row.CAPACITY
    
    # Sort the dates to be in proper order
    days = sorted(data.OCCUPANCY_DATE.unique())
    return [occupied[day] for day in days], [capacity[day] - occupied[day] for day in days], [day[4:10] for day in days]

def create_stack_plot(occupied, capacity, labels, year):
    # Axis data and removes the year from label
    x = labels
    y = [occupied, capacity]

    # Set up graph data
    pal = sns.color_palette("Set1")
    plt.stackplot(x,y, labels=['Occupied', 'Avaliable'], colors=pal, alpha=0.7)
    plt.legend(loc='lower right')
    plt.margins(0,0)
    plt.title('Shelter Occupied vs Avaliable')

    # Save the graph (can use plt.show() to display graph instead)
    plt.savefig("./plots/Shelter-{}.pdf".format(year))
    
    # Clear all configurations
    plt.clf()


def generate_stack_plots():
    paths = glob.glob("./data/shelter-*.csv")
    for path in paths:
        occupied, capacity, labels = prepare_plot_data(path)
        if len(occupied):
            create_stack_plot(occupied, capacity, labels, path[-8:-4])
    
if __name__ == "__main__":
   generate_stack_plots()