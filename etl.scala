import org.apache.spark.sql.types._

val inputPath = "/databricks-datasets/structured-streaming/events/"

// Since we know the data format already, let's define the schema to speed up processing (no need for Spark to infer schema)
val jsonSchema = new StructType().add("time", TimestampType).add("action", StringType)

val staticInputDF =
  spark
    .read
    .schema(jsonSchema)
    .json(inputPath)

display(staticInputDF)
