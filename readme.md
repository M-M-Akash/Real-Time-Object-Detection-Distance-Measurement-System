# Real Time Object Detection System with Multiple Cameras
This project aims to build a real-time object detection system that can capture video streams from multiple cameras using RTSP protocol, analyze the video frames to detect objects, and save detected object images in a local storage directory.

For object detection algorithm, I have used the pre-trained YOLOv8 model in this project. The model file was exported in ONNX format because we can then leverage the benefits of using ONNX runtime. ONNX runtime optimizes and accelerates machine learning inferencing. 
ONNX runtime optimizes and accelerates machine learning inferencing.
 
While running the system can handle if any camera goes offline unexpectedly. At that time the whole system doesn't crash, only streams the camera which is online. If there is no active camera available it terminates the program.

## Development Pipeline 
The development pipeline consists of the following tasks:

- Capturing video frames from multiple cameras using RTSP protocol in an efficient way with lower CPU usage and displaying the streaming feed.
Implementing an object detection algorithm using a pre-trained model such as YOLO.

- Integrating the object detection algorithm with the streaming script to detect objects in real-time from multiple camera sources and display the video stream with bounding boxes around the detected objects.

- Adding a feature of saving detected object images in a local storage directory. Filename should contain detected object name and current timestamp. This feature is implemented using python asynchronous programming to make sure program concurrency.
### How the distance measurement works?
This formula is used to determine the distance 

``` python
    distancei = (2 x 3.14 x 180) ÷ (w + h x 360) x 1000 + 3
```
For measuring distance, at first, we have to understand how a camera sees an object. 
<p align="center">
<img src="http://muizzer07.pythonanywhere.com/media/files/sketch_N6c1Tb7.png">
</p>

You can relate this image to the white dog picture where the dog was localized. Again we will get four numbers in the bounding box which is (x0,y0,width,height). Here x0,y0 is used to tiled or adjust the bounding box. Width and Height these two variables are used in the formula of measuring the object and describing the detail of the detected object/objects. Width and Height will vary depending on the distance of the object from the camera.

As we know, an image goes refracted when it goes through a lens because the ray of light can also enter the lens, whereas, in the case of a mirror, the light can be reflected. That's why we get an exact reflection of the image. But in the case of the lens image gets a little stretched. The following image illustrates how the image and the corresponding angles look when it enters through a lens.
<p align="center">
 <img src="http://muizzer07.pythonanywhere.com/media/files/lens-object-internal-scenario_cg2o8yA.png">
</p>
If we see there are three variables named:

- do (Distance of object from the lens)
- di (Distance of the refracted image from the convex lens)
- f (focal length or focal distance)

So the green line <b>"do"</b> represents the actual distance of the object from the convex length. And <b>"di"</b> gives a sense of what the actual image looks like. Now if we consider a triangle on the left side of the image(new refracted image) with base <b> "do" </b> and draw an opposite triangle similar to the left side one. So the new base of the opposite triangle will also be done with the same perpendicular distance. Now if we compare the two triangles from the right side, we will see <b> "do"</b> and <b> "di" </b> is parallel, and the angle creates on each side of both triangles are opposite to each other. From this, we can infer that both the triangles on the right side are also similar. Now, as they are similar, the ratio of the corresponding sides will be also similar. So do/di = A/B. Again if we compare two triangles on the right side of the image where opposite angles are equal and one angle of both the triangles are right angle (90°) (dark blue area). So A:B is both hypotenuses of a similar triangle where both triangles has a right angle. So the new equation can be defined as :
<p align="center">
 <img src="http://muizzer07.pythonanywhere.com/media/files/Eq1_SycSI35.gif">
</p>
Now, if we derive from that equation we will find:-
<p align="center"> 
 <img src="http://muizzer07.pythonanywhere.com/media/files/Eqn2_jRdlvju.gif">
</p>
And eventually will come to at 
<p align="center">
<img src="http://muizzer07.pythonanywhere.com/media/files/Eqn3.gif">
</p>
Where f is the focal length or also called the arc length by using the following formula 
<p align="center">
<img src="http://muizzer07.pythonanywhere.com/media/files/Eqn4.gif">
</p>
we will get our final result in "inches" from this formula of distance. 

``` python
    distancei = (2 x 3.14 x 180) ÷ (w + h x 360) x 1000 + 3
```

## Installation
To use this system you need to install some necessary libraries that are mentioned in requirements.txt.
```python

pip install -r requirements.txt

```
For ONNX runtime installation 

**If you have NVIDIA GPU:**
```python

pip install onnxruntime-gpu

```
**Otherwise:**
```python

pip install onnxruntime

```

**You will also need to provide rtsp links for the cameras.**
In the file `camera_urls.json` you need to paste the rtsp links in a list.
```powershell

akash@akash:~$ cat camera_urls.json
["rtsp://192.168.0.100:8080/h264_pcm.sdp","rtsp://192.168.0.103:8080/h264_pcm.sdp"]

```


## Usage 
First we need to capture frames from real-time cameras. 
To capture multiple streams with OpenCV, we can use threading which can improve performance by alleviating the heavy I/O operations to a separate thread. Since accessing the webcam/IP/RTSP stream using `cv2.VideoCapture().read()` is a blocking operation, our main program is stuck until the frame is read from the camera device. If you have multiple streams, this latency will definitely be visible. To remedy this problem, we can use threading to spawn another thread to handle retrieving the frames using a queue in parallel instead of relying on a single thread to obtain the frames in sequential order. Threading allows frames to be continuously read without impacting the performance of our main program. 

**To quit the the video streaming press 'q'**

To display the raw video stream from both cameras in real-time, run the following command:
```powershell

akash@akash:~$ python raw_video_stream.py

```

Next I have implemented the object detection model on those captured frames. While working on this task I followed this [repository](https://github.com/ibaiGorordo/ONNX-YOLOv8-Object-Detection). 

On this repository readme file you will see how to export pretrained yolov8 model in .ONNX format. While exporting the the model you also need to define the image(width,height). 

**Note: You should resize the frames before inferencing on model. It might affect the accuracy of the model if the input image has a different aspect ratio compared to the input size of the model.**

To display the video stream with bounding boxes around the detected objects, run the following command:
```powershell

akash@akash:~$ python detection_video_stream.py

```

Also added feature of saving detected object images from all camera streams in providing argument directory. By cropping the objects following their bounding box values. Filename contains detected object name and current timestamp. I have implemented this feature using python asynchronous programming to make sure program the cpu unit doesn't sit idle when saving images take time.

To use this feature also display the video detection you need to run the following command:
```powershell

akash@akash:~$ python detection_video_and_crop_objects.py --save_dir "path_to_save_images/"

```

## References
M. A. Khan, P. Paul, M. Rashid, M. Hossain and M. A. R. Ahad, "An AI-Based Visual Aid With Integrated Reading Assistant for the Completely Blind," in IEEE Transactions on Human-Machine Systems.
doi: 10.1109/THMS.2020.3027534
- [Real-time Distance Measurement Using Single Image](http://emaraic.com/blog/distance-measurement)
