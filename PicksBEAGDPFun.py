from collections.abc import Iterable
import matplotlib.pyplot as plt
import requests
import pandas as pd
import numpy as np
import mplcursors
import beaapi
from IPython.display import display


BEA_API_KEY = '23DF8493-2808-4318-9234-FFA677113171'
BEA_API_URL = 'https://apps.bea.gov/api/data/'

def BEAShowDataSeries(picksGroups : dict, 
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
    elif pop == 'QoQ':    
        supertitle = picksGroups['Name'] + ' (Quarter over Quarter)'
    elif pop == 'MoM':
        supertitle = picksGroups['Name'] + ' (Month over Month)'
    else:
        return ValueError(f"Unknown Period over Period option.")    

    startYear = startYear if pop == 'None' else str(int(startYear) - 1)
    years = ','.join(str(year) for year in range(int(startYear), int(endYear)+1))
    
    for groupidx, group in enumerate(picksGroups['Groups']):

        # Retrive data series IDs from current group
        for series in group:
            seriesID = series['ID']
            dataSet  = series['DataSet']
            bea_tbl = beaapi.get_data(BEA_API_KEY, datasetname=dataSet, TableName=seriesID, Frequency=picksGroups['Periodicity'], Year=years)
            df = pd.DataFrame(bea_tbl)
            df = df[df['LineNumber']==series['LineNo']]
            # load and show data series in current group
            # Convert date format and sort by date
            if picksGroups['Periodicity'] == 'Q':
                df['xtick'] = df['TimePeriod'].str[-4:] # for quarter
                df['month'] = (df['TimePeriod'].str[-1].astype(int) - 1) * 3 + 1  # fpr quarter
            elif picksGroups['Periodicity'] == 'M':
                df['xtick'] = df['TimePeriod'].str[-5:]   # for month
                df['month'] = df['TimePeriod'].str[-2:].astype(int)   # for month
            else:
                return ValueError(f"Unknown Periodicity symbol {picksGroups['Periodicity']}")
            df['year'] = df['TimePeriod'].str[0:4]
            df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))
            df = df.sort_values('date')
            df['value'] = df['DataValue'].astype(float)
            if pop == 'None':
                pass
            elif pop == 'YoY':
                df['value'] = df['value'].pct_change(periods=12) * 100
                group[seriesID]['Unit'] = '%'
                df = df[df['year'] > int(startYear)]
            elif pop == 'MoM':
                df['value'] = df['value'].pct_change() * 100
                group[seriesID]['Unit'] = '%'
                df = df[df['year'] > int(startYear)]
            else:
                return ValueError(f"Unknown Period over Period opption.")   

            df.set_index('date', inplace=True)
            label = series['EnglishName'] 
            # Plot
            if series['YAxisPos'] == 'left':
                series['Curve'], = axes[groupidx].plot(df.index, df['value'], marker=series['Marker'], linestyle='-', color=series['Color'], label=label)
                axes[groupidx].set_xlabel('Date')
                axes[groupidx].set_ylabel(series['Unit'])
                axes[groupidx].yaxis.set_label_position(series['YAxisPos'])
                axes[groupidx].yaxis.tick_left()
                axes[groupidx].set_xticks(df.index)
                axes[groupidx].set_xticklabels(df['xtick'])
            else:
                series['Curve'], = twinaxes[groupidx].plot(df.index, df['value'], marker=series['Marker'], linestyle='-', color=series['Color'], label=label)
                twinaxes[groupidx].set_xlabel('Date')
                twinaxes[groupidx].set_ylabel(series['Unit'])
                twinaxes[groupidx].yaxis.set_label_position(series['YAxisPos'])
                twinaxes[groupidx].yaxis.tick_right()

        curves = [series['Curve'] for series in group]
        legends = [series['ChineseName'] if language == 'CHN' else series['EnglishName'] for series in group]
        axes[groupidx].legend(curves, legends, loc='upper left')
        mplcursors.cursor(curves, hover=True) # enable cursor

    # Add a title and show the plot
    fig.suptitle(supertitle)

    fig.tight_layout()  # Adjust layout to prevent overlap

    plt.show()
