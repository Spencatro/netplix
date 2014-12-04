/**
 * Created by Morgan on 11/19/2014.
 */
package org.molabs.netplixcontroller.utilities;

public class UrlBuilder {
    public static String url;

    static {
        url = "http://np.spencer-hawkins.com/";
    }
    /*public UrlBuilder() {
        this.url = "http://np.spencer-hawkins.com/";
    }*/

    public static String dbDump() {
        return url + "dbdump";
    }

    public static String search(String query) {
        return url + "search/" + query;
    }

    public static String searchByActor(String query) {
        return url + "search/by_actor/" + query;
    }

    public static String searchByTitle(String query) {
        return url + "search/by_title/" + query;
    }

    public static String envinfo() {
        return url + "envinfo";
    }

    public static String playStream(Integer id) {
        return url + "play/" + id;
    }

    public static String playRenderer() { return url + "play_renderer"; }

    public static String pauseRenderer() { return url + "pause_renderer"; }

    public static String seek(int id, double percent) {
        String returnUrl = "";
        if(percent >= 0 && percent <= 1) {
            returnUrl = url + "seek/" + id + "/" + percent;
        }
        return returnUrl;
    }

    public static String stopAll() { return url + "stop_all"; }
}
