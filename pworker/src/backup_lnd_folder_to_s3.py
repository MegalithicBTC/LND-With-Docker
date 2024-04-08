import os
import zipfile
import uuid
import boto3
import shutil
import time

def run_backup():
    # Use environment variables for AWS credentials and region
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_region = 'us-west-2'  # Specify your desired AWS region here

    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,  # Specify the region here
    )

    def upload_file_to_s3(file_path, bucket_name, folder_name, file_name_on_s3):
        file_name = file_name_on_s3
        s3_object_key = os.path.join(folder_name, file_name)

        try:
            s3.upload_file(file_path, bucket_name, s3_object_key,
                ExtraArgs={'StorageClass': 'INTELLIGENT_TIERING'})
            print(f'Uploaded {file_path} to S3 as {s3_object_key}')
        except Exception as e:
            print(f'Error uploading {file_path} to S3: {str(e)}')

    channel_alias = os.environ.get('alias')

    # Define the paths to the source files and folders
    lnd_folder = "/workspace/bound_lnd_folder"
    lnd_machine_specific_env = "/workspace/parent_folder/lnd_machine_specific.env"
    evacuate_folder = "/workspace/parent_folder/evacuate"

    # Create a temporary directory for zipping
    temp_dir = "/tmp/temp_zip"
    os.makedirs(temp_dir, exist_ok=True)

    # Copy all files to the temporary directory
    for root, dirs, files in os.walk(lnd_folder):
        for file in files:
            file_path = os.path.join(root, file)
            dest_path = os.path.join(temp_dir, os.path.relpath(file_path, lnd_folder))
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(file_path, dest_path)

    shutil.copy2(lnd_machine_specific_env, os.path.join(temp_dir, os.path.basename(lnd_machine_specific_env)))

    # Define the name of the zip archive you want to create
    zip_filename = channel_alias + "-" + "lnd_archive.zip"
    zip_path = evacuate_folder + "/" + zip_filename

    # Create a new zip archive from the temporary directory
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                archive_path = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, archive_path)

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)

    print(f"Created {zip_filename} containing lnd folder, lnd_machine_specific.env.")
    uuid_str = str(uuid.uuid4())
    s3_filename = zip_filename.replace(".zip", uuid_str + ".zip")
    upload_file_to_s3(zip_path, "ezvid-lightning", 'node-backups', s3_filename)
    print('uploaded to s3')

while True:
    # print('sleeping before backup')
    # time.sleep(500)
    run_backup()
    time.sleep(43200) # 12 hours
    print('done sleeping, starting backup loop again')