import requests
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
import matplotlib.font_manager as fm
import numpy as np
from PicksEmployment import PickEmploymentGroups, PickProductivityGroups
from collections.abc import Iterable

# Ensure that the SimHei font is used for displaying Chinese characters
plt.rcParams['font.sans-serif'] = ['SimHei']  # Set SimHei as default font      # this will change font for the whole plot
plt.rcParams['axes.unicode_minus'] = False    # Ensure minus sign is displayed correctly
# Define fonts
chinese_font = fm.FontProperties(fname='SimHei.ttf', size=6)  # Path to SimHei font file
english_font = fm.FontProperties(fname=fm.findSystemFonts(fontpaths=None, fontext='ttf')[0])  # Use a default system font for English

# BLS API settings
BLS_API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
API_KEY = "8da8111c50c846ab971494707ae44d4c"
headers = {'Content-type': 'application/json'}

def ShowDataSeries(picksGroups : list) :

    fig, axes = plt.subplots(len(picksGroups['Groups']), 1, figsize=(12, 8))
    axes = [axes] if not isinstance(axes, Iterable) else axes
    twinaxes = [ax.twinx() for ax in axes] 

    for groupidx, group in enumerate(picksGroups['Groups']):
        # Retrive data series IDs from current group
        seriesIDs = [series['ID'] for series in group]

        dataRequestInfo = {
            "seriesid": seriesIDs,
            "startyear": "2023",
            "endyear": "2024",
            "registrationkey": API_KEY
        }

        response = requests.post(BLS_API_URL, json=dataRequestInfo, headers=headers)
        json_data = response.json()
        series_data = json_data['Results']['series']

        # load and show data series in current group
        ylimleftmin, ylimleftmax = float('inf'), -float('inf')
        ylimrightmin, ylimrightmax = float('inf'), -float('inf')
        for seriesID in range(len(series_data)):
            df = pd.DataFrame(series_data[seriesID]['data'])
            # Convert date format and sort by date
            df['xtick'] = df['year'].str[-2:] + df['period']
            df['year'] = df['year'].astype(int)
            df['period'] = df['period'].apply(lambda x: x.replace(picksGroups['Periodicity'], '')) # Periodicity is 'M', 'Q', etc
            if picksGroups['Periodicity'] == 'Q':
                df['month'] = (df['period'].astype(int) - 1) * 3 + 1    # convert quarter to month
            elif picksGroups['Periodicity'] == 'M':
                df['month'] = df['period'].astype(int)
            else:
                return ValueError(f"Unknown Periodicity symbol {picksGroups['Periodicity']}")
            
            df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))
            df = df.sort_values('date')
            # Convert value to float and set date as index
            df['value'] = df['value'].astype(float)
            df.set_index('date', inplace=True)

            # Plot
            if group[seriesID]['YAxisPos'] == 'left':
                group[seriesID]['Curve'], = axes[groupidx].plot(df.index, df['value'], marker=group[seriesID]['Marker'], linestyle='-', color=group[seriesID]['Color'], label=group[seriesID]['EnglishName'])
                axes[groupidx].set_xlabel('Date')
                axes[groupidx].set_ylabel(group[seriesID]['Unit'])
                axes[groupidx].yaxis.set_label_position(group[seriesID]['YAxisPos'])
                axes[groupidx].yaxis.tick_left()
                axes[groupidx].set_xticks(df.index)
                axes[groupidx].set_xticklabels(df['xtick'])
                #axes[groupidx].set_ylim(group[seriesID]['YLim'])   
                ylimleftmin = np.min(df['value']) if ylimleftmin > np.min(df['value']) else ylimleftmin
                ylimleftmax = np.max(df['value']) if ylimleftmax < np.min(df['value']) else ylimleftmax
            else:
                group[seriesID]['Curve'], = twinaxes[groupidx].plot(df.index, df['value'], marker=group[seriesID]['Marker'], linestyle='-', color=group[seriesID]['Color'], label=group[seriesID]['EnglishName'])
                twinaxes[groupidx].set_xlabel('Date')
                twinaxes[groupidx].set_ylabel(group[seriesID]['Unit'])
                twinaxes[groupidx].yaxis.set_label_position(group[seriesID]['YAxisPos'])
                twinaxes[groupidx].yaxis.tick_right()
                # twinaxes[groupidx].set_ylim(group[seriesID]['YLim'])    
                ylimrightmin = np.min(df['value']) if ylimrightmin > np.min(df['value']) else ylimrightmin
                ylimrightmax = np.max(df['value']) if ylimrightmax < np.min(df['value']) else ylimrightmax
            

        # Combine Legend Handles and Labels from Both Axes, legend text comes from the label property of each plot. 
        lines_1, labels_1 = axes[groupidx].get_legend_handles_labels()
        lines_2, labels_2 = twinaxes[groupidx].get_legend_handles_labels()
        lines = lines_1 + lines_2
        labels = labels_1 + labels_2
        axes[groupidx].legend(lines, labels, loc='upper left')

        curves = [series['Curve'] for series in group]
        mplcursors.cursor(curves, hover=True) # enable cursor

    # Add a title and show the plot
    fig.suptitle(picksGroups['Name'])

    fig.tight_layout()  # Adjust layout to prevent overlap

    plt.show()


def main():
    ShowDataSeries(PickProductivityGroups)
    ShowDataSeries(PickEmploymentGroups)
    pass
    
if __name__ == "__main__":
    main()