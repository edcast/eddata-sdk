from google.cloud import bigquery
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--cred_file", "-c", help = "Absolute path of the service account json")
parser.add_argument("--query", "-q", help = "Query to run against bigquery")
parser.add_argument("--out", "-o", help = "Path with file name - '/home/user/user_card_perf.csv'", default= "./output.csv")
args = parser.parse_args()

CRED_FILE = args.cred_file
QUERY = args.query
OUTPUT = args.out

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CRED_FILE

client = bigquery.Client()

result = client.query(QUERY).to_dataframe()  # Make an API request.


print("Storing data in CSV : " + OUTPUT)
result.to_csv(OUTPUT, index=False)
