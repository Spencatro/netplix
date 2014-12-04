package org.molabs.netplixcontroller.activities;

import android.app.Activity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.SeekBar;
import android.widget.TextView;

import org.molabs.netplixcontroller.R;
import org.molabs.netplixcontroller.utilities.NetworkHelper;
import org.molabs.netplixcontroller.utilities.UrlBuilder;

public class NowPlaying extends Activity {
    private int movieID = -1;
    private String movieTitle;
    private String moviePreviewUrl;
    private String movieLength;
    private boolean isPlaying = false;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.now_playing);

        Bundle extras = getIntent().getExtras();
        if (extras != null) {
            movieID = extras.getInt("movieID");
            movieTitle = extras.getString("movieTitle");
            moviePreviewUrl = extras.getString("moviePreviewUrl");
            movieLength = extras.getString("movieLength");


            TextView titleView = (TextView) findViewById(R.id.titleTextView);
            titleView.setText(movieTitle);

            TextView timeView = (TextView) findViewById(R.id.totalTime);
            timeView.setText(movieLength);
        }

        TextView tView = (TextView) findViewById(R.id.nowPlayingID);
        ImageView previewImageView = (ImageView) findViewById((R.id.moviePreviewImage));
        //tView.setText("hello" + movieID);

        if(moviePreviewUrl != null) {
            try {
                NetworkHelper.getImage(moviePreviewUrl, (ImageView) findViewById(R.id.moviePreviewImage));
                //previewImageView.setImageBitmap(bmp);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        if(movieID >= 0) {
            String url = UrlBuilder.playStream(movieID);
            NetworkHelper.request(url);
        }

        SeekBar movieSlider = (SeekBar) findViewById(R.id.seekBar);

        movieSlider.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            int progressChanged = 0;

            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser){
                progressChanged = progress;
                String url = UrlBuilder.seek(movieID, (double) progress/100.0);
                NetworkHelper.request(url);
                //System.out.println("Seekbar " + progressChanged);
            }

            public void onStartTrackingTouch(SeekBar seekBar) {
                // TODO Auto-generated method stub
            }

            public void onStopTrackingTouch(SeekBar seekBar) {
                //Toast.makeText(SeekbarActivity.this, "seek bar progress:" + progressChanged,
                        //Toast.LENGTH_SHORT).show();
            }
        });
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

        finish();
        //quit this activity, go back to loop.
    }
}
