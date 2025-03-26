import cv2
from ultralytics import YOLO
import json

# Load a pretrained YOLO11n model
model = YOLO("best.pt")


cam = cv2.VideoCapture(0)

i = 0

def a():
    while 1:
        success, frame = cam.read()
    
        if (success == False):
            print("Cannot read frame")
            
            return
        
        key = cv2.waitKey(20) & 0xFF

        if (key == ord('q')):
            return
        
        #elif (key == 32): #space
        if 1:
            cv2.imwrite("neuro.jpg", frame)
            #i += 1
            
            results = model(frame)
        
            for result in results:
                boxes = result.boxes  # Boxes object for bounding box outputs
                masks = result.masks  # Masks object for segmentation masks outputs
                keypoints = result.keypoints  # Keypoints object for pose outputs
                probs = result.probs  # Probs object for classification outputs
                obb = result.obb  # Oriented boxes object for OBB outputs
                #result.show()  # display to screen
                result.save(filename="result.jpg")  # save to disk
                #print([probs])
                j = json.loads(result.to_json())
                if j: 
                    print(j[0]['class'])
                    #return j[0]['class']
                else:
                    print("ушлепка нет")
                    #return -1
        f = cv2.imread("result.jpg")
        cv2.imshow("neural", f)

        cv2.imshow("frame", frame)

a()

cam.release()
cv2.destroyAllWindows()
cv2.waitKey(10)
# Read an image using OpenCV
#source = cv2.imread("neuro.jpg")

# Run inference on the source
#results = model(source)  # list of Results objects

#for result in results:
#    probs = result.probs 
#    print(probs)
