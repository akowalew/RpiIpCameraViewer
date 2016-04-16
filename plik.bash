#!/bin/bash
screen -dmS top_left sh -c 'omxplayer "rtsp://192.168.0.20:554/user=admin&password=&channel=1&stream=0.sdp?real_stream--rtp-caching=100" --live'
