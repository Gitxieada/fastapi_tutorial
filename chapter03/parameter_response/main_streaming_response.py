#!/usr/bin/evn python
# -*- coding: utf-8 -*-

from fastapi import FastAPI

from starlette.responses import  HTMLResponse, RedirectResponse
from os import getcwd, path

app = FastAPI()


import cv2

PORTION_SIZE = 1024 * 1024
current_directory = getcwd() + "/"
CHUNK_SIZE = 1024 * 1024
from pathlib import Path

video_path = Path("big_buck_bunny.mp4")

def read_in_chunks():
    # 读取视频位置
    videoPath = "./big_buck_bunny.mp4"  # 读取视频路径
    # 打开视频
    cap = cv2.VideoCapture(videoPath)
    # 判断是否打开成功
    suc = cap.isOpened()  # 是否成功打开
    # 循环开始读取数据流
    while suc:
        # 读取数据帧
        suc, output_frame = cap.read()
        # 装在数据帧
        if output_frame is not None:
            # 把数据帧转化为图片
            _, encodedImage = cv2.imencode(".jpg", output_frame)
            # 设置播放帧的速度等待时间
            cv2.waitKey(1)
            # 迭代返回对应的数据帧
            yield (b'--frame\r\n' b'Content-Type: image/jpeg/\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
        else:
            break
    # 释放
    cap.release()


@app.get("/streamvideo")
def main():
    # 迭代的方式返回流数据
    return StreamingResponse(read_in_chunks(), media_type="multipart/x-mixed-replace;boundary=frame")

if __name__ == "__main__":
    import uvicorn
    import os
    app_modeel_name = os.path.basename(__file__).replace(".py", "")
    print(app_modeel_name)
    uvicorn.run(f"{app_modeel_name}:app", host='127.0.0.1', reload=True)
