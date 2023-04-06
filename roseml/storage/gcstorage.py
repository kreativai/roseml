from google.cloud import storage
import re
from typing import Tuple, Union
from pathlib import Path
from yarl import URL
from tqdm import tqdm

class GCStorage:
    def __init__(self, creds=None, project_id=None):
        """

        Args:
            creds (_type_, optional): path to json adc key
            project_id deprecated
        """
        if creds:
            self.client = storage.Client.from_service_account_json(creds)
        elif project_id:
            self.client = storage.Client(project_id)
        else:
            self.client = storage.Client()
    
    def _parse_gs_url(self, gs_uri: str) -> Tuple[str, str]:
        matches = re.match("gs://(.*?)/(.*)", gs_uri)
        if matches:
            bucket_name, object_name = matches.groups()
        else:
            raise ValueError(f"{gs_uri} is not valid gs filename")
        return bucket_name, object_name

    def _get_gs_blob(self, gs_uri: str) -> storage.Blob:
        bucket_name, gs_filename = self._parse_gs_url(gs_uri)
        bucket = storage.Bucket(self.client, bucket_name)
        blob = storage.Blob(gs_filename, bucket)
        return blob

    def download_file(self, gs_uri: str, local_filename: str) -> None:
        """
        Args:
            gs_uri (str): full gs filename gs://bucket_name/filename
            local_filename (str): abs or relative localpath
        """
        blob = self._get_gs_blob(gs_uri)
        blob.download_to_filename(local_filename)

    def upload_file(self, gs_uri: str, local_filename: str) -> None:
        """
        Args:
            gs_uri (str): full gs filename gs://bucket_name/filename
            local_filename (str): abs or relative localpath
        """
        blob = self._get_gs_blob(gs_uri)
        blob.upload_from_filename(local_filename)

    def upload_from_string(self, gs_uri: Union[URL, str], serialized_data: str) -> None:
        """
        Args:
            gs_uri (str): full gs filename gs://bucket_name/filename
            binary (bytes): binary
        """
        gs_uri = str(gs_uri)
        blob = self._get_gs_blob(gs_uri)
        blob.upload_from_string(serialized_data)

    def exists(self, gs_uri: str) -> bool:
        """
        Args:
            gs_uri (str): full gs filename gs://bucket_name/filename
        Returns:
            bool: exists or not
        """
        blob = self._get_gs_blob(gs_uri)
        return blob.exists()
    
    def list_blobs_from_folder(self, gs_folder_uri: str) -> iter:
        bucket_name, folder_name = self._parse_gs_url(gs_uri=gs_folder_uri)
        bucket = storage.Bucket(self.client, bucket_name)
        return bucket.list_blobs(prefix=folder_name)
    
    def download_files_from_folder(self, gs_folder_uri: str, local_folder: str) -> None:
        file_blobs = self.list_blobs_from_folder(gs_folder_uri=gs_folder_uri)
        Path(local_folder).mkdir(parents=True, exist_ok=True)
        for blob in file_blobs:
            if blob.name.endswith('/'): # skip folders
                continue
            local_filename = f'{local_folder}/{Path(blob.name).name}'
            blob.download_to_filename(local_filename)
    
    def download_folder(self, gs_folder_uri: str, local_folder: str) -> None:
        bucket_name, folder_name = self._parse_gs_url(gs_uri=gs_folder_uri)
        
        bucket = self.client.get_bucket(bucket_or_name=bucket_name)
        blobs = bucket.list_blobs(prefix=folder_name)

        Path(local_folder).mkdir(parents=True)
        for blob in tqdm(blobs):
            filename = f'{local_folder}/{blob.name.replace(folder_name, "")}'
            Path(filename).parent.mkdir(parents=True, exist_ok=True)
            blob.download_to_filename(filename)

    def upload_folder(self, gs_folder_uri: str, local_folder: str) -> None:
        """slow - todo increase speed

        Args:
            gs_folder_uri (str): _description_
            local_folder (str): _description_
        """
        local_folder = Path(local_folder)
        local_paths = local_folder.glob('**/*')
        for path in local_paths:
            print(path)
            if path.is_dir():
                continue
            relative_path = path.relative_to(local_folder)
            self.upload_file(gs_uri=gs_folder_uri + '/' + str(relative_path), 
                             local_filename=str(path))

    def update_metadata(self, gs_uri: str, metadata: dict) -> None:
        """
        Args:
            gs_uri (str): full gs filename gs://bucket_name/filename
            metadata (dict): example: {'color': 'Red', 'name': 'Test'}
        """
        blob = self._get_gs_blob(gs_uri)
        blob.metadata = metadata
        blob.patch()
