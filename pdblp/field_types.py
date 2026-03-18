import random

# ─── Helpers ─────────────────────────────────────────────────────────────────

def _dummy_equity_ticker(i: int) -> str:
    """
    Generate unique Excel-style ticker names:
    0 → A, 1 → B, ..., 25 → Z,
    26 → AA, 27 → AB, ..., 51 → AZ,
    52 → BA, ... and so on without limit.
    """
    result = ""
    n = i + 1
    while n > 0:
        n -= 1
        result = chr(ord('A') + n % 26) + result
        n //= 26
    return f"{result} US EQUITY"


def _dummy_isin(i: int) -> str:
    """
    Generate a valid-format 12-char ISIN: US + 10 digits.
    e.g. i=0 → US0000000000, i=1 → US0000000001
    """
    return f"US{i:010d}"


# ─── ref() / bdh() ───────────────────────────────────────────────────────────

# Type mapping for scalar fields
FIELD_TYPES = {
    'PX_LAST':            'float',
    'PX_OPEN':            'float',
    'PX_HIGH':            'float',
    'PX_LOW':             'float',
    'PX_VOLUME':          'float',
    'TURNOVER':           'float',
    'PX_BID':             'float',
    'PX_ASK':             'float',
    'NET_INCOME':         'float',
    'EQY_INIT_PO_DT':     'date',
    'EQY_INIT_PO_SH_PX':  'float',
    'ID_ISIN':            'str',
    # Add more fields as needed
}

# Override dummy value per field where default f"dummy_{fld}" is wrong format.
# Signature: dummy_fn(ticker: str, i: int) -> value
FIELD_DUMMY_VALUES = {
    'ID_ISIN': lambda ticker, i: _dummy_isin(i),
}


# ─── bulkref() ───────────────────────────────────────────────────────────────

# How many dummy members to return per index in bulkref dummy mode
BULKREF_DUMMY_NUM_MEMBERS = 10

# Format: { field: { name: (dtype, dummy_fn(position: int)) } }
# dtype  : 'float' | 'int' | 'date' | 'str'
# dummy_fn: called with the member position index (0-based), must return
#           a value that matches the real Bloomberg format for that name.
BULKREF_FIELD_NAME_TYPES = {
    'INDEX_MEMBERS_SHARES': {
        'Index Member':     ('str',   lambda i: _dummy_equity_ticker(i)),
        'Number of Shares': ('float', lambda i: round(random.uniform(100e6, 5000e6), 6)),
    },
    'INDX_MWEIGHT_PX': {
        'Index Member':   ('str',   lambda i: _dummy_equity_ticker(i)),
        'Percent Weight': ('float', lambda i: round(random.uniform(0.01, 10.0), 6)),
        'Actual Weight':  ('float', lambda i: round(random.uniform(0.01, 10.0), 6)),
        'Current Price':  ('float', lambda i: round(random.uniform(10.0, 800.0), 6)),
    },
    'EQY_DVD_ADJUST_FACT': {
        'Adjustment Date':                 ('date',  lambda i: '2024-01-01'),
        'Adjustment Factor':               ('float', lambda i: round(random.uniform(0.5, 2.0), 6)),
        'Adjustment Factor Operator Type': ('float', lambda i: round(random.uniform(1.0, 5.0), 6)),
        'Adjustment Factor Flag':          ('float', lambda i: round(random.uniform(0.0, 1.0), 6)),
    },
    'ERN_ANN_DT_AND_PER': {
        'Earnings Announcement Date': ('date', lambda i: f'2024-{(i % 4) * 3 + 1:02d}-15'),
        'Earnings Year and Period':   ('str',  lambda i: f'{2024 - i // 4}Q{(i % 4) + 1}'),
    },
    # Add more fields as needed
}
