/**
 * Created by Morgan on 11/14/2014.
 */
package org.molabs.netplixcontroller.models;

import java.util.ArrayList;

public class Media {
    private int id;
    private ArrayList<String> actors = new ArrayList<String>();
    private String filePath;
    private String title;
    private String previewUrl;

    public Media() {

    }

    public Media(int id, String filePath, String title) {
        this.id = id;
        this.filePath = filePath;
        this.title = title;
    }

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }

    public ArrayList<String> getActors() { return actors; }
    public void setActors(ArrayList<String> actors) { this.actors = actors; }

    public String getFilePath() { return filePath; }
    public void setFilePath(String filePath) { this.filePath = filePath; }

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getPreviewUrl() { return title; }
    public void setPreviewUrl(String previewUrl) { this.previewUrl = previewUrl; }

    public String toString() { return title; }
}
