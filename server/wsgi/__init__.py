import os
# import pygst
import json
import threading
import pprint
from flask import Flask, jsonify, request, redirect, url_for
from flask import render_template, abort
from flask import request
from werkzeug import secure_filename
import requests

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
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = DATA_DIR

def load_db_file():
    with open(DB_JSON_FILE) as fp:
        jsonificated = json.load(fp)
    return jsonificated


#Create our index or root / route
@app.route("/")
@app.route("/index")
def index():
    return "<h1>Netplix server</h1>" \
           "<p>The following is a short API for the Netplix server</p>" \
           "<p>All pages return a json file. Most languages can trivially parse json.</p>" \
           "<p><b>http://root-url/search/[some string]</b>: searches both titles and actor lists<br>" \
           "<b>http://root-url/search/by_actor/[some string]</b>: searches by actor list only<br>" \
           "<b>http://root-url/search/by_title/[some string]</b>: searches by title only<br>" \
           "<b>http://root-url/dbdump</b>: shows a dump of the current database<br>" \
           "<b>http://root-url/envinfo</b>: lists all environment variables<br>" \
           "<b>http://root-url/play/[Integer ID]</b>: NOT IMPLEMENTED: begins playing title by ID--not title!<br>" \
           "<b>http://root-url/[URL HIDDEN, ADMIN ONLY!]</b>: Deletes all entries in the database<br>" \
           "<b>http://root-url/[URL HIDDEN, ADMIN ONLY!]</b>: upload page</p>" \
           ""

@app.route('/threadtest')
def threadtest():
    pass

@app.route('/upbloat', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        actors = request.form['actors'].split(",")
        title = request.form['title']
        if not actors or not title:
            return "Error: Must complete form!"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            db_dict = load_db_file()
            if not 'id_pointer' in db_dict:
                db_dict['id_pointer'] = 10 # Just in case
            id_pointer = int(db_dict['id_pointer'])
            db_dict['catalog'][id_pointer] = {
                'title':title,
                'actors':actors,
                'filepath':os.path.join(DATA_DIR,filename)
            }
            db_dict["id_pointer"] = id_pointer+1
            with open(DB_JSON_FILE,'w') as fp:
                json.dump(db_dict, fp)
            return "Success! File "+str(filename)+" was uploaded"+str(actors)
        else:
            return "Error: File "+str(file.filename)+" is not in allowed filetype list."
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file><br>
         Title:<input type=text name=title><br>
         Actors (comma separated):<input type=text name=actors><br>
         <input type=submit value=Upload>
    </form>
    '''

@app.route("/clear_db_are_you_sure_yes_i_am")
def clear_db():
    with open(DB_JSON_FILE, 'w') as fp:
        json.dump({'id_pointer':0,'catalog':{}}, fp)
    return "Success, db is empty"

@app.route("/envinfo")
def envinfo():
    return jsonify(os.environ)

@app.route("/dbdump")
def dbdump():
    return jsonify(load_db_file())

@app.route("/search/by_title/<title>")
def search_by_title(title):
    db_dict = load_db_file()
    results_dict = {}
    catalog = db_dict['catalog']
    for key in catalog.keys():
        if title.lower() in catalog[key]['title'].lower():
            results_dict[key] = catalog[key]
    return jsonify(results_dict)

@app.route("/search/by_actor/<actor>")
def search_by_actor(actor):
    db_dict = load_db_file()
    results_dict = {}
    catalog = db_dict['catalog']
    for key in catalog.keys():
        for actor_string in catalog[key]['actors']:
            if actor.lower() in actor_string.lower():
                results_dict[key] = catalog[key]
    return jsonify(results_dict)

@app.route("/search/<search_string>")
def search(search_string):
    db_dict = load_db_file()
    results_dict = {}
    catalog = db_dict['catalog']
    for key in catalog.keys():
        if search_string.lower() in catalog[key]['title'].lower():
            results_dict[key] = catalog[key]
            continue
        for actor in catalog[key]['actors']:
            if search_string.lower() in actor.lower():
                results_dict[key] = catalog[key]
                continue
    return jsonify(results_dict)

@app.route("/play/<id>")
def play(id):
    db_dict = load_db_file()
    catalog = db_dict['catalog']
    if id not in catalog.keys():
        return "ERROR: Video with ID "+str(id)+" does not exist!", 404
    title = db_dict['catalog'][id]['title']
    return "You tried to play "+str(title)+"<br />ERROR: Not yet implemented"

@app.route("/register_new_renderer/")
def register_new_renderer(ip):
    new_ip = request.remote_addr
    r = requests.get("http://"+str(new_ip)+":"+RENDERER_HTTP_PORT)
    if r.status_code != 200:
        return "ERROR: Your IP is not running a renderer webserver. Failed to register renderer."
    else:
        return "Your IP:"+str(request.remote_addr)+"<br>You said your IP is:"+str(ip)

@app.route("/list_renderers")
def list_renderers():
    pass


if __name__ == "__main__":
    pass
    app.run(debug = "True")
