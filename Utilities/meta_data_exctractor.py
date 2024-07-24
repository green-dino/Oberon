import os
import hashlib
import time
from typing import Dict, Optional

class FileMetadataExtractor:
    @staticmethod
    def extract_metadata(file_path: str) -> Dict[str, any]:
        metadata = {}
        try:
            if not os.path.exists(file_path):
                metadata['error'] = "File does not exist"
                return metadata

            file_stat = os.stat(file_path)
            metadata.update({
                'mactimes': [
                    time.ctime(file_stat.st_atime),
                    time.ctime(file_stat.st_mtime),
                    time.ctime(file_stat.st_ctime)
                ],
                'mode': file_stat.st_mode,
                'file_size': file_stat.st_size,
                'uid': file_stat.st_uid,
                'gid': file_stat.st_gid,
                'is_file': os.path.isfile(file_path),
                'is_link': os.path.islink(file_path),
                'is_directory': os.path.isdir(file_path),
                'is_mount': os.path.ismount(file_path),
                'accessible': os.access(file_path, os.R_OK) and os.path.isfile(file_path)
            })
            
            if metadata['accessible']:
                with open(file_path, 'rb') as fp:
                    metadata['buffer'] = fp.read()
            else:
                metadata['buffer'] = b''
        except OSError as e:
            metadata['error'] = f"File exception: {str(e)}"
        return metadata

class FileHasher:
    def __init__(self, buffer: bytes):
        self.buffer = buffer

    def hash_file(self, hash_type: str) -> Optional[str]:
        hash_functions = {
            "MD5": hashlib.md5,
            "SHA1": hashlib.sha1,
            "SHA224": hashlib.sha224,
            "SHA256": hashlib.sha256,
            "SHA384": hashlib.sha384,
            "SHA512": hashlib.sha512
        }
        try:
            if hash_type in hash_functions:
                hash_obj = hash_functions[hash_type]()
                hash_obj.update(self.buffer)
                return hash_obj.hexdigest().upper()
            else:
                raise ValueError("Invalid Hash Type Specified")
        except Exception as e:
            raise RuntimeError(f"File Hash Failure: {str(e)}")

class FileExaminer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.metadata = FileMetadataExtractor.extract_metadata(file_path)
        self.hasher = FileHasher(self.metadata.get('buffer', b''))
        self.last_error = self.metadata.get('error', "OK")
        self.file_type = self._determine_file_type()
        self.mount_point = self.metadata.get('is_mount', False)

    def _determine_file_type(self) -> str:
        if self.metadata.get('is_file'):
            return "File"
        elif self.metadata.get('is_link'):
            return "Link"
        elif self.metadata.get('is_directory'):
            return "Directory"
        return "Unknown"

    def get_last_hash(self, hash_type: str) -> str:
        return getattr(self.hasher, hash_type.lower(), "")

    def __del__(self):
        print(f"FileExaminer object for {os.path.basename(self.file_path)} deleted.")
