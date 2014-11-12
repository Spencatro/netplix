requirements.txt -- required python modules, openshift will automatically download and install the latest of each
wsgi/ -- folder that contains the actual app code


Manually getting a stream to work in VLC!
==================================

SERVER:
vlc -vvv /path/to/filename.mp4 --sout '#rtp{dst=SERVER_IP,port=1234,sdp=rtsp://SERVER_IP:5005/stream_name.sdp}'

CLIENT:
vlc rtsp://SERVER_IP:5005/stream_name.sdp