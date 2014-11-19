/**
 * Created by Morgan on 11/19/2014.
 */
package org.molabs.netplixcontroller.utilities;

import android.app.Activity;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;

import org.molabs.netplixcontroller.R;
import org.molabs.netplixcontroller.models.Media;

import java.util.List;

public class CustomListAdapter extends BaseAdapter {
    private Activity activity;
    private LayoutInflater inflater;
    private List<Media> mediaItems;

    public CustomListAdapter(Activity activity, List<Media> mediaItems) {
        this.activity = activity;
        this.mediaItems = mediaItems;
    }

    @Override
    public int getCount() {
        return mediaItems.size();
    }

    @Override
    public Object getItem(int location) {
        return mediaItems.get(location);
    }

    @Override
    public long getItemId(int position) {
        return mediaItems.get(position).getId();
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {

        if (inflater == null)
            inflater = (LayoutInflater) activity
                    .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        if (convertView == null)
            convertView = inflater.inflate(R.layout.list_row, null);

        TextView title = (TextView) convertView.findViewById(R.id.title);
        TextView actors = (TextView) convertView.findViewById(R.id.actors);

        // getting movie data for the row
        Media m = mediaItems.get(position);

        // title
        title.setText(m.getTitle());

        // actors
        String actorString = "";
        for (String str : m.getActors()) {
            actorString += str + ", ";
        }
        actorString = actorString.length() > 0 ? actorString.substring(0,
                actorString.length() - 2) : actorString;
        actors.setText(actorString);

        return convertView;
    }

    public void resetData( List<Media> mediaItems) {
        this.mediaItems = mediaItems;
    }
}
