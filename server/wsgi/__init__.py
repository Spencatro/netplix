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
import time
import threading

import config
import vlc

if not os.path.exists(config.DB_JSON_FILE):
    # make the empty db file
    # Should only ever happen once
    with open(config.DB_JSON_FILE, 'w') as fp:
        empty_db = {"SCHEMA_VERSION":1.0}
        json.dump(empty_db, fp)

vlc_instance = vlc.Instance()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in config.ALLOWED_EXTENSIONS

class NetplixApp(Flask):

    def __init__(self, arg):
        #
        super(NetplixApp, self).__init__(arg)
        self.route("/")(self.index)
        self.route("/index")(self.index)
        self.route('/threadtest')(self.threadtest)
        self.route('/upbloat', methods=['GET', 'POST'])(self.upload)
        self.route("/clear_db_are_you_sure_yes_i_am")(self.clear_db)
        self.route("/envinfo")(self.envinfo)
        self.route("/dbdump")(self.dbdump)
        self.route("/search/by_title/<title>")(self.search_by_title)
        self.route("/search/by_actor/<actor>")(self.search_by_actor)
        self.route("/search/<search_string>")(self.search)
        self.route("/play/<resource_id>")(self.play)
        self.route("/heartbeat/")(self.heartbeat)
        self.route("/show/")(self.show_vlm)

    def load_db_file(self):
        with open(config.DB_JSON_FILE) as fp:
            jsonificated = json.load(fp)
        return jsonificated

    def index(self):
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

    def threadtest(self):
        pass


    def upload(self):
        if request.method == 'POST':
            file = request.files['file']
            actors = request.form['actors'].split(",")
            title = request.form['title']
            if not actors or not title:
                return "Error: Must complete form!"
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                db_dict = self.load_db_file()
                if not 'id_pointer' in db_dict:
                    db_dict['id_pointer'] = 10 # Just in case
                id_pointer = int(db_dict['id_pointer'])
                db_dict['catalog'][id_pointer] = {
                    'title':title,
                    'actors':actors,
                    'filepath':os.path.join(config.DATA_DIR,filename)
                }
                db_dict["id_pointer"] = id_pointer+1
                with open(config.DB_JSON_FILE,'w') as fp:
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

    def clear_db(self):
        with open(config.DB_JSON_FILE, 'w') as fp:
            json.dump({'id_pointer':0,'catalog':{}}, fp)
        return "Success, db is empty"

    def envinfo(self):
        return jsonify(os.environ)

    def dbdump(self):
        return jsonify(self.load_db_file())

    def search_by_title(self, title):
        db_dict = self.load_db_file()
        results_dict = {}
        catalog = db_dict['catalog']
        for key in catalog.keys():
            if title.lower() in catalog[key]['title'].lower():
                results_dict[key] = catalog[key]
        return jsonify(results_dict)


    def search_by_actor(self, actor):
        db_dict = self.load_db_file()
        results_dict = {}
        catalog = db_dict['catalog']
        for key in catalog.keys():
            for actor_string in catalog[key]['actors']:
                if actor.lower() in actor_string.lower():
                    results_dict[key] = catalog[key]
        return jsonify(results_dict)

    def search(self, search_string):
        db_dict = self.load_db_file()
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


    def play(self, resource_id):
        db_dict = self.load_db_file()
        catalog = db_dict['catalog']
        if resource_id not in catalog.keys():
            return "ERROR: Video with ID "+str(resource_id)+" does not exist!", 404
        title = db_dict['catalog'][resource_id]['title']
        filepath = db_dict['catalog'][resource_id]['filepath']

        rtsp_uri = 'rtsp://'+str(config.SERVER_IP)+':'+str(config.RENDERER_STREAM_PORT)+'/'+str(resource_id)+'.sdp'
        sout = '#rtp{dst='+config.SERVER_IP+',port='+str(config.SERVER_STREAM_PORT)+',sdp='+rtsp_uri+'}'

        def threading_target():
            vlc_instance.vlm_add_broadcast(str(resource_id), filepath, sout, 0, None, True, False)
            vlc_instance.vlm_play_media(str(resource_id))
            time.sleep(100)


        thread = threading.Thread(target=threading_target)
        thread.start()

        db_dict['now_playing'] = rtsp_uri

        with open(config.DB_JSON_FILE,'w') as fp:
            json.dump(db_dict, fp)
        
        return jsonify({'rtsp':rtsp_uri})

    def heartbeat(self):
        db = self.load_db_file()
        uri = db['now_playing']
        return jsonify({'uri':uri})

    def show_vlm(self):
        res = vlc_instance.vlm_show_media()
        return str(dir(res))


app = NetplixApp(__name__)
app.config['UPLOAD_FOLDER'] = config.DATA_DIR

if __name__ == "__main__":
    pass
    app.run(debug = "True")
