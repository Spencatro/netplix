__author__ = 'Spencer'

import vlc

instance = vlc.Instance()

RENDERER_HTTP_PORT = 49678
RENDERER_STREAM_PORT = 49679

SERVER_STREAM_PORT = 49680
SERVER_IP = "104.236.30.164"

rtsp_uri = 'rtsp://'+str(SERVER_IP)+':'+str(RENDERER_STREAM_PORT)+'/'+str(id)+'.sdp'
sout = '#rtp{dst='+SERVER_IP+',port='+str(SERVER_STREAM_PORT)+',sdp='+rtsp_uri+'}'

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
