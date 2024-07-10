from PlotSetup import Colors, Markers

# We organize certain data series into one group, they are revalent and can be plotted into on figure. 
# Same group of data series must have close ylim, same periodicity, etc
PickGDPGroups = {
    'Name': 'GDP',
    'Periodicity': 'Q',
    'PoP': False,    # Whether calculate period on period percentage change    
    'Groups': [
        [
            {'ID': 'T10101', 
            'EnglishName': 'Percent Change From Preceding Period in Real Gross Domestic Product',
            'ChineseName': '实际国内生产总值(GDP)前期变化百分比',
            'Unit': '%',
            'Color': Colors[0],
            'Marker': Markers[0],
            'XLim': None,
            'YLim': None,
            'YAxisPos': 'left',
            'Curve': None}
        ]
    ]
}

