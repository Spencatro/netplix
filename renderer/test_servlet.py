__author__ = 'Spencer'

import vlc

instance = vlc.Instance()

player = instance.media_player_new()

sout = '#rtp{dst=SERVER_IP,port=1234,sdp=rtsp://SERVER_IP:5005/stream_name.sdp}'

player.vlm_add_broadcast("Test Media", r'/var/www/FlaskApp/netplix/server/DATA/bella+afp.mp4', sout, 0, None, True, False)
