package org.molabs.netplixcontroller.activities;

import android.app.Activity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageButton;
import android.widget.TextView;

import org.molabs.netplixcontroller.R;
import org.molabs.netplixcontroller.utilities.NetworkHelper;
import org.molabs.netplixcontroller.utilities.UrlBuilder;

public class NowPlaying extends Activity {
    private int movieID = -1;
    private String movieTitle;
    private String moviePreviewUrl;
    private boolean isPlaying = false;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.now_playing);

        Bundle extras = getIntent().getExtras();
        if (extras != null) {
            movieID = extras.getInt("movieID");
            movieTitle = extras.getString("movieTitle");


            TextView titleView = (TextView) findViewById(R.id.titleTextView);
            titleView.setText(movieTitle);
        }

        TextView tView = (TextView) findViewById(R.id.nowPlayingID);
        tView.setText("hello" + movieID);

        if(movieID >= 0) {
            String url = UrlBuilder.playStream(movieID);
            NetworkHelper.request(url);
        }
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_now_playing, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    public void playPauseMovie(View view) {
        //JsonObjectRequest(view, RequestTypes.play);
        if(!isPlaying && movieID >= 0) {
            String url = UrlBuilder.playRenderer();
            isPlaying = true;
            ImageButton playPauseImg = (ImageButton) findViewById(R.id.playPauseButton);
            playPauseImg.setImageResource(R.drawable.pause);
            System.out.println("Playing " + movieID);

            NetworkHelper.request(url);
        } else if (movieID >= 0) {
            //pause
            String url = UrlBuilder.pauseRenderer();
            isPlaying = false;
            ImageButton playPauseImg = (ImageButton) findViewById(R.id.playPauseButton);
            playPauseImg.setImageResource(R.drawable.play);
            System.out.println("Pausing " + movieID);

            NetworkHelper.request(url);
        }
    }

    public void stopMovie(View view) {
        String url = UrlBuilder.stopAll();
        System.out.println("Stop All");

        NetworkHelper.request(url);

        //quit this activity, go back to loop.
    }
}
