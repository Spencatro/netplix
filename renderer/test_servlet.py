__author__ = 'Spencer'

import vlc
import time

instance = vlc.Instance()

sout = '#rtp{dst=104.236.30.164,port=1234,sdp=rtsp://104.236.30.164:5005/stream_name.sdp}'

instance.vlm_add_broadcast("Test Media", r'/var/www/FlaskApp/netplix/server/DATA/bella+afp.mp4', sout, 0, None, True, False)
instance.vlm_play_media("Test Media")

paused = False

while(1):
	command = raw_input("p toggles playback")
	if "p" in command:
		if paused:
			instance.vlm_play_media("Test Media")
		else:
			instance.vlm_pause_media("Test Media")
