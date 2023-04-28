# Real Time Object Detection System
This system will read video streams in real-time from multiple camera sources, analyze video frames to detect objects and detected objects will be saved in folders.
For objection detection algorithm pretrained yolov8 model is used here. The model file was exported in ONNX format because then we can then leverage the benefits of using ONNX runtime. 
ONNX runtime optimizes and accelerates machine learning inferencing.
 
While running the system can handle if any camera goes offline unexpectedly. The whole system doesn't crash, only streams the camera which is online. If there is no camera active it terminates the program.


To capture multiple streams with OpenCV, we can use threading which can improve performance by alleviating the heavy I/O operations to a separate thread. Since accessing the webcam/IP/RTSP stream using `cv2.VideoCapture().read()` is a blocking operation, our main program is stuck until the frame is read from the camera device. If you have multiple streams, this latency will definitely be visible. To remedy this problem, we can use threading to spawn another thread to handle retrieving the frames using a queue in parallel instead of relying on a single thread to obtain the frames in sequential order. Threading allows frames to be continuously read without impacting the performance of our main program. 




## Installation
To use this system you need to install some necessary libraries that are mentioned in requirements.txt.
`pip install -r requirements.txt` 
For ONNX runtime installation 
If you have NVIDIA GPU:`pip install onnxruntime-gpu`
otherwise:`pip install onnxruntime`

You will also need to provide rtsp links for the cameras. In the file **camera_urls.json** you need to paste the rtsp links in a list.


## Usage 

**To quit the the video streaming press 'q'**

To display the raw video stream from both cameras in real-time, run the following command:
`python raw_video_stream.py'

Next I have implemented the object detection model on those captured frames. While working on this task I followed this [codebase](https://github.com/ibaiGorordo/ONNX-YOLOv8-Object-Detection). 
To display the video stream with bounding boxes around the detected objects, run the following command:
`python detection_video_stream.py`

Also added feature of saving detected object images from both camera streams respectively in local storage diretory 'Camera1' and 'Camera2'. Filename contains detected object name and current timestamp. I have implemented this feature using python asynchronous programming to make sure program concurrency while the images are being saved in directories. To use this feature also display the video detection you need to run the following command:
`python detection_video_and_crop_objects.py --save_dir "path_to_save_images/"`
