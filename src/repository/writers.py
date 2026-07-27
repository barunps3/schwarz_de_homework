
class SparkWriter:
    def __init__(self, df: DataFrame):
        self.df = df

    def write_dataset(
        self,
        path: str,
        file_format: str = "parquet",
        mode: str = "overwrite",
        partition_by: Optional[List[str]] = None,
        **options
    ) -> None:
        """A single generic writer for any target format."""
        writer = self.df.write.format(file_format).mode(mode)
        if partition_by:
            writer = writer.partitionBy(*partition_by)
        if options:
            writer = writer.options(**options)
        writer.save(path)