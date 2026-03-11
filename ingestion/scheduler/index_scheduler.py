import schedule
import time
from ingestion.batch.batch_ingest import run_batch_ingestion


def run_job():

    print("Running scheduled indexing job...")

    run_batch_ingestion()


schedule.every(1).hours.do(run_job)

print("Index scheduler started")

while True:

    schedule.run_pending()

    time.sleep(1)