import os
import time
import boto3
import uuid
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import FileModifiedEvent, FileMovedEvent

# Use environment variables for AWS credentials and region
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
aws_region = os.environ.get('S3_BUCKET_REGION')
bucket_name =  os.environ.get('S3_BUCKET_NAME')

print("starting watch_backups.py")

# AWS S3 Bucket and Folder settings
folder_name = 'lnd-channel-backups'

lnd_folder = " /workspace/lightning/lnd/"
file_to_monitor = lnd_folder + "lnd-data/data/chain/bitcoin/mainnet/channel.backup"
print("monitoring this file", file_to_monitor)

# Initialize S3 client with the specified region
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region,  # Specify the region here
)

# Upload function
def upload_file_to_s3(file_path, bucket_name, folder_name):
    channel_backup_filenames_on_s3 =  str(uuid.uuid4())[:6] + '-' + "channel.backup"
    file_name = channel_backup_filenames_on_s3
    s3_object_key = os.path.join(folder_name, file_name)
    try:
        s3.upload_file(file_path, bucket_name, s3_object_key)
        print(f'Uploaded {file_path} to S3 as {s3_object_key}')
    except Exception as e:
        print(f'Error uploading {file_path} to S3: {str(e)}')

# Check for the existence of channel.backup file with retries
while not os.path.exists(file_to_monitor):
    print(f'{file_to_monitor} does not exist. Retrying in 10 seconds...')
    time.sleep(10)

# Upload the backup immediately on script boot
upload_file_to_s3(file_to_monitor, bucket_name, folder_name)

class FileChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if isinstance(event, ( FileMovedEvent)):
            if event.dest_path == file_to_monitor:
                print(f'Event type: {event.event_type} - dest path: {event.dest_path}')
                upload_file_to_s3(file_to_monitor, bucket_name, folder_name)
               
# Create an observer to watch for file changes
observer = Observer()
observer.schedule(FileChangeHandler(), path=os.path.dirname(file_to_monitor), recursive=False)
observer.start()

print('---uploading channel backup on start--- ')
upload_file_to_s3(file_to_monitor, bucket_name, folder_name)
try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    observer.stop()
observer.join()