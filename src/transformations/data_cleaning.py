from datetime import datetime

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


# Get cleaned and quarantine df if given columns have null values
def quarantine_null_values(df: DataFrame, cols: list[str]) -> tuple[DataFrame, DataFrame]:
    """
    Quarantine rows with null values in the given columns.
    Returns a tuple of two DataFrames: the first is the cleaned DataFrame,
    the second is the quarantine DataFrame.
    """
    if not cols:
        raise ValueError("cols must be a non-empty list of column names")
    condition = df[cols[0]].isNull()
    for c in cols[1:]:
        condition = condition | df[c].isNull()
    return df.filter(~condition), df.filter(condition)


def quarantine_negative_values(df: DataFrame, cols: list[str]) -> tuple[DataFrame, DataFrame]:
    """
    Quarantine rows with negative values in the given columns.
    Returns a tuple of two DataFrames: the first is the cleaned DataFrame,
    the second is the quarantine DataFrame.
    """
    if not cols:
        raise ValueError("cols must be a non-empty list of column names")
    condition = df[cols[0]] < 0
    for c in cols[1:]:
        condition = condition | (df[c] < 0)
    return df.filter(~condition), df.filter(condition)


def quarantine_date_range(
    df: DataFrame, start_datetime: datetime, end_datetime: datetime, col: str
) -> tuple[DataFrame, DataFrame]:
    """
    Quarantine rows with dates outside the given range.
    start_datetime: start time
    end_datetime: end time, will be excluded
    Returns a tuple of two DataFrames: the first is the cleaned DataFrame,
    the second is the quarantine DataFrame.
    """
    if not start_datetime or not end_datetime or not col:
        raise ValueError("start_date and end_date must be non-empty strings")
    condition = (df[col] >= F.lit(start_datetime)) & (df[col] < F.lit(end_datetime))
    return df.filter(condition), df.filter(~condition)


def timestamp_normalization(
    df: DataFrame,
    timestamp_col: str,
    timezone: str,
    rename_timestamp_col: str = "",
) -> DataFrame:
    """
    Replace timestamp_col with UTC timestamp and Local timestamp.

    timezone: timezone of the timestamp_col as known by the user
    timestamp_col: the raw timestamp column
    rename_timestamp_col: name used to derive utc and local timestamp cols

    Returns a DataFrame with utc_timestamp column and local_timestamp column
    """
    if not timestamp_col or not timezone:
        raise ValueError("timestamp_col and timezone must be non-empty strings")
    if not rename_timestamp_col:
        rename_timestamp_col = timestamp_col

    utc_timestamp_col_name = f"{rename_timestamp_col}_utc"
    local_timestamp_col_name = f"{rename_timestamp_col}_local"
    df = (
        df.withColumn(utc_timestamp_col_name, F.to_utc_timestamp(timestamp_col, timezone))
        .withColumn(
            local_timestamp_col_name, F.from_utc_timestamp(utc_timestamp_col_name, timezone)
        )
        .drop(timestamp_col)
    )
    return df
