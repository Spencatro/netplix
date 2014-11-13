__author__ = 'sxh112430'
import os
import json
import os.path as path

RUNNING_LOCALLY = False
PROJECT_PATH = path.normpath(path.dirname(path.realpath(__file__)))
RUNNING_LOCALLY = True
DATA_DIR = path.join(PROJECT_PATH,"server","DATA")

RENDERER_HTTP_PORT = 49678
RENDERER_STREAM_PORT = 49679

SERVER_STREAM_PORT = 49680
SERVER_IP = "104.236.30.164"

DB_JSON_FILE = os.path.join(DATA_DIR,"db.json")

ALLOWED_EXTENSIONS = set(['mp4'])