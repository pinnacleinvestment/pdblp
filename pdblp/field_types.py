# Field type mapping for pdblp dummy data generation
# Types: 'float', 'int', 'str', 'date'

FIELD_TYPES = {
    # bdh/ref fields
    'PX_LAST': 'float',
    'PX_OPEN': 'float',
    'TURNOVER': 'float',
    'NET_INCOME': 'float',
    'EQY_INIT_PO_DT': 'date',
    'EQY_INIT_PO_SH_PX': 'float',
    'ID_ISIN': 'str',
    # Add more fields as needed
}

BULKREF_FIELD_NAME_TYPES = {
    'INDEX_MEMBERS_SHARES': {
        'Index Member': 'str',
        'Number of Shares': 'float',
    },
    'INDX_MWEIGHT_PX': {
        'Index Member': 'str',
        'Percent Weight': 'float',
        'Actual Weight': 'float',
        'Current Price': 'float',
    },
    'EQY_DVD_ADJUST_FACT': {
        'Adjustment Date': 'date',
        'Adjustment Factor': 'float',
        'Adjustment Factor Operator Type': 'float',
        'Adjustment Factor Flag': 'float',
    },
    'ERN_ANN_DT_AND_PER': {
        'Earnings Announcement Date': 'date',
        'Earnings Year and Period': 'str',
    },
    # Add more fields and their name mappings as needed
}
