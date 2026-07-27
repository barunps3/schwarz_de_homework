class SparkReader:
  def __init__(self, spark):
    self.spark = spark

  def read(self, 
        path: str,
        file_format: str,
        schema: Optional[StructType] = None,
        **options):
    reader = self.spark.read.format(file_format)
    if schema:
        reader = reader.schema(schema)
    if options:
        reader = reader.options(**options)
    return reader.load(path)