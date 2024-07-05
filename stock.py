import requests
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
import matplotlib.font_manager as fm
import numpy as np




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

employmentPicksColor = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w', 'w'] # newcmp.resampled(len(employmentPicksID)) # 

employmentPicksMarker = ['.', 's', 'v', 'p', '*', '+', 'x', 'D', '^', '<', '>', 'k', 'w']


# We organize certain data series into one group, they are revalent and can be plotted into on figure. 
employmentPicksGroups = [ 
    # Group 1
    [
        {'ID': 'LNS11000000', 
        'EnglishName': 'Civilian Labor Force (K)',
        'ChineseName': '全美劳动人口（千人）',
        'Unit': 'K',
        'Color': employmentPicksColor[0],
        'Marker': employmentPicksMarker[0],
        'XLim': None,
        'YLim': [150000, 200000],
        'YAxisPos': 'left',
        'Curve': None},

        {'ID': 'LNS12000000', 
        'EnglishName': 'Civilian Employment (K)',
        'ChineseName': '全美在业人口（千人）',
        'Unit': 'K',
        'Color': employmentPicksColor[1],
        'Marker': employmentPicksMarker[1],
        'XLim': None,
        'YLim': [150000, 200000],
        'YAxisPos': 'left',
        'Curve': None},      

        {'ID': 'CES0000000001', 
        'EnglishName': 'Total Nonfarm Employment (K)',
        'ChineseName': '非农就业人口（千人）',
        'Unit': 'K',
        'Color': employmentPicksColor[4],
        'Marker': employmentPicksMarker[4],
        'XLim': None,
        'YLim': [150000, 200000],
        'YAxisPos': 'left',
        'Curve': None}
    ],

    # Group 2
    [
        {'ID': 'LNS13000000', 
        'EnglishName': 'Civilian Unemployment (K)',
        'ChineseName': '全美失业人口（千人）',
        'Unit': 'K',
        'Color': employmentPicksColor[2],
        'Marker': employmentPicksMarker[2],
        'XLim': None,
        'YLim': [150000, 200000],
        'YAxisPos': 'left',
        'Curve': None},                

        {'ID': 'LNS14000000', 
        'EnglishName': 'Unemployment Rate (%)',
        'ChineseName': '失业率（％）',
        'Unit': '%',
        'Color': employmentPicksColor[3],
        'Marker': employmentPicksMarker[3],
        'XLim': None,
        'YLim': [3, 10],
        'YAxisPos': 'right',
        'Curve': None},  
    ],

    # Group 3
    [
        {'ID': 'CES0500000002', 
         'EnglishName': 'Total Private Average Weekly Hours of All Employee (Hours)',
         'ChineseName': '私有部门平均每周工作时间（小时）',
         'Unit': 'Hours',
         'Color': employmentPicksColor[0],
         'Marker': employmentPicksMarker[0],
         'XLim': None,
         'YLim': [20, 40],
         'YAxisPos': 'left',
         'Curve': None},

        {'ID': 'CES0500000007', 
         'EnglishName': 'Total Private Average Weekly Hours of Prod. and Nonsup. Employees (Hours)',
         'ChineseName': '私有部门生产非管理人员平均每周工作时间（小时）',
         'Unit': 'Hours',
         'Color': employmentPicksColor[1],
         'Marker': employmentPicksMarker[1],
         'XLim': None,
         'YLim': [20, 40],
         'YAxisPos': 'left',
         'Curve': None},

        {'ID': 'CES0500000003', 
         'EnglishName': 'Total Private Average Hourly Earnings of All Employees (USD)',
         'ChineseName': '私有部门平均时薪（美元）',
         'Unit': 'USD',
         'Color': employmentPicksColor[2],
         'Marker': employmentPicksMarker[2],
         'XLim': None,
         'YLim': [20, 40],
         'YAxisPos': 'right',
         'Curve': None},

        {'ID': 'CES0500000008', 
         'EnglishName': 'Total Private Average Hourly Earnings of Prod. and Nonsup. Employees (USD)',
         'ChineseName': '私有部门生产非管理人员时薪（美元）',
         'Unit': 'USD',
         'Color': employmentPicksColor[3],
         'Marker': employmentPicksMarker[3],
         'XLim': None,
         'YLim': [20, 40],
         'YAxisPos': 'right',
         'Curve': None}
    ]
]

totalNrDataSeries = sum([len(group) for group in employmentPicksGroups])
# curves = [None] * totalNrDataSeries
fig, axes = plt.subplots(len(employmentPicksGroups), 1, figsize=(12, 8))
twinaxes = [ax.twinx() for ax in axes] 

for groupidx, group in enumerate(employmentPicksGroups):
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
        df['year'] = df['year'].astype(int)
        df['period'] = df['period'].apply(lambda x: x.replace('M', ''))
        df['month'] = df['period'].astype(int)
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
fig.suptitle('Employment Data')

fig.tight_layout()  # Adjust layout to prevent overlap

plt.show()
