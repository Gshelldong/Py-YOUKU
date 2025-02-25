import os

BASE_PATH = os.path.dirname(
    os.path.dirname(__file__)
)

UPLOAD_FILES = os.path.join(BASE_PATH,'upload_files')

DOWNLOAD_FILES = os.path.join(BASE_PATH,'download_files')