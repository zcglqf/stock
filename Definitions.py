## GroupRequestInfoDataType and RequestInfoDataType are the starting point if need to change 
## infomation header needed to retrieve data
# Data Type for information header with fields needed to retrieve data from BLS, BEA, etc.
RequestInfoDataType = {
    'ID': 'LNS11000000',     # redundent for now, because Group data type has it
    'DataSet': 'NIPA',       # redundent
    'LineNo': 1,
    'EnglishName': 'Civilian Labor Force (K)',
    'ChineseName': '全美劳动人口（千人）',
    'Unit': 'K',
    'Color': 'b',
    'Marker': '+',
    'XLim': None,
    'YLim': None,
    'YAxisPos': 'left',
    'Curve': None}

# Data Type that aims to group relevant data series
GroupRequestInfoDataType = {
    'Name': 'Employment',
    'DataSet': 'NIPA',
    'TableID': 'T10101',
    'Periodicity': 'M',
    'PoP': False,    # Whether calculate period on period percentage change    
    'Groups': [[]]}  # Each group share a plot, groups defined herein share a figure.

class DataRequestInfo(dict):
    def __init__(self, *args, **kwargs):
        self._allowed_fields = RequestInfoDataType.keys()
        super().__init__(*args, **kwargs)
        if self.keys() != self._allowed_fields:
                raise KeyError(f"All fields '{self._allowed_fields}' must be specified.")
        self._locked = True
    
    def __setitem__(self, key, value):
        if self._locked and key not in self._allowed_fields:
            raise KeyError(f"Field '{key}' is not defined.")     
        super().__setitem__(key, value)

    def update(self, *args, **kwargs):
        if self._locked:
            for key in dict(*args, **kwargs):
                if key not in self._allowed_fields:
                    raise KeyError(f"Cannot add new field '{key}' to RestrictedDict")
        super().update(*args, **kwargs)
    
    def unlock(self):
        self._locked = False
    
    def lock(self):
        self._locked = True

class GroupDataRequestInfo(dict):
    def __init__(self, *args, **kwargs):
        self._allowed_fields = GroupRequestInfoDataType.keys()
        super().__init__(*args, **kwargs)
        if self.keys() != self._allowed_fields:
                raise KeyError(f"All fields '{self._allowed_fields}' must be specified.")
        self._locked = True
    
    def __setitem__(self, key, value):
        if self._locked and key not in self._allowed_fields:
            raise KeyError(f"Field '{key}' is not defined.")     
        super().__setitem__(key, value)

    def update(self, *args, **kwargs):
        if self._locked:
            for key in dict(*args, **kwargs):
                if key not in self._allowed_fields:
                    raise KeyError(f"Cannot add new field '{key}' to RestrictedDict")
        super().update(*args, **kwargs)
    
    def unlock(self):
        self._locked = False
    
    def lock(self):
        self._locked = True