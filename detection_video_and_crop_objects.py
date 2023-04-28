import cv2
import json
import argparse
from src.VideoStream import VideoStream
from src.yolov8_detector import draw_objects_and_crop_async



def detection_video_and_crop_objects(save_dir, camera_urls):
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
                combined_img = draw_objects_and_crop_async(save_path=save_dir, img=resized_frame)
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
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_dir', type=str, required=True, help='Directory to save the cropped images')
    args = parser.parse_args()
    detection_video_and_crop_objects(args.save_dir,camera_urls)