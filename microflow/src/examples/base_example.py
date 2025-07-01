from microflow.datasources.http import HttpDataSource
from microflow.outputs.gcs import GCSOutput
from microflow.pipeline import run_pipeline

cat_data_source = HttpDataSource(host="https://catfact.ninja", endpoint="fact")
gcs_output = GCSOutput(bucket_name="dev-bucket-7592u5", blob_path="cat_facts")

 
run_pipeline(
    pipeline_name="cat_facts",
    ingestion=cat_data_source,
    outputs=[gcs_output]
)
