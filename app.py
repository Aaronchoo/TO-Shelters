import sys

sys.path.append('/functions')

from functions.choropleth_map import generate_choropleth_maps
from functions.donut import donut_make_plots
from functions.stacked_population import generate_stack_plots

def generate_plots():
    for argv in sys.argv:
        if 'choropleth' == argv:
            generate_choropleth_maps()
        if 'donut' == argv:
            donut_make_plots()
        if 'stacked_population' == argv:
            generate_stack_plots()

if __name__ == '__main__':
    generate_plots()