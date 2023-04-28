import cv2
from yolov8 import YOLOv8
from datetime import datetime
import os
import asyncio

model_path = "models/yolov8m.onnx"
yolov8_detector = YOLOv8(model_path, conf_thres=0.5, iou_thres=0.5)

async def detect_objects(img):
    """This function will detect objects in frame and 
    draw bounding boxes around the objects

    Args:
        img (_type_): _camera frame_

    Returns:
        _image_: _the bounded box image_
    """
    # Detect Objects
    boxes, scores, class_ids = yolov8_detector(img)

    # to_thread() allows the function to run in separate thread
    # thus allows other code to run parallel don't block other executions
    combined_img = await asyncio.to_thread(yolov8_detector.draw_detections, img)
    return combined_img


async def draw_objects_and_crop(save_path, img):
    """This function will detect the objects, draw bounding boxes 
    and crop the detected objects

    Args:
        save_path (_string_): _the directory path the images will be saved_
        img (_type_): _camera frame_

    Returns:
        _image_: _image with bounding boxes_
    """
    
    boxes, scores, class_ids = yolov8_detector(img)
    combined_img = await asyncio.to_thread(yolov8_detector.draw_detections, img)
    labels, objects = await asyncio.to_thread(yolov8_detector.crop_objects, img)
        # the await keyword is used to wait for the function to complete 
        # and allow other codes to run in parallel 
    await save_objects(save_path, labels, objects)
    return combined_img

async def save_objects(save_path, labels, objects):
    """_This function will save the the detected objects cropped images 
    on the providing directory_

    Args:
        save_path (_type_): _the path where the images will be saved
        labels (_type_): _the detected objects class names_
        objects (_type_): _the detected objects cropped images_
    """

    for label, object in zip(labels, objects):

        now = datetime.now()
        current_time = now.strftime("_%d_%m_%H_%M_")
        # filename contains the detected object name and current timestamp
        filename = '%s.png' %(label+current_time)
        await asyncio.to_thread(cv2.imwrite,os.path.join(save_path,filename), object)
        
        
def draw_objects_and_crop_async(save_path, img):
    result = asyncio.run(draw_objects_and_crop(save_path, img))
    return result

def draw_detect_objects_async(img):
    result = asyncio.run(detect_objects(img))
    return result