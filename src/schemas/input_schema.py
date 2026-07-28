from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    DoubleType,
    StringType
)

NEW_YORK_WEATHER_SCHEMA = StructType([
    StructField("year", StringType(), False),
    StructField("month", StringType(), False),
    StructField("day", StringType(), False),

    StructField("temp", DoubleType(), True),
    StructField("temp_source", StringType(), True),

    StructField("tmin", DoubleType(), True),
    StructField("tmin_source", StringType(), True),

    StructField("tmax", DoubleType(), True),
    StructField("tmax_source", StringType(), True),

    StructField("rhum", IntegerType(), True),
    StructField("rhum_source", StringType(), True),

    StructField("prcp", DoubleType(), True),
    StructField("prcp_source", StringType(), True),

    StructField("wspd", DoubleType(), True),
    StructField("wspd_source", StringType(), True),

    StructField("pres", DoubleType(), True),
    StructField("pres_source", StringType(), True),

    StructField("cldc", IntegerType(), True),
    StructField("cldc_source", StringType(), True),
])