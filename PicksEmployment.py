from PlotSetup import Colors, Markers

# We organize certain data series into one group, they are revalent and can be plotted into on figure. 
# Same group of data series must have close ylim, same periodicity, etc
PickEmploymentGroups = {
    'Name': 'Employment',
    'Periodicity': 'M',
    'PoP': False,    # Whether calculate period on period percentage change    
    'Groups': [
        [
            {'ID': 'LNS11000000', 
            'EnglishName': 'Civilian Labor Force (K)',
            'ChineseName': '全美劳动人口（千人）',
            'Unit': 'K',
            'Color': Colors[0],
            'Marker': Markers[0],
            'XLim': None,
            'YLim': [150000, 200000],
            'YAxisPos': 'left',
            'Curve': None},

            {'ID': 'LNS12000000', 
            'EnglishName': 'Civilian Employment (K)',
            'ChineseName': '全美在业人口（千人）',
            'Unit': 'K',
            'Color': Colors[1],
            'Marker': Markers[1],
            'XLim': None,
            'YLim': [150000, 200000],
            'YAxisPos': 'left',
            'Curve': None},      

            {'ID': 'CES0000000001', 
            'EnglishName': 'Total Nonfarm Employment (K)',
            'ChineseName': '非农就业人口（千人）',
            'Unit': 'K',
            'Color': Colors[4],
            'Marker': Markers[4],
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
            'Color': Colors[2],
            'Marker': Markers[2],
            'XLim': None,
            'YLim': [150000, 200000],
            'YAxisPos': 'left',
            'Curve': None},                

            {'ID': 'LNS14000000', 
            'EnglishName': 'Unemployment Rate (%)',
            'ChineseName': '失业率（％）',
            'Unit': '%',
            'Color': Colors[3],
            'Marker': Markers[3],
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
            'Color': Colors[0],
            'Marker': Markers[0],
            'XLim': None,
            'YLim': [20, 40],
            'YAxisPos': 'left',
            'Curve': None},

            {'ID': 'CES0500000007', 
            'EnglishName': 'Total Private Average Weekly Hours of Prod. and Nonsup. Employees (Hours)',
            'ChineseName': '私有部门生产非管理人员平均每周工作时间（小时）',
            'Unit': 'Hours',
            'Color': Colors[1],
            'Marker': Markers[1],
            'XLim': None,
            'YLim': [20, 40],
            'YAxisPos': 'left',
            'Curve': None},

            {'ID': 'CES0500000003', 
            'EnglishName': 'Total Private Average Hourly Earnings of All Employees (USD)',
            'ChineseName': '私有部门平均时薪（美元）',
            'Unit': 'USD',
            'Color': Colors[2],
            'Marker': Markers[2],
            'XLim': None,
            'YLim': [20, 40],
            'YAxisPos': 'right',
            'Curve': None},

            {'ID': 'CES0500000008', 
            'EnglishName': 'Total Private Average Hourly Earnings of Prod. and Nonsup. Employees (USD)',
            'ChineseName': '私有部门生产非管理人员时薪（美元）',
            'Unit': 'USD',
            'Color': Colors[3],
            'Marker': Markers[3],
            'XLim': None,
            'YLim': [20, 40],
            'YAxisPos': 'right',
            'Curve': None}
        ]
    ]
}

PickProductivityGroups = {
    'Name': 'Employment',
    'Periodicity': 'Q',
    'PoP': False,    # Whether calculate period on period percentage change    
    'Groups': [ 
        # Group 1
        [
            {'ID': 'PRS84006092', 
            'EnglishName': 'Business - Labor Productivity (Output per Hour), percent change from previous quarter',
            'ChineseName': '商业 - 劳动生产率（每小时产出），季度环比',
            'Unit': 'quarter over quarter (%)',
            'Color': 'r',
            'Marker': Markers[0],
            'XLim': None,
            'YLim': None,
            'YAxisPos': 'left',
            'Curve': None},

            {'ID': 'PRS84006112', 
            'EnglishName': 'Business - Unit Labor Costs, percent change from previous quarter',
            'ChineseName': '商业 - 单位劳动成本，季度环比',
            'Unit': 'quarter over quarter (%)',
            'Color': 'r',
            'Marker': Markers[1],
            'XLim': None,
            'YLim': None,
            'YAxisPos': 'left',
            'Curve': None},      

            {'ID': 'PRS84006152', 
            'EnglishName': 'Business - Real Hourly Compensation, percent change from previous quarter',
            'ChineseName': '商业 - 实际每小时报酬，季度环比',
            'Unit': 'quarter over quarter (%)',
            'Color': 'r',
            'Marker': Markers[2],
            'XLim': None,
            'YLim': None,
            'YAxisPos': 'left',
            'Curve': None},

            {'ID': 'PRS85006092', 
            'EnglishName': 'Nonfarm Business - Labor Productivity (Output per Hour), percent change from previous quarter',
            'ChineseName': '非农商业 - 劳动生产率（每小时产出），季度环比',
            'Unit': 'quarter over quarter (%)',
            'Color': 'g',
            'Marker': Markers[3],
            'XLim': None,
            'YLim': None,
            'YAxisPos': 'left',
            'Curve': None},                

            {'ID': 'PRS85006112', 
            'EnglishName': 'Nonfarm Business - Unit Labor Costs, percent change from previous quarter',
            'ChineseName': '非农商业 - 单位劳动成本，季度环比',
            'Unit': 'quarter over quarter (%)',
            'Color': 'g',
            'Marker': Markers[4],
            'XLim': None,
            'YLim': None,
            'YAxisPos': 'left',
            'Curve': None},  

            {'ID': 'PRS85006152', 
            'EnglishName': 'Nonfarm Business - Real Hourly Compensation, percent change from previous quarter',
            'ChineseName': '非农商业 - 实际每小时报酬，季度环比',
            'Unit': 'quarter over quarter (%)',
            'Color': 'g',
            'Marker': Markers[5],
            'XLim': None,
            'YLim': None,
            'YAxisPos': 'left',
            'Curve': None},

            {'ID': 'PRS30006092', 
            'EnglishName': 'Manufacturing - Labor Productivity (Output per Hour), percent change from previous quarter',
            'ChineseName': '制造业 - 劳动生产率（每小时产出），季度环比',
            'Unit': 'quarter over quarter (%)',
            'Color': 'b',
            'Marker': Markers[6],
            'XLim': None,
            'YLim': None,
            'YAxisPos': 'left',
            'Curve': None},

            {'ID': 'PRS30006112', 
            'EnglishName': 'Manufacturing - Unit Labor Costs, percent change from previous quarter',
            'ChineseName': '制造业 - 单位劳动成本，季度环比',
            'Unit': 'quarter over quarter (%)',
            'Color': 'b',
            'Marker': Markers[7],
            'XLim': None,
            'YLim': None,
            'YAxisPos': 'left',
            'Curve': None},

            {'ID': 'PRS30006152', 
            'EnglishName': 'Manufacturing - Real Hourly Compensation, percent change from previous quarter',
            'ChineseName': '制造业 - 实际每小时报酬，季度环比',
            'Unit': 'quarter over quarter (%)',
            'Color': 'b',
            'Marker': Markers[8],
            'XLim': None,
            'YLim': None,
            'YAxisPos': 'left',
            'Curve': None}
        ]
    ]
}

PickCPIPPIGroups = {
    'Name': 'CPI, PPI Price Index',
    'Periodicity': 'M',
    'PoP': False,    # Whether calculate period on period percentage change
    'Groups': [ 
        # Group 1: CPI
        [
            {'ID': 'CUUR0000SA0', 
            'EnglishName': 'CPI for All Urban Consumers (CPI-U) 1982-84=100 ',
            'ChineseName': '城市消费者的消费者价格指数',
            'Unit': 'None',
            'Color': Colors[0],
            'Marker': Markers[0],
            'XLim': None,
            'YLim': None,
            'YAxisPos': 'left',
            'Curve': None},

            {'ID': 'CWUR0000SA0', 
            'EnglishName': 'CPI for Urban Wage Earners and Clerical Workers (CPI-W) 1982-84=100',
            'ChineseName': '城市工资收入者和文职人员的消费者价格指数',
            'Unit': 'None',
            'Color': Colors[1],
            'Marker': Markers[1],
            'XLim': None,
            'YLim': None,
            'YAxisPos': 'left',
            'Curve': None},      

            {'ID': 'CUUR0000SA0L1E', 
            'EnglishName': 'CPI-U/Less Food and Energy',
            'ChineseName': '城市消费者价格指数不含食品和能源',
            'Unit': 'None',
            'Color': Colors[2],
            'Marker': Markers[2],
            'XLim': None,
            'YLim': None,
            'YAxisPos': 'left',
            'Curve': None},

            {'ID': 'CWUR0000SA0L1E', 
            'EnglishName': 'CPI-W/Less Food and Energy',
            'ChineseName': '城市工资收入者和文职人员消费者价格指数不含食品和能源',
            'Unit': 'None',
            'Color': Colors[3],
            'Marker': Markers[3],
            'XLim': None,
            'YLim': None,
            'YAxisPos': 'left',
            'Curve': None},                
        ],

        # Group 2: PPI
        [
            {'ID': 'WPUFD4', 
            'EnglishName': 'PPI Final Demand',
            'ChineseName': '最终需求生产者价格指数', # 到手价
            'Unit': 'None',
            'Color': Colors[0],
            'Marker': Markers[0],
            'XLim': None,
            'YLim': None,
            'YAxisPos': 'left',
            'Curve': None},  

            {'ID': 'WPUFD49104', 
            'EnglishName': 'PPI Final Demand less foods and energy',
            'ChineseName': '最终需求生产者价格指数不含食品和能源',
            'Unit': 'None',
            'Color': Colors[1],
            'Marker': Markers[1],
            'XLim': None,
            'YLim': None,
            'YAxisPos': 'left',
            'Curve': None},

            {'ID': 'WPUFD49207', 
            'EnglishName': 'PPI Finished Goods 1982=100',
            'ChineseName': '最终产品生产者价格指数', # 成品价
            'Unit': 'None',
            'Color': Colors[3],
            'Marker': Markers[3],
            'XLim': None,
            'YLim': None,
            'YAxisPos': 'left',
            'Curve': None},

            {'ID': 'EIUIR', 
            'EnglishName': 'Imports - All Commodities',
            'ChineseName': '进口 - 所有商品',
            'Unit': 'None',
            'Color': Colors[4],
            'Marker': Markers[4],
            'XLim': None,
            'YLim': None,
            'YAxisPos': 'left',
            'Curve': None},

            {'ID': 'EIUIQ', 
            'EnglishName': 'Exports - All Commodities',
            'ChineseName': '出口 - 所有商品',
            'Unit': 'None',
            'Color': Colors[5],
            'Marker': Markers[8],
            'XLim': None,
            'YLim': None,
            'YAxisPos': 'left',
            'Curve': None}
        ]
    ]
}


PickCompensationGroups = {
    'Name': 'Compensation',
    'Periodicity': 'Q',
    'PoP': False,    # Whether calculate period on period percentage change
    'Groups': [ 
        # Group 1: CPI
        [
            {'ID': 'CIU1010000000000A', 
            'EnglishName': 'Employment Cost Index (ECI) Civilian',
            'ChineseName': '就业成本指数 (ECI) - 民用',
            'Unit': 'None',
            'Color': Colors[0],
            'Marker': Markers[0],
            'XLim': None,
            'YLim': None,
            'YAxisPos': 'left',
            'Curve': None},

            {'ID': 'CIU2010000000000A', 
            'EnglishName': 'ECI Private',
            'ChineseName': '就业成本指数 (ECI) - 私营部门',
            'Unit': 'None',
            'Color': Colors[1],
            'Marker': Markers[1],
            'XLim': None,
            'YLim': None,
            'YAxisPos': 'left',
            'Curve': None},      

            {'ID': 'CIU2020000000000A', 
            'EnglishName': 'ECI Private Wage and Salaries',
            'ChineseName': '就业成本指数 (ECI) - 私营部门工资和薪金',
            'Unit': 'None',
            'Color': Colors[2],
            'Marker': Markers[2],
            'XLim': None,
            'YLim': None,
            'YAxisPos': 'left',
            'Curve': None}
        ]
    ]
}
