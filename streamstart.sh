sudo modprobe bcm2835-v4l2

export STREAMER_PATH=/home/pi/mjpg-streamer/mjpg-streamer-experimental
export LD_LIBRARY_PATH=$STREAMER_PATH
$STREAMER_PATH/mjpg_streamer -i "input_uvc.so -d /dev/video0 -r 640x480 -f 5 -n" -o "output_http.so -p 8080 -w $STREAMER_PATH/www"
