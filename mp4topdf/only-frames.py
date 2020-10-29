# -*- coding: utf-8 -*-
import cv2
from skimage.metrics import structural_similarity as ssim
import os
import sys
from PIL import Image


def main():
    if len(sys.argv) != 2:
        print('error parsing args, required `python3 main.py video_file`')
        exit(0)

    file_name = sys.argv[1]
    try:
        capture = cv2.VideoCapture(file_name)
    except:
        print('no such file')
    escaped_file_name = file_name.replace(
        "\\", "").replace("/", "_").replace(".", "")
    good_frames = []
    files = []

    old_frame = None
    is_first_frame = True
    good_frame_counter = 0
    frame_counter = 0
    total = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    try:
        os.mkdir("./output")
    except:
        print("can't create directory ./output, maybe created?")

    while True:
        for i in range(15):
            retval, frame = capture.read()
            frame_counter = frame_counter + 1

        retval, frame = capture.read()
        if is_first_frame and retval:
            new_filename = "output/%s_frame%d.jpg" % (
                escaped_file_name, good_frame_counter)
            cv2.imwrite(new_filename, frame)
            files.append(new_filename)
            good_frame_counter = good_frame_counter + 1
            is_first_frame = False

        if retval == True:
            new_filename = "output/%s_frame%d.jpg" % (
                escaped_file_name, good_frame_counter)
            print("frame {}/{}".format(frame_counter, total))
            cv2.imwrite(new_filename, frame)
            good_frame_counter = good_frame_counter + 1
            frame_counter = frame_counter + 1
        else:
            print('end of video or file error')
            break

    capture.release()

if __name__ == "__main__":
    main()
