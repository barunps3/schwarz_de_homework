from datetime import datetime

import pytest
from pyspark.sql.types import StructField, StructType, TimestampType

from transformations.data_cleaning import quarantine_date_range, timestamp_normalization


def test_timestamp_normalization_creates_utc_and_local_columns(spark):
    data = [(datetime(2024, 1, 1, 0, 0),), (datetime(2024, 1, 1, 12, 0),)]
    schema = StructType([StructField("pickup_datetime", TimestampType(), True)])
    input_df = spark.createDataFrame(data, schema)

    result_df = timestamp_normalization(
        input_df,
        timestamp_col="pickup_datetime",
        timezone="America/New_York",
        rename_timestamp_col="pickup",
    )

    assert "pickup_datetime" not in result_df.columns
    assert "pickup_utc" in result_df.columns
    assert "pickup_local" in result_df.columns

    rows = result_df.select("pickup_utc", "pickup_local").collect()
    assert rows[0]["pickup_utc"] == datetime(2024, 1, 1, 5, 0)
    assert rows[0]["pickup_local"] == datetime(2024, 1, 1, 0, 0)
    assert rows[1]["pickup_utc"] == datetime(2024, 1, 1, 17, 0)
    assert rows[1]["pickup_local"] == datetime(2024, 1, 1, 12, 0)


def test_timestamp_normalization_raises_for_empty_inputs(spark):
    input_df = spark.createDataFrame(
        [],
        StructType([StructField("pickup_datetime", TimestampType())]),
    )

    with pytest.raises(
        ValueError,
        match="timestamp_col and timezone must be non-empty strings",
    ):
        timestamp_normalization(input_df, "", "America/New_York")


def test_quarantine_date_range_handles_boundaries_and_edge_values(spark):
    data = [
        (datetime(2023, 12, 31, 23, 59, 59),),
        (datetime(2024, 1, 1, 0, 0),),
        (datetime(2024, 1, 1, 12, 0),),
        (datetime(2024, 1, 2, 0, 0),),
    ]
    schema = StructType([StructField("event_time", TimestampType(), True)])
    input_df = spark.createDataFrame(data, schema)

    cleaned_df, quarantined_df = quarantine_date_range(
        input_df,
        start_datetime=datetime(2024, 1, 1, 0, 0),
        end_datetime=datetime(2024, 1, 2, 0, 0),
        col="event_time",
    )

    cleaned_times = [row["event_time"] for row in cleaned_df.collect()]
    quarantined_times = [row["event_time"] for row in quarantined_df.collect()]

    assert cleaned_times == [datetime(2024, 1, 1, 0, 0), datetime(2024, 1, 1, 12, 0)]
    assert quarantined_times == [
        datetime(2023, 12, 31, 23, 59, 59),
        datetime(2024, 1, 2, 0, 0),
    ]


def test_quarantine_date_range_raises_for_missing_inputs(spark):
    input_df = spark.createDataFrame([], StructType([StructField("event_time", TimestampType())]))

    with pytest.raises(ValueError, match="start_date and end_date must be non-empty strings"):
        quarantine_date_range(input_df, None, datetime(2024, 1, 2, 0, 0), "event_time")
