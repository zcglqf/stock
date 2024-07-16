from PlotSetup import Colors, Markers
from Definitions import RequestInfoDataType, GroupRequestInfoDataType, DataRequestInfo, GroupDataRequestInfo
# We organize certain data series into one group, they are revalent and can be plotted into on figure. 
# Same group of data series must have close ylim, same periodicity, etc
PickGDPGroups = GroupDataRequestInfo({
    'Name': 'GDP',
    'DataSet': 'NIPA',
    'TableID': 'T10101',    
    'Periodicity': 'Q',
    'PoP': False,    # Whether calculate period on period percentage change    
    'Groups': [
        [
            DataRequestInfo({
                'ID': 'T10101', 
                'DataSet': 'NIPA',
                'LineNo': 1,
                'EnglishName': 'Percent Change From Preceding Period in Real Gross Domestic Product',
                'ChineseName': '实际国内生产总值(GDP)环比变化百分比',
                'Unit': '%',
                'Color': Colors[0],
                'Marker': Markers[0],
                'XLim': None,
                'YLim': None,
                'YAxisPos': 'left',
                'Curve': None
                }
            )
        ],
        [
            DataRequestInfo({
                'ID': 'T10101', 
                'DataSet': 'NIPA',
                'LineNo': 2,
                'EnglishName': 'Personal consumption expenditures',
                'ChineseName': '个人消费支出',
                'Unit': '%',
                'Color': Colors[0],
                'Marker': Markers[0],
                'XLim': None,
                'YLim': None,
                'YAxisPos': 'left',
                'Curve': None
                }
            ),
            DataRequestInfo({
                'ID': 'T10101', 
                'DataSet': 'NIPA',
                'LineNo': 3,
                'EnglishName': 'Goods',
                'ChineseName': '商品',
                'Unit': '%',
                'Color': Colors[1],
                'Marker': Markers[1],
                'XLim': None,
                'YLim': None,
                'YAxisPos': 'left',
                'Curve': None
                }
            ),
            DataRequestInfo({
                'ID': 'T10101', 
                'DataSet': 'NIPA',
                'LineNo': 6,
                'EnglishName': 'Services',
                'ChineseName': '服务',
                'Unit': '%',
                'Color': Colors[2],
                'Marker': Markers[2],
                'XLim': None,
                'YLim': None,
                'YAxisPos': 'left',
                'Curve': None
                }
            )


        ]
    ]
})



