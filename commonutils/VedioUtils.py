import cv2
def get_frame_count(input_video):
    # 使用 OpenCV 库读取视频文件
    cap = cv2.VideoCapture(input_video)
    # 获取帧数
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # 释放视频对象
    cap.release()
    return frame_count
