from pyspark.sql import DataFrame
from pyspark.sql.types import StructType


class SparkRepository:
    def __init__(self, spark):
        self.spark = spark

    def read(self, path: str, file_format: str, schema: StructType | None = None, **options):
        reader = self.spark.read.format(file_format)
        if schema:
            reader = reader.schema(schema)
        if options:
            reader = reader.options(**options)
        return reader.load(path)

    def write(
        self,
        df: DataFrame,
        path: str,
        file_format: str = "parquet",
        mode: str = "overwrite",
        partition_by: list[str] | None = None,
        **options,
    ) -> None:
        """A single generic writer for any target format."""
        writer = df.write.format(file_format).mode(mode)
        if partition_by:
            writer = writer.partitionBy(*partition_by)
        if options:
            writer = writer.options(**options)
        writer.save(path)
