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

DB_JSON_FILE = os.path.join(DATA_DIR,"db.json")

if not os.path.exists(DB_JSON_FILE):
    # make the empty db file
    # Should only ever happen once
    with open(DB_JSON_FILE, 'w') as fp:
        empty_db = {"SCHEMA_VERSION":1.0}
        json.dump(empty_db, fp)
ALLOWED_EXTENSIONS = set(['mp4'])