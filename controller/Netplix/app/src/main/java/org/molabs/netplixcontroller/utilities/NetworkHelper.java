/**
 * Created by Morgan on 12/4/2014.
 */
package org.molabs.netplixcontroller.utilities;

import android.graphics.Bitmap;
import android.widget.ImageView;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.ImageRequest;
import com.android.volley.toolbox.StringRequest;

import org.molabs.netplixcontroller.R;
import org.molabs.netplixcontroller.app.AppController;

public class NetworkHelper {

    public static void request(String url) {
        //RequestQueue queue = Volley.newRequestQueue(this);

        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        System.out.println(response);
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                //mTextView.setText("That didn't work!");
                System.out.println("Error on request");
            }
        });
        AppController.getInstance().addToRequestQueue(stringRequest);
    }

    public static void getImage(String url, final ImageView mImageView) {
        ImageRequest request = new ImageRequest(url, new Response.Listener<Bitmap>() {
            @Override
            public void onResponse(Bitmap bitmap) {
                mImageView.setImageBitmap(bitmap);
            }
        }, 0, 0, null,
        new Response.ErrorListener() {
            public void onErrorResponse(VolleyError error) {
                mImageView.setImageResource(R.drawable.movie);
            }
        });

        AppController.getInstance().addToRequestQueue(request);
    }
}
