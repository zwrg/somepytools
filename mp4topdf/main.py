# -*- coding: utf-8 -*-
import cv2
from skimage.metrics import structural_similarity as ssim
import os
import sys
from PIL import Image


def main():
    if len(sys.argv) != 4:
        print('error parsing args, required `python3 main.py video_file pdf_filename max_score`')
        exit(0)

    file_name = sys.argv[1]
    pdf_filename = sys.argv[2]
    max_score = sys.argv[3]
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

    try:
        os.mkdir("./output")
    except:
        print("can't create directory ./output, maybe created?")

    while True:

        retval, frame = capture.read()
        if is_first_frame and retval:
            new_filename = "output/%s_frame%d.jpg" % (
                escaped_file_name, good_frame_counter)
            cv2.imwrite(new_filename, frame)
            files.append(new_filename)
            good_frame_counter = good_frame_counter + 1
            is_first_frame = False

        if retval == True:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if old_frame is not None:
                gray_old_frame = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
            if old_frame is not None:
                (score, diff) = ssim(gray_frame, gray_old_frame, full=True)
                print("{} frame: {}, ssim: {}".format(
                    escaped_file_name, frame_counter, score))
                if(score < max_score):
                    diff = (diff * 255).astype("uint8")
                    good_frames.append(frame)
                    new_filename = "output/%s_frame%d.jpg" % (
                        escaped_file_name, good_frame_counter)
                    files.append(new_filename)
                    print("ssim < 0.98, saving frame to file: %s" %
                          new_filename)
                    cv2.imwrite(new_filename, frame)
                    good_frame_counter = good_frame_counter + 1
            old_frame = frame
            frame_counter = frame_counter + 1
        else:
            print('end of video or file error')
            break

    capture.release()

    images_to_pdf = []

    for image in files:
        images_to_pdf.append(Image.open(r'{}'.format(image)))

    for image in images_to_pdf:
        image = image.convert('RGB')

    try:
        if len(images_to_pdf) > 0:
            print('saving to %s' % pdf_filename)
            images_to_pdf[0].save(r'output/%s' % pdf_filename,
                                  save_all=True, append_images=images_to_pdf[1:])
    except:
        print('error during pdf saving')


if __name__ == "__main__":
    main()
