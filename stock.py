import requests
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
import matplotlib.font_manager as fm
import matplotlib.cm as cm
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import numpy as np

# Try to create a colormap that can mostly seperate the colors
top = mpl.colormaps['Oranges_r'].resampled(128)
middle = mpl.colormaps['Greens'].resampled(128)
bottom = mpl.colormaps['Blues'].resampled(128)

newcolors = np.vstack((top(np.linspace(0, 1, 128)),
                       middle(np.linspace(0, 1, 128)),
                       bottom(np.linspace(0, 1, 128))))
newcmp = ListedColormap(newcolors, name='newRGB')



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

# Example payload for unemployment rate (Series ID: 'LNS14000000')
employmentPicksID = ['LNS11000000',                
                     'LNS12000000',             
                     'LNS13000000',               
                     'LNS14000000',           
                     'CES0000000001',                          
                     'CES0500000002',                                       
                     'CES0500000007', 
                     'CES0500000003',
                     'CES0500000008']

employmentPicksName = ['Civilian Labor Force (K)', 
                       'Civilian Employment (K)', 
                       'Civilian Unemployment (K)', 
                       'Unemployment Rate (%)', #
                       'Total Nonfarm Employment (K)', #
                       'Total Private Average Weekly Hours of All Employee (Hours)', 
                       'Total Private Average Weekly Hours of Prod. and Nonsup. Employees (Hours)',  #
                       'Total Private Average Hourly Earnings of All Employees (USD)',
                       'Total Private Average Hourly Earnings of Prod. and Nonsup. Employees (Hours)'] #

employmentPicksNameChinese = ['全美劳动人口（千人）', 
                              '全美在业人口（千人）',
                              '全美失业人口（千人）',
                              '失业率（％）',
                              '非农就业人口（千人）',
                              '私有部门平均每周工作时间（小时）',
                              '私有部门生产非管理人员平均每周工作时间（小时）',
                              '私有部门平均时薪（美元）',
                              '私有部门生产非管理人员时薪（美元）']

employmentPicksUnit = ['K', 'K', 'K', 'Percentage(%)', 'Head Counts', 'Hours', 'Hours', 'USD', 'USD']

employmentPicksColor = newcmp.resampled(len(employmentPicksID)) # ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w', 'w']

employmentPicksMarker = ['.', 's', 'v', 'p', '*', '+', 'x', 'D', '^', '<', '>', 'k', 'w']

employmentPicksLineWidth = [0.5, 
                            0.5, 
                            0.5, 
                            3, #
                            3, #
                            0.5, 
                            3,  #
                            0.5,
                            3] # 

employmentPicksShareSameAxisWith = [-1, 0, 0, -1, 0, -1, 5, -1, 8]   # y-axis reuse table
employmentPicksYLim = [[150000, 200000],
                       [150000, 200000],
                       [150000, 200000],
                       [0, 0.1],
                       [150000, 200000],
                       [20, 40],
                       [20, 40],
                       [20, 40],
                       [20, 40]
                       ]

dataUnemploymentRate = {
    "seriesid": employmentPicksID,
    "startyear": "2023",
    "endyear": "2024",
    "registrationkey": API_KEY
}

response = requests.post(BLS_API_URL, json=dataUnemploymentRate, headers=headers)
json_data = response.json()

#
# Extract data and plot
axes = [None] * len(json_data['Results']['series'])
curves = [None] * len(json_data['Results']['series'])
fig, ax1 = plt.subplots(figsize=(12, 8))

series_data = json_data['Results']['series']
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
    axes[seriesID] = ax1 if seriesID == 0 else ax1.twinx()
    curves[seriesID], = axes[seriesID].plot(df.index, df['value'], marker=employmentPicksMarker[seriesID], linestyle='-', color=employmentPicksColor(seriesID), label=employmentPicksName[seriesID], linewidth = employmentPicksLineWidth[seriesID])
    axes[seriesID].set_xlabel('Date')
    axes[seriesID].set_ylabel(employmentPicksUnit[seriesID], color=employmentPicksColor(seriesID))
    axes[seriesID].tick_params(axis='y', labelcolor=employmentPicksColor(seriesID))
    
    (N, r) = divmod(seriesID, 2) 
    labelShift = 60 * N if N > 0 else 0
    labelLeftRight = 'left' if r == 0 else 'right'
    # if seriesID > 0:
    #axes[seriesID].spines['right'].set_position(('outward', 60 * (seriesID-1)))
    axes[seriesID].yaxis.set_label_position(labelLeftRight)
    axes[seriesID].spines[labelLeftRight].set_position(('outward', labelShift))
    axes[seriesID].yaxis.tick_left() if r == 0 else axes[seriesID].yaxis.tick_right()
    #handles, labels = axes[seriesID].get_legend_handles_labels()
    #axes[seriesID].legend(loc='upper right', bbox_to_anchor=(1,1)) if handles else None
    axes[seriesID].set_ylim(employmentPicksYLim[seriesID])
    # Resuse y-axis lim and tick of another data
"""     if employmentPicksShareSameAxisWith[seriesID] != -1 :
         axes[seriesID].set_ylim(axes[employmentPicksShareSameAxisWith[seriesID]].get_ylim())
         #axes[seriesID].set_yticks(axes[employmentPicksShareSameAxisWith[seriesID]].get_yticks())
         axes[seriesID].spines[labelLeftRight].set_color(employmentPicksColor(seriesID))
         #axes[seriesID].yaxis.set_ticks_position('none') """


# Add a title and show the plot
plt.title('Employment Data')
fig.legend(employmentPicksNameChinese, loc='upper center',  bbox_to_anchor=(0.5, 0.95), fontsize=6)
fig.tight_layout()  # Adjust layout to prevent overlap
mplcursors.cursor(curves, hover=True) # enable cursor

plt.show()


