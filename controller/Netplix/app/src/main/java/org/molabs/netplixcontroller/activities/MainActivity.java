package org.molabs.netplixcontroller.activities;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Context;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.AdapterView;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.VolleyLog;
import com.android.volley.toolbox.JsonObjectRequest;

import org.json.JSONArray;
import org.json.JSONObject;
import org.molabs.netplixcontroller.R;
import org.molabs.netplixcontroller.app.AppController;
import org.molabs.netplixcontroller.models.Media;
import org.molabs.netplixcontroller.utilities.CustomListAdapter;
import org.molabs.netplixcontroller.utilities.UrlBuilder;

import java.util.ArrayList;
import java.util.List;


public class MainActivity extends Activity {
    // Log tag
    private static final String TAG = MainActivity.class.getSimpleName();

    // Movies json url
    private String url;
    //private static final String url = "http://np.spencer-hawkins.com/search/j";
    private ProgressDialog pDialog;
    private List<Media> mediaList = new ArrayList<Media>();
    private ListView listView;
    private CustomListAdapter adapter;
    private int selectedMedia;

    public enum RequestTypes { search, play }

    // Create a message handling object as an anonymous class.
    private AdapterView.OnItemClickListener mMessageClickedHandler = new AdapterView.OnItemClickListener() {
        public void onItemClick(AdapterView parent, View v, int position, long id) {
            hideKeyboard();
            LinearLayout ll = (LinearLayout)findViewById(R.id.mediaControl);

            TextView tView = (TextView) findViewById(R.id.movieTitle);
            tView.setText(mediaList.get(position).toString());

            ll.setVisibility(View.VISIBLE);

            selectedMedia = (int)id;
        }
    };
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        listView = (ListView) findViewById(R.id.list);
        adapter = new CustomListAdapter(this, mediaList);
        listView.setAdapter(adapter);

        listView.setOnItemClickListener(mMessageClickedHandler);
    }

    public void JsonObjectRequest(View view, final RequestTypes requestType) {
        switch(requestType) {
            case search:
                String query = ((EditText)findViewById(R.id.searchText)).getText().toString();
                url = UrlBuilder.search(query);
                break;
            case play:
                url = UrlBuilder.play(selectedMedia);
                break;
        }

        pDialog = new ProgressDialog(this);
        // Showing progress dialog before making http request
        pDialog.setMessage("Loading...");
        pDialog.show();
        JsonObjectRequest mediaRequest = new JsonObjectRequest(Request.Method.GET, url, null, new Response.Listener<JSONObject>() {

            @Override
            public void onResponse(JSONObject response) {
                Log.d(TAG, response.toString());
                hidePDialog();

                switch(requestType) {
                    case search:
                        parseSearchResponse(response);
                        break;
                    case play:
                        parsePlayResponse(response);
                        break;
                }
            }
        }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                VolleyLog.d(TAG, "Error: " + error.getMessage());
                hidePDialog();
            }
        });

        // Adding request to request queue
        AppController.getInstance().addToRequestQueue(mediaRequest);
    }

    public void parseSearchResponse (JSONObject response) {
        Media media;
        resetData();

        try {
            JSONArray jsonArray = response.getJSONArray("results");
            for (int i = 0; i < jsonArray.length(); i++) {
                try {
                    JSONObject jsObject = jsonArray.getJSONObject(i);
                    media = new Media();
                    media.setTitle(jsObject.getString("title"));
                    media.setId(Integer.parseInt(jsObject.getString("id")));
                    media.setFilePath(jsObject.getString("filepath"));

                    JSONArray actorsArry = jsObject.getJSONArray("actors");
                    ArrayList<String> actors = new ArrayList<String>();
                    for (int j = 0; j < actorsArry.length(); j++) {
                        actors.add((String) actorsArry.get(j));
                    }
                    media.setActors(actors);

                    mediaList.add(media);
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        // notifying list adapter about data changes
        // so that it renders the list view with updated data
        adapter.notifyDataSetChanged();
    }

    public void parsePlayResponse(JSONObject response) {
        //Log.d(Tag, response);
        System.out.println("parsePlayResponse");
    }

    public void search(View view) {
        JsonObjectRequest(view, RequestTypes.search);
    }

    public void playMovie(View view) {
        JsonObjectRequest(view, RequestTypes.play);
    }

    /*public void search(View view, final RequestTypes requestType) {
        String query = ((EditText)findViewById(R.id.searchText)).getText().toString();
        url = UrlBuilder.search(query);

        pDialog = new ProgressDialog(this);
        // Showing progress dialog before making http request
        pDialog.setMessage("Loading...");
        pDialog.show();

        // changing action bar color
        getActionBar().setBackgroundDrawable(
                new ColorDrawable(Color.parseColor("#1b1b1b")));

        // Creating volley request obj

        JsonObjectRequest mediaRequest = new JsonObjectRequest(Request.Method.GET, url, null, new Response.Listener<JSONObject>() {

            @Override
            public void onResponse(JSONObject response) {
                Log.d(TAG, response.toString());
                hidePDialog();
                Media media;
                resetData();

                try {
                    JSONArray jsonArray = response.getJSONArray("results");
                    for (int i = 0; i < jsonArray.length(); i++) {
                        try {
                            JSONObject jsObject = jsonArray.getJSONObject(i);
                            media = new Media();
                            media.setTitle(jsObject.getString("title"));
                            media.setId(Integer.parseInt(jsObject.getString("id")));
                            media.setFilePath(jsObject.getString("filepath"));

                            JSONArray actorsArry = jsObject.getJSONArray("actors");
                            ArrayList<String> actors = new ArrayList<String>();
                            for (int j = 0; j < actorsArry.length(); j++) {
                                actors.add((String) actorsArry.get(j));
                            }
                            media.setActors(actors);

                            mediaList.add(media);
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }

                // notifying list adapter about data changes
                // so that it renders the list view with updated data
                adapter.notifyDataSetChanged();
            }
        }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                VolleyLog.d(TAG, "Error: " + error.getMessage());
                hidePDialog();
            }
        });

        // Adding request to request queue
        AppController.getInstance().addToRequestQueue(mediaRequest);
    }

    private void play(View view) {
        url = UrlBuilder.play(selectedMedia);

        StringRequest stringRequest = new StringRequest(Request.Method.GET, url, new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                // Display the first 500 characters of the response string.
                //mTextView.setText("Response is: "+ response.substring(0,500));
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                //mTextView.setText("That didn't work!");
            }
        });
        // Add the request to the RequestQueue.
        AppController.getInstance().addToRequestQueue(stringRequest);
    }*/

    private void hidePDialog() {
        if (pDialog != null) {
            pDialog.dismiss();
            pDialog = null;
        }
    }

    private void resetData() {
        mediaList = new ArrayList<Media>();
        adapter.resetData(mediaList);
    }

    private void hideKeyboard() {
        InputMethodManager inputManager = (InputMethodManager) this.getSystemService(Context.INPUT_METHOD_SERVICE);

        // check if no view has focus:
        View view = this.getCurrentFocus();
        if (view != null) {
            inputManager.hideSoftInputFromWindow(view.getWindowToken(), InputMethodManager.HIDE_NOT_ALWAYS);
        }
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        hidePDialog();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }
}
