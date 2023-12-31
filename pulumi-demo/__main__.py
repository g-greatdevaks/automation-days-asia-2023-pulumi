"""A Google Cloud Python Pulumi program"""

import pulumi
from pulumi_gcp import storage

# Create a GCP resource (Storage Bucket)
#bucket = storage.Bucket('my-bucket', location="US")

bucket = storage.Bucket(
    "my-bucket",
    location="US",
    website=storage.BucketWebsiteArgs(main_page_suffix="index.html"),
    uniform_bucket_level_access=True,
)

bucketObject = storage.BucketObject(
    'index.html',
    bucket=bucket.name,
    content_type='text/html',
    source=pulumi.FileAsset('index.html')
)

bucketIAMBinding = storage.BucketIAMBinding('my-bucket-IAMBinding',
    bucket=bucket.name,
    role="roles/storage.objectViewer",
    members=["allUsers"]
)

# Export the DNS name of the bucket
pulumi.export('bucket_name', bucket.url)

# Export the bucket's endpoint URL.
pulumi.export('bucket_endpoint', pulumi.Output.concat('http://storage.googleapis.com/', bucket.id, "/", bucketObject.name))