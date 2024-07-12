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

BEA_API_KEY = '23DF8493-2808-4318-9234-FFA677113171'
BEA_API_URL = 'https://apps.bea.gov/api/data/'

def BLSShowDataSeries(picksGroups : list, 
                   startYear:str='2023', 
                   endYear:str='2024', 
                   language:str='CHN',   # language for legend, label is always english
                   pop:str='None') :     # period over period

    fig, axes = plt.subplots(len(picksGroups['Groups']), 1, figsize=(12, 8))
    axes = [axes] if not isinstance(axes, Iterable) else axes
    twinaxes = [ax.twinx() for ax in axes] 

    if pop == 'None':
        supertitle = picksGroups['Name']
    elif pop == 'YoY':
        supertitle = picksGroups['Name'] + ' (Year over Year)'
    elif pop == 'MoM':
        supertitle = picksGroups['Name'] + ' (Month over Month)'
    else:
        return ValueError(f"Unknown Period over Period opption.")    

    for groupidx, group in enumerate(picksGroups['Groups']):
        # Retrive data series IDs from current group
        seriesIDs = [series['ID'] for series in group]

        dataRequestInfo = {
            "seriesid": seriesIDs,
            "startyear": startYear if pop == 'None' else str(int(startYear) - 1), # if need to perform period over period then start from an earlier year.
            "endyear": endYear,
            "registrationkey": BLS_API_KEY
        }

        response = requests.post(BLS_API_URL, json=dataRequestInfo, headers=headers)
        json_data = response.json()
        print(f"Data request status: { json_data['status'] }, {response.text}")
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
            if pop == 'None':
                pass
            elif pop == 'YoY':
                df['value'] = df['value'].pct_change(periods=12) * 100
                group[seriesID]['Unit'] = '%'
                df = df[df['year'] > int(dataRequestInfo['startyear'])]
            elif pop == 'MoM':
                df['value'] = df['value'].pct_change() * 100
                group[seriesID]['Unit'] = '%'
                df = df[df['year'] > int(dataRequestInfo['startyear'])]
            else:
                return ValueError(f"Unknown Period over Period opption.")            

            df.set_index('date', inplace=True)

            label = group[seriesID]['EnglishName'] 
            # Plot
            if group[seriesID]['YAxisPos'] == 'left':
                group[seriesID]['Curve'], = axes[groupidx].plot(df.index, df['value'], marker=group[seriesID]['Marker'], linestyle='-', color=group[seriesID]['Color'], label=label)
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
                group[seriesID]['Curve'], = twinaxes[groupidx].plot(df.index, df['value'], marker=group[seriesID]['Marker'], linestyle='-', color=group[seriesID]['Color'], label=label)
                twinaxes[groupidx].set_xlabel('Date')
                twinaxes[groupidx].set_ylabel(group[seriesID]['Unit'])
                twinaxes[groupidx].yaxis.set_label_position(group[seriesID]['YAxisPos'])
                twinaxes[groupidx].yaxis.tick_right()
                # twinaxes[groupidx].set_ylim(group[seriesID]['YLim'])    
                ylimrightmin = np.min(df['value']) if ylimrightmin > np.min(df['value']) else ylimrightmin
                ylimrightmax = np.max(df['value']) if ylimrightmax < np.min(df['value']) else ylimrightmax            

        # Combine Legend Handles and Labels from Both Axes, legend text comes from the label property of each plot. 

        """ lines_1, labels_1 = axes[groupidx].get_legend_handles_labels()
        lines_2, labels_2 = twinaxes[groupidx].get_legend_handles_labels()
        lines = lines_1 + lines_2
        labels = labels_1 + labels_2
        axes[groupidx].legend(lines, labels, loc='upper left') """

        curves = [series['Curve'] for series in group]
        legends = [series['ChineseName'] if language == 'CHN' else series['EnglishName'] for series in group]
        axes[groupidx].legend(curves, legends, loc='upper left')
        mplcursors.cursor(curves, hover=True) # enable cursor

    # Add a title and show the plot
    fig.suptitle(supertitle)

    fig.tight_layout()  # Adjust layout to prevent overlap

    plt.show()

def BEAShowDataSeries(picksGroups : list, 
                   startYear:str='2023', 
                   endYear:str='2024', 
                   language:str='CHN', 
                   pop:str='None') :     # period over period
    
    fig, axes = plt.subplots(len(picksGroups['Groups']), 1, figsize=(12, 8))
    axes = [axes] if not isinstance(axes, Iterable) else axes
    twinaxes = [ax.twinx() for ax in axes] 

    if pop == 'None':
        supertitle = picksGroups['Name']
    elif pop == 'YoY':
        supertitle = picksGroups['Name'] + ' (Year over Year)'
    elif pop == 'MoM':
        supertitle = picksGroups['Name'] + ' (Month over Month)'
    else:
        return ValueError(f"Unknown Period over Period opption.")    

    for groupidx, group in enumerate(picksGroups['Groups']):
        # Retrive data series IDs from current group
        seriesIDs = [series['ID'] for series in group]

        dataRequestInfo = {
            'UserID': BEA_API_KEY,
            'method': 'GetData',
            'dtatsetname': 'NIPA',
            'TableName': 'T10101',
            'Frequency': picksGroups['Periodicity'],
            'Year': 'ALL',
            'ResultFormat': 'json'
        }

        response = requests.post(BEA_API_URL, params=dataRequestInfo)
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            # Convert the JSON data to a pandas DataFrame
            df = pd.DataFrame(data['BEAAPI']['Results']['Data'])
            print(df)
        else:
            print(f"Error: {response.status_code}")

"""         json_data = response.json()
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
            if pop == 'None':
                pass
            elif pop == 'YoY':
                df['value'] = df['value'].pct_change(periods=12) * 100
                group[seriesID]['Unit'] = '%'
                df = df[df['year'] > int(dataRequestInfo['startyear'])]
            elif pop == 'MoM':
                df['value'] = df['value'].pct_change() * 100
                group[seriesID]['Unit'] = '%'
                df = df[df['year'] > int(dataRequestInfo['startyear'])]
            else:
                return ValueError(f"Unknown Period over Period opption.")            

            df.set_index('date', inplace=True)

            label=group[seriesID]['ChineseName'] if language == 'CHN' else group[seriesID]['EnglishName'] 
            # Plot
            if group[seriesID]['YAxisPos'] == 'left':
                group[seriesID]['Curve'], = axes[groupidx].plot(df.index, df['value'], marker=group[seriesID]['Marker'], linestyle='-', color=group[seriesID]['Color'], label=label)
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
                group[seriesID]['Curve'], = twinaxes[groupidx].plot(df.index, df['value'], marker=group[seriesID]['Marker'], linestyle='-', color=group[seriesID]['Color'], label=label)
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
        mplcursors.cursor(curves, hover=True) # enable cursor """

"""     # Add a title and show the plot
    fig.suptitle(supertitle)

    fig.tight_layout()  # Adjust layout to prevent overlap

    plt.show() """


def main():

    """ list_of_sets = beaapi.get_data_set_list(BEA_API_KEY)
    display(list_of_sets)
    list_of_params = beaapi.get_parameter_list(BEA_API_KEY, 'NIPA')
    display(list_of_params) """
    # search_data = beaapi.search_metadata('Gross domestic', BEA_API_KEY) useful code in this comment block:
    """     bea_tbl = beaapi.get_data(BEA_API_KEY, datasetname='NIPA', TableName='T10101', Frequency='Q', Year='2021,2022,2023,2024')
 
    df = pd.DataFrame(bea_tbl)
    df = df[df['LineNumber']==1]
    # Convert date format and sort by date
    df['xtick'] = df['TimePeriod'].str[-4:]
    df['year'] = df['TimePeriod'].str[0:4]
    df['month'] = (df['TimePeriod'].str[-1].astype(int) - 1) * 3 + 1
    df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))
    df = df.sort_values('date')
    df['value'] = df['DataValue'].astype(float)
    df.set_index('date', inplace=True)

    fig, axes = plt.subplots(figsize=(12, 8))
    surve, = axes.plot(df.index, df['value'], marker='*', linestyle='-', color='b', label='GDP')
    axes.set_xticks(df.index)
    axes.set_xticklabels(df['xtick'])
    plt.show() """


    # BEAShowDataSeries(PickGDPGroups)
    BLSShowDataSeries(PickEmploymentGroups)
    BLSShowDataSeries(PickProductivityGroups)
    BLSShowDataSeries(PickCPIPPIGroups)
    BLSShowDataSeries(PickCPIPPIGroups, pop='YoY')
    BLSShowDataSeries(PickCPIPPIGroups, pop='MoM')
    
    BLSShowDataSeries(PickCompensationGroups)

    
if __name__ == "__main__":
    main()