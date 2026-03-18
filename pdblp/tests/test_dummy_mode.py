import pytest
import pandas as pd
import re

from pdblp import pdblp


@pytest.fixture(scope="module")
def dummy_con():
    return pdblp.BCon(debug=False, port=8194, timeout=5000, dummy=True).start()


# ─────────────────────────────────────────────────────────────
# SCALAR (ref / bdh) TESTS
# ─────────────────────────────────────────────────────────────

def test_dummy_ref_isin_format(dummy_con):
    df = dummy_con.ref(["AAPL US Equity", "MSFT US Equity"], ["ID_ISIN"])

    assert len(df) == 2

    for val in df["value"]:
        assert isinstance(val, str)
        assert re.match(r"^US\d{10}$", val), f"Invalid ISIN format: {val}"


def test_dummy_bdh_structure(dummy_con):
    df = dummy_con.bdh(
        tickers=["AAPL US Equity", "MSFT US Equity"],
        flds=["PX_LAST", "PX_OPEN"],
        start_date="20240101",
        end_date="20240103",
        longdata=True
    )

    # basic structure check
    assert set(df.columns) == {"date", "ticker", "field", "value"}
    assert len(df) > 0


def test_dummy_scalar_value_types(dummy_con):
    df = dummy_con.ref(
        ["AAPL US Equity"],
        ["PX_LAST", "EQY_INIT_PO_DT"]
    )

    px_val = df[df["field"] == "PX_LAST"]["value"].iloc[0]
    dt_val = df[df["field"] == "EQY_INIT_PO_DT"]["value"].iloc[0]

    assert isinstance(px_val, float)
    assert isinstance(dt_val, str)  # dummy date string


# ─────────────────────────────────────────────────────────────
# BULKREF TESTS
# ─────────────────────────────────────────────────────────────

def test_dummy_bulkref_member_count(dummy_con):
    df = dummy_con.bulkref("SPX INDEX", "INDEX_MEMBERS_SHARES")

    # expect 10 members * 2 fields = 20 rows
    assert len(df["position"].unique()) == 10


def test_dummy_bulkref_position_grouping(dummy_con):
    df = dummy_con.bulkref("SPX INDEX", "INDEX_MEMBERS_SHARES")

    grouped = df.groupby("position")

    for pos, g in grouped:
        names = set(g["name"])
        assert "Index Member" in names
        assert "Number of Shares" in names


def test_dummy_bulkref_ticker_format(dummy_con):
    df = dummy_con.bulkref("SPX INDEX", "INDEX_MEMBERS_SHARES")

    tickers = df[df["name"] == "Index Member"]["value"].unique()

    for t in tickers:
        assert t.endswith("US EQUITY")
        assert re.match(r"^[A-Z]+ US EQUITY$", t)


def test_dummy_bulkref_no_duplicate_members(dummy_con):
    df = dummy_con.bulkref("SPX INDEX", "INDEX_MEMBERS_SHARES")

    tickers = df[df["name"] == "Index Member"]["value"]

    assert tickers.nunique() == len(tickers)


def test_dummy_bulkref_unknown_field_fallback(dummy_con):
    df = dummy_con.bulkref("SPX INDEX", "UNKNOWN_FIELD")

    # should still return data
    assert len(df) > 0
    assert set(df.columns) == {"ticker", "field", "name", "value", "position"}


# ─────────────────────────────────────────────────────────────
# BULKREF HIST TESTS
# ─────────────────────────────────────────────────────────────

def test_dummy_bulkref_hist_structure(dummy_con):
    df = dummy_con.bulkref_hist(
        "SPX INDEX",
        "INDEX_MEMBERS_SHARES",
        dates=["20240101", "20240201"]
    )

    assert set(df.columns) == {"date", "ticker", "field", "name", "value", "position"}
    assert df["date"].nunique() == 2


# ─────────────────────────────────────────────────────────────
# CONSISTENCY TESTS
# ─────────────────────────────────────────────────────────────

def test_dummy_deterministic_per_position(dummy_con):
    df = dummy_con.bulkref("SPX INDEX", "INDEX_MEMBERS_SHARES")

    # same position should always map to same ticker
    mapping = {}

    for _, row in df.iterrows():
        if row["name"] == "Index Member":
            pos = row["position"]
            val = row["value"]

            if pos in mapping:
                assert mapping[pos] == val
            else:
                mapping[pos] = val


def test_dummy_multiple_calls_consistent_shape(dummy_con):
    df1 = dummy_con.bulkref("SPX INDEX", "INDEX_MEMBERS_SHARES")
    df2 = dummy_con.bulkref("SPX INDEX", "INDEX_MEMBERS_SHARES")

    assert df1.shape == df2.shape
    assert list(df1.columns) == list(df2.columns)