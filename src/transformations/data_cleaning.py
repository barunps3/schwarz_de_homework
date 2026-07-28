from pyspark.sql import DataFrame
from pyspark.sql import functions as F

# Get cleaned and quarantine df if given columns have null values
def quarantine_null_values(df: DataFrame, cols: list[str]) -> tuple[DataFrame, DataFrame]:
    """
    Quarantine rows with null values in the given columns.
    Returns a tuple of two DataFrames: the first is the cleaned DataFrame, the second is the quarantine DataFrame."""
    if not cols:
        raise ValueError("cols must be a non-empty list of column names")
    condition = df[cols[0]].isNull()
    for c in cols[1:]:
        condition = condition | df[c].isNull()
    return df.filter(~condition), df.filter(condition)


def quarantine_negative_values(df: DataFrame, cols: list[str]) -> tuple[DataFrame, DataFrame]:
    """
    Quarantine rows with negative values in the given columns.
    Returns a tuple of two DataFrames: the first is the cleaned DataFrame, the second is the quarantine DataFrame."""
    if not cols:
        raise ValueError("cols must be a non-empty list of column names")
    condition = df[cols[0]] < 0
    for c in cols[1:]:
        condition = condition | (df[c] < 0)
    return df.filter(~condition), df.filter(condition)


def quarantine_date_range(df: DataFrame,
    start_date: str,
    end_date: str, 
    date_format: str,
    cols: list[str]) -> tuple[DataFrame, DataFrame]:
    """
    Quarantine rows with dates outside the given range.
    Returns a tuple of two DataFrames: the first is the cleaned DataFrame,
    the second is the quarantine DataFrame."""
    if not cols:
        raise ValueError("cols must be a non-empty list of column names")
    if not start_date or not end_date:
        raise ValueError("start_date and end_date must be non-empty strings")
    condition = (df[cols[0]] < start_date) | (df[cols[0]] > end_date)
    for c in cols:
        condition = condition | (df[c] < start_date) | (df[c] > end_date)
    return df.filter(~condition), df.filter(condition)
