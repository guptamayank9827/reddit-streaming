import time
import sys
import praw
import os
from dotenv import load_dotenv
from kafka import KafkaProducer


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("""
        Usage: reddit_streaming.py <topics>
        """, file=sys.stderr)
        sys.exit(-1)

    topic = sys.argv[1]

    load_dotenv()

    sub_reddit = os.getenv('SUBREDDIT')
    query_wait_time = int(os.getenv('QUERY_WAIT_TIME_SECONDS'))

    # Initialize Reddit OAuth
    reddit = praw.Reddit(
        client_id = os.getenv('CLIENT_ID'),
        client_secret = os.getenv('CLIENT_SECRET'),
        user_agent = os.getenv('APP_NAME')
    )
    print("Reddit API Set")

    # Initialize the producer
    kafka_producer = KafkaProducer(bootstrap_servers="kafka:9092")
    print("Kafka Producer Set")

    while True:
        # Produce messages
        for index, submission in enumerate(reddit.subreddit(sub_reddit).new()):
            print(submission.title)
            kafka_producer.send(topic, submission.title.encode("utf-8"))

        kafka_producer.flush()

        time.sleep(query_wait_time)