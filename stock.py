import requests
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
import matplotlib.font_manager as fm
import numpy as np
from PicksEmployment import PickEmploymentGroups, PickProductivityGroups, PickCPIPPIGroups, PickCompensationGroups
from PicksBEAGDP import PickGDPGroups
from collections.abc import Iterable
import beaapi
from IPython.display import display
from PicksEmploymentFun import BLSShowDataSeries
from PicksBEAGDPFun import BEAShowDataSeries

# Ensure that the SimHei font is used for displaying Chinese characters
plt.rcParams['font.sans-serif'] = ['SimHei']  # Set SimHei as default font      # this will change font for the whole plot
plt.rcParams['axes.unicode_minus'] = False    # Ensure minus sign is displayed correctly
# Define fonts
chinese_font = fm.FontProperties(fname='SimHei.ttf', size=6)  # Path to SimHei font file
english_font = fm.FontProperties(fname=fm.findSystemFonts(fontpaths=None, fontext='ttf')[0])  # Use a default system font for English

# BLS API settings
BLS_API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
BLS_API_KEY = "8da8111c50c846ab971494707ae44d4c"
headers = {'Content-type': 'application/json'}

def main():

    BEAShowDataSeries(PickGDPGroups)

    """
    BLSShowDataSeries(PickEmploymentGroups)
    BLSShowDataSeries(PickProductivityGroups)
    BLSShowDataSeries(PickCPIPPIGroups)
    BLSShowDataSeries(PickCPIPPIGroups, pop='YoY')
    BLSShowDataSeries(PickCPIPPIGroups, pop='MoM')
    
    BLSShowDataSeries(PickCompensationGroups)
    """
    
if __name__ == "__main__":
    main()