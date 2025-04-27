import sys
import string
import spacy

from pyspark.sql import SparkSession
from pyspark.sql.types import ArrayType, StringType
from pyspark.sql.functions import explode, split, udf, col, to_json, struct

nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
	# Remove punctuations
	return "".join([ch.lower() for ch in text if ch == " " or (ch.isalpha() and ch not in string.punctuation)])

# Function to extract named entities from text
def extract_entities(text):
	named_entities = ["PERSON", "ORG", "GPE", "LOC", "EVENT", "WORK_OF_ART"]
	doc = nlp(preprocess_text(text))
	return [ent.text for ent in doc.ents if ent.label_.upper() in named_entities and len(ent.text.split()) == 1]

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("""
        Usage: entity_recognition_streaming.py <bootstrap-servers> <source_topic> <destination_topic>
        """, file=sys.stderr)
        sys.exit(-1)

    bootstrapServers = sys.argv[1]
    src_topic = sys.argv[2]
    dest_topic = sys.argv[3]

    spark = SparkSession\
        .builder\
        .appName("NamedEntityRecognition")\
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    print("Extracting entities")
	# Define a user-defined function (UDF) to extract named entities
    extract_entities_udf = udf(extract_entities, ArrayType(StringType()))

    df = spark.readStream \
		.format("kafka") \
		.option("kafka.bootstrap.servers", bootstrapServers) \
		.option("subscribe", src_topic) \
		.load()

    print("Tokenizing text")
	# Tokenize the message text
	# Split the lines into words
    df = df.select(
		# explode turns each item in an array into a separate row
		explode(split(df.value, ' ')).alias('word')
	)

    df = df.withColumn("entities", extract_entities_udf("word"))

	# Explode the array of named entities to individual rows
    df = df.select(explode("entities").alias("entity"))

	# Group by entity and count the occurrences
    agg_df = df.groupBy("entity").count()
	
    agg_df = agg_df.withColumn("value", to_json(struct(col("entity"), col("count"))))

    print(f"About to send data to kafka {dest_topic}")

    kafka_query = agg_df \
			.select("value") \
			.writeStream \
			.outputMode("update") \
			.format("kafka") \
			.option("kafka.bootstrap.servers", bootstrapServers) \
			.option("topic", dest_topic) \
			.option("checkpointLocation", "/tmp/checkpoint") \
			.start()

    console_query = agg_df \
            .select("value") \
            .writeStream \
			.outputMode("update") \
			.format("console") \
			.start()

    kafka_query.awaitTermination()
    console_query.awaitTermination()