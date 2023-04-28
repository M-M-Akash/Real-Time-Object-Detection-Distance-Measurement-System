import cv2
import json
from src.VideoStream import VideoStream
from src.yolov8_detector import draw_detect_objects_async

def detection_video_stream(camera_urls):
    # Create VideoStream instances for each camera
    cameras = [VideoStream(url) for url in camera_urls]

    # Start reading frames from each camera
    for camera in cameras:
        camera.start()

    # Display frames from each camera in separate windows
    while cameras:
        for i, camera in enumerate(cameras):
            frame = camera.read()
            if frame is not None:
                # resize frame to match the input size of the model
                resized_frame = cv2.resize(frame, (640,480), interpolation= cv2.INTER_LINEAR)
                combined_img = draw_detect_objects_async(resized_frame)
                cv2.imshow(f"Camera {i+1}", combined_img)
            else:
                print(f"Camera {cameras.index(camera)+1} disconnected")
                camera.stop()
                camera.exit()
                cv2.destroyAllWindows()
                cameras.remove(camera)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    # Stop reading frames from each camera
    for camera in cameras:
        camera.stop()
        camera.exit()

    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    
    with open('camera_urls.json', 'r') as f:
        camera_urls = json.load(f)
    detection_video_stream(camera_urls)