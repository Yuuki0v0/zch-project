#!/bin/bash

set -eu

videofile="video/D13/20211025_150000_video.mp4"
process_width=1920
process_height=1080
shrink_rate=1  # 1920/1920
frame_rate=29
yolo_threshold=0.5

paramjson=$(cat << EOS
{
    \"shrink_rate\": ${shrink_rate},
    \"frame_rate\": ${frame_rate}
}
EOS
)

gst-launch-1.0 filesrc location=${videofile} \
    ! decodebin \
    ! videoconvert \
    ! videoscale \
    ! capsfilter caps="video/x-raw,width=${process_width},height=${process_height},frame_rate=${frame_rate/1},format=BGRx" \
    ! queue \
    ! gvadetect model=model/D13/frozen_darknet_yolov3_model.xml model-proc=model/D13/procd13_yolo-v3.json threshold=${yolo_threshold} inference-interval=12 \
    ! queue \
    ! gvatrack tracking-type=short-term \
    ! queue \
    ! gvawatermark \
    ! gvapython module=python/D13/display_yolo_image.py class=Main kwarg=\"$(echo ${paramjson})\" \
    ! queue \
    ! gvapython module=python/D13/working_status_detection.py class=Main kwarg=\"$(echo ${paramjson})\" \
    ! queue \
    ! videoconvert \
    ! xvimagesink sync=false

