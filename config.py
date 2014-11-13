__author__ = 'sxh112430'
import os
import json

RUNNING_LOCALLY = False
if not 'APACHE_LOCK_DIR' in os.environ:
    RUNNING_LOCALLY = True
    DATA_DIR = "../DATA/"
else:
    DATA_DIR = "/var/www/FlaskApp/netplix/server/DATA/"

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