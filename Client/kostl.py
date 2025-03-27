from ultralytics import YOLO
import json
from flask import Flask
import cv2 as cv

# Load a pretrained YOLO11n model
model = YOLO("best.pt")

app = Flask(__name__)

cam = cv.VideoCapture(0)

def getRes():
    _, frame = cam.read()
    cv.imwrite("savedFrame.png", frame)
    res = model(frame)[0]
    res.save(filename="result.jpg")
    j = json.loads(res.to_json())
    if not j: return '-1'
    if j[0]['confidence'] < .8 and j[0]['class'] == 0: return '-1'
    return str(j[0]['class'])

@app.route("/")
def ind():
    return getRes()

app.run("0.0.0.0", 24680)