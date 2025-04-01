## Project: Gesture Controlled Music
### Team: Jayden Okorougo, Anthony Hernandez, Gulliver Brower
### Date: March 25-March 31

#### Project Focus This Week
*This week, we finalized our project proposal and began setting up the foundation for our gesture-controlled music system. Our work focused mainly on hardware setup, researching hand tracking frameworks (MediaPipe vs. OpenCV) and MIDI/Reaper communication software, and running basic gesture detection on a Raspberry Pi.

## Tuesday, March 25 from 3:00pm - 6:00pm

#### 3:00-4:30pm
* Worked on setting things up and researching information on the software we need.
	* Created a dedicated project folder in the raspberry pi
	* Set up markdown file in GitHub
	* Created shared doc to share information 
	* Installed DAW (Reaper)
	* Set up camera

Some guiding questions we will need to answer as we work through this project:

**Core functionality:**
Need to decide on gesture types (open hand, fist, finger distance).
How many gestures will be mapped to different notes or commands?
Hand shapes or finger distance to control volume, pitch, other effects?
MIDI mapping; which gestures will correspond with which sounds or effects?

**Hardware information:**
*Camera*: Find a better camera to use or stick with USB camera in lab? Research camera resolution and frame rate to make sure they will meet our needs for gesture recognition.
*Speaker*: Which speaker will we use? JBL with bluetooth or USB connected speaker? test audio output from the Raspberry Pi before connecting to Reaper.
*Raspberry Pi*: Bring in 8GB Raspberry Pi, try to reduce lag as much as possible (comes with cooling fan and case as well)

Settled on using the USB webcam provided in lab and will bring in the 8GB memory Raspberry Pi and external speaker next lab session.

#### 4:30-6:00pm
Conducted research, read documentation, watched videos and planned out how we would implement the software (OpenCV vs MediaPipe) and the MIDI communication:

##### Software Setup:
**MediaPipe vs OpenCV?** OpenCV is more customizable but would have to write the hand tracking code from scratch. MediaPipe already has pre-trained hand tracking model. 

We can first use MediaPipe and test the model (and the camera), and then possibly combine it with OpenCV for customization and additional image processing, like adding filters, gesture classification, and visuals (bounding boxes, overlays). OpenCV can be used to process the hand keypoints detected by media pipe: could recognize gestures based on the positions of specific keypoints, or combining multiple frames to increase accuracy. 

Reference Video: https://www.youtube.com/watch?v=a99p_fAr6e4&list=PL0FM467k5KSyt5o3ro2fyQGt-6zRkHXRv

Notes from the video: 
* Need to install jupyter, opencv, mediapipe
* Helpful repo: https://github.com/kinivi/hand-gesture-recognition-mediapipe
* Hand recognition / multiple hands will slow down frame rate
* Press K (data collection mode) while app is running, then the index number (0-9) to take a snapshot and add it to the data that will be used to train the neural network (essentially saving the hand landmarks). Should do left and right hands, close/far, etc. to get better results; more data = better classification.
* Edit NUM_CLASSES in Jupyter Notebook (located in keypoint_classification) to match the number of signs/gestures you have
* To get more than 10 signs, edit python code (may need to add more neurons)

Will most likely limit the number of gestures used to make it less complex.

#### rtmidi

##### Ports/Outputs:
Get MIDI output channels with ``out = rtmidi.MidiOut()`` ``ports = out.get_ports()``. Then the ports can be opened with ``out.open_port(<port ID>)``.
 
##### Writing Signals:
Use ``with out`` to send messages to the open port.
Notes are defined as a 1x3 array of numbers ``[<Status|Channel>, <Pitch>, <Velocity>]``

**Status | Channel:** Should be written as Hex to make it more readable (0xNibbles).
The Nibbles are written as two numbers 0-F and represent the command to be sent(Status) and on what channel(Channel). A list of all commands can be found [Here](https://www.songstuff.com/recording/article/midi-message-format/#elementor-toc__heading-anchor-0)

**Pitch:** Notes are in semitones so octaves are separated by 12 int (60 is middle C).
**Velocity:** Velocity changes how 'hard' the key is pressed.

## Wednesday, March 26 from 12:45pm - 3:35pm
#### 12:45-2:00pm
Continued setting things up and researching; we decided to use a 8GB Raspberry Pi, and attempted to install all the necessary packages on that one, but ran into issues trying to install mediapipe.

We were able to install mediapipe-rpi4 using the command:
```bash
sudo apt update && sudo apt upgrade -y.
sudo apt install -y python3-pip python3-opencv libatlas-base-dev.
pip install mediapipe-rpi4.
```

But for some reason this was not sufficent enough to get the program to run. Eventually we switched back to the 4GB Raspberry Pi, and were able to install the following:
* Installed OpenCV, MediaPipe and TensorFlow Lite (the lite version is compatible with Raspberry Pi)
* Installed Reaper and rtmidi Python
* Installed JupyterNotebook and PyCharms IDE (using pi apps)
* Continued research on OpenCV and MediaPipe to troubleshoot the other pi.
```bash
pip install opencv-python
pip install mediapipe
pip install numpy tflite-runtime
sudo apt install jupyter-notebook
```
#### 2:00-3:35pm
Began working on coding basic hand recognition and gesture recognition
* We were able to install mediapipe on the 4GB Raspberry Pi device. 
* Ran into issues using the PyCharm IDE, and decided to go back to using Thonny IDE for simplicity. We then ran the code in the command line. We also needed to create a virtual environment in order for the code to run and function properly:
```bash
python3 -m venv myenv
source myenv/bin/activate
python HANDS.py
```
* Successfully wrote and ran some code to track hands using mediapipe on the 4GB Raspberry Pi.
* Did notice a frame rate drop when the camera is tracking hands, which would probably increase the more hands we track. Will need to keep this in mind when implementing.

Tested rtmidi on a personal laptop using the following code:
```python
import time  
import rtmidi  
  
midiout= rtmidi.MidiOut()  
available_ports = midiout.get_ports()  
if available_ports:  
    midiout.open_port(0)  
else:  
    midiout.open_virtual_port("My virtual output")  
#sends a note of pitch Note to Channel (written as a hex value)  
def SendNote(Note: int, Velocity: int = 100, Channel: int = 0x00, Duration: int = 1) -> None:  
    noteOn = [0x90, Note, Velocity]  
    noteOff = [0x80, Note, Velocity]  
    midiout.send_message(noteOn)  
    time.sleep(Duration)  
    midiout.send_message(noteOff)  
  
with midiout:  
    SendNote(60)  
del midiout
```

The above code works by creating a virtual MIDI channel with MIDIloopback and then sends the MIDI messages through the channel to be output through the laptops speakers.
### Wednesday, March 26 from 5:00pm - 9:00pm

* Continued working on and expanding the hand recognition to incorporate gestures. 
	* Mostly tried to figure out why mediapipe installation was not working on the 8GB Raspberry Pi, and eventually switched back over to the 4GB Raspberry Pi, which we were able to install mediapipe on earlier. 
	* Used and cloned the github repository,  https://github.com/kinivi/hand-gesture-recognition-mediapipe, which has a prebuilt model to detect hands and gestures, and after installing `mediapipe`, `numpy`, `matplotlib`, `tflite-runtime` and some other things, I was able to get the code to run. (note: forgot to take picture during this time, this picture is taken at a later session):

![IMG_2241](https://github.com/user-attachments/assets/6973e0b7-6419-47a5-8a30-d3e2020e45f4)

Full list of all installations (using the command `pip3 list`) on the 4GB Raspberry Pi 4:
```bash
**

Package               Version
--------------------- --------------
absl-py               2.2.1
attrs                 25.3.0
cffi                  1.17.1
contourpy             1.3.1
cycler                0.12.1
flatbuffers           20181003210633
fluidsynth            0.2
fonttools             4.56.0
jax                   0.5.3
jaxlib                0.5.3
kiwisolver            1.4.8
matplotlib            3.10.1
mediapipe             0.10.18
ml_dtypes             0.5.1
numpy                 1.26.4
opencv-contrib-python 4.11.0.86
opt_einsum            3.4.0
packaging             24.2
pathspec              0.12.1
pillow                11.1.0
pip                   25.0.1
protobuf              4.25.6
pycparser             2.22
pyfluidsynth          1.3.4
pyparsing             3.2.3
python-dateutil       2.9.0.post0
scikit_build_core     0.11.1
scipy                 1.15.2
sentencepiece         0.2.0
setuptools            66.1.1
six                   1.17.0
sounddevice           0.5.1
tflite-runtime        2.14.0
**
```


**app.py** (gesture tracking code)

```python
#!/usr/bin/env python

# -*- coding: utf-8 -*-

import csv
import copy
import argparse
import itertools
from collections import Counter
from collections import deque

import cv2 as cv
import numpy as np
import mediapipe as mp

from utils import CvFpsCalc
from model import KeyPointClassifier
from model import PointHistoryClassifier

def get_args():

parser = argparse.ArgumentParser()

parser.add_argument("--device", type=int, default=0)
parser.add_argument("--width", help='cap width', type=int, default=960)
parser.add_argument("--height", help='cap height', type=int, default=540)

parser.add_argument('--use_static_image_mode', action='store_true')
parser.add_argument("--min_detection_confidence",

help='min_detection_confidence',
type=float,
default=0.7)

parser.add_argument("--min_tracking_confidence",
help='min_tracking_confidence',
type=int,
default=0.5)

args = parser.parse_args()
return args


def main():

# Argument parsing #################################################################

args = get_args()

cap_device = args.device
cap_width = args.width
cap_height = args.height

use_static_image_mode = args.use_static_image_mode
min_detection_confidence = args.min_detection_confidence
min_tracking_confidence = args.min_tracking_confidence

use_brect = True

# Camera preparation ###############################################################

cap = cv.VideoCapture(cap_device)
cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

# Model load #############################################################
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
static_image_mode=use_static_image_mode,
max_num_hands=1,
min_detection_confidence=min_detection_confidence,
min_tracking_confidence=min_tracking_confidence,
)


keypoint_classifier = KeyPointClassifier()
point_history_classifier = PointHistoryClassifier()

# Read labels ###########################################################
with open('model/keypoint_classifier/keypoint_classifier_label.csv',
encoding='utf-8-sig') as f:
keypoint_classifier_labels = csv.reader(f)
keypoint_classifier_labels = [
row[0] for row in keypoint_classifier_labels
]

with open(
'model/point_history_classifier/point_history_classifier_label.csv',
encoding='utf-8-sig') as f:
point_history_classifier_labels = csv.reader(f)
point_history_classifier_labels = [
row[0] for row in point_history_classifier_labels
]


# FPS Measurement ########################################################
cvFpsCalc = CvFpsCalc(buffer_len=10)

# Coordinate history #################################################################
history_length = 16
point_history = deque(maxlen=history_length)

# Finger gesture history ################################################
finger_gesture_history = deque(maxlen=history_length)

# ########################################################################
mode = 0
while True:
fps = cvFpsCalc.get()

# Process Key (ESC: end) #################################################
key = cv.waitKey(10)
if key == 27: # ESC
break
number, mode = select_mode(key, mode)
 
# Camera capture #####################################################
ret, image = cap.read()
if not ret:
break
image = cv.flip(image, 1) # Mirror display
debug_image = copy.deepcopy(image)

# Detection implementation #############################################################
image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
image.flags.writeable = False
results = hands.process(image)
image.flags.writeable = True

# ####################################################################
if results.multi_hand_landmarks is not None:
for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
results.multi_handedness):

# Bounding box calculation
brect = calc_bounding_rect(debug_image, hand_landmarks)

# Landmark calculation
landmark_list = calc_landmark_list(debug_image, hand_landmarks)
 
# Conversion to relative coordinates / normalized coordinates
pre_processed_landmark_list = pre_process_landmark(
landmark_list)
pre_processed_point_history_list = pre_process_point_history(
debug_image, point_history)

# Write to the dataset file
logging_csv(number, mode, pre_processed_landmark_list,
pre_processed_point_history_list)

# Hand sign classification
hand_sign_id = keypoint_classifier(pre_processed_landmark_list)
if hand_sign_id == 2: # Point gesture
point_history.append(landmark_list[8])
else:
point_history.append([0, 0])
  
# Finger gesture classification
finger_gesture_id = 0
point_history_len = len(pre_processed_point_history_list)
if point_history_len == (history_length * 2):
finger_gesture_id = point_history_classifier(
pre_processed_point_history_list)

# Calculates the gesture IDs in the latest detection
finger_gesture_history.append(finger_gesture_id)
most_common_fg_id = Counter(
finger_gesture_history).most_common()

# Drawing part
debug_image = draw_bounding_rect(use_brect, debug_image, brect)
debug_image = draw_landmarks(debug_image, landmark_list)
debug_image = draw_info_text(
debug_image,
brect,
handedness,
keypoint_classifier_labels[hand_sign_id],
point_history_classifier_labels[most_common_fg_id[0][0]],
)

else:
point_history.append([0, 0])
debug_image = draw_point_history(debug_image, point_history)
debug_image = draw_info(debug_image, fps, mode, number)

# Screen reflection #############################################################

cv.imshow('Hand Gesture Recognition', debug_image)
cap.release()
cv.destroyAllWindows()

def select_mode(key, mode):

number = -1

if 48 <= key <= 57: # 0 ~ 9
number = key - 48

if key == 110: # n
mode = 0

if key == 107: # k
mode = 1

if key == 104: # h
mode = 2

return number, mode

def calc_bounding_rect(image, landmarks):
image_width, image_height = image.shape[1], image.shape[0]
landmark_array = np.empty((0, 2), int)

for _, landmark in enumerate(landmarks.landmark):
landmark_x = min(int(landmark.x * image_width), image_width - 1)
landmark_y = min(int(landmark.y * image_height), image_height - 1)

landmark_point = [np.array((landmark_x, landmark_y))]
landmark_array = np.append(landmark_array, landmark_point, axis=0)

x, y, w, h = cv.boundingRect(landmark_array)

return [x, y, x + w, y + h]


def calc_landmark_list(image, landmarks):
image_width, image_height = image.shape[1], image.shape[0]
landmark_point = []

# Keypoint
for _, landmark in enumerate(landmarks.landmark):
landmark_x = min(int(landmark.x * image_width), image_width - 1)
landmark_y = min(int(landmark.y * image_height), image_height - 1)

# landmark_z = landmark.z
landmark_point.append([landmark_x, landmark_y])
return landmark_point

def pre_process_landmark(landmark_list):
temp_landmark_list = copy.deepcopy(landmark_list)

# Convert to relative coordinates
base_x, base_y = 0, 0
for index, landmark_point in enumerate(temp_landmark_list):
if index == 0:
base_x, base_y = landmark_point[0], landmark_point[1]

temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

# Convert to a one-dimensional list
temp_landmark_list = list(
itertools.chain.from_iterable(temp_landmark_list))

# Normalization
max_value = max(list(map(abs, temp_landmark_list)))
def normalize_(n):
return n / max_value

temp_landmark_list = list(map(normalize_, temp_landmark_list))
return temp_landmark_list

def pre_process_point_history(image, point_history):
image_width, image_height = image.shape[1], image.shape[0]
temp_point_history = copy.deepcopy(point_history)

  

# Convert to relative coordinates

base_x, base_y = 0, 0
for index, point in enumerate(temp_point_history):
if index == 0:
base_x, base_y = point[0], point[1]

temp_point_history[index][0] = (temp_point_history[index][0] -
base_x) / image_width
temp_point_history[index][1] = (temp_point_history[index][1] -
base_y) / image_height

# Convert to a one-dimensional list
temp_point_history = list(
itertools.chain.from_iterable(temp_point_history))
return temp_point_history

def logging_csv(number, mode, landmark_list, point_history_list):
if mode == 0:
pass

if mode == 1 and (0 <= number <= 9):
csv_path = 'model/keypoint_classifier/keypoint.csv'

with open(csv_path, 'a', newline="") as f:
writer = csv.writer(f)
writer.writerow([number, *landmark_list])

if mode == 2 and (0 <= number <= 9):
csv_path = 'model/point_history_classifier/point_history.csv'

with open(csv_path, 'a', newline="") as f:
writer = csv.writer(f)
writer.writerow([number, *point_history_list])

return

# Key Points
for index, landmark in enumerate(landmark_point):
if index == 0: # 手首1
cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
-1)

...

return image

def draw_bounding_rect(use_brect, image, brect):

if use_brect:
# Outer rectangle
cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]),
(0, 0, 0), 1)

return image

def draw_info_text(image, brect, handedness, hand_sign_text,
finger_gesture_text):
cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[1] - 22),
(0, 0, 0), -1)

info_text = handedness.classification[0].label[0:]
if hand_sign_text != "":
info_text = info_text + ':' + hand_sign_text
cv.putText(image, info_text, (brect[0] + 5, brect[1] - 4),
cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv.LINE_AA)

if finger_gesture_text != "":
cv.putText(image, "Finger Gesture:" + finger_gesture_text, (10, 60),
cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 4, cv.LINE_AA)
cv.putText(image, "Finger Gesture:" + finger_gesture_text, (10, 60),
cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2,
cv.LINE_AA)  
return image

def draw_point_history(image, point_history):
for index, point in enumerate(point_history):
if point[0] != 0 and point[1] != 0:
cv.circle(image, (point[0], point[1]), 1 + int(index / 2),
(152, 251, 152), 2)
return image

def draw_info(image, fps, mode, number):
cv.putText(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX,
1.0, (0, 0, 0), 4, cv.LINE_AA)
cv.putText(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX,
1.0, (255, 255, 255), 2, cv.LINE_AA)
mode_string = ['Logging Key Point', 'Logging Point History']

if 1 <= mode <= 2:
cv.putText(image, "MODE:" + mode_string[mode - 1], (10, 90),
cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
cv.LINE_AA)

if 0 <= number <= 9:
cv.putText(image, "NUM:" + str(number), (10, 110),
cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
cv.LINE_AA)
return image

if __name__ == '__main__':

main()
```

### Friday, March 28 from 12:45pm - 3:45pm
Tested rtmidi code on raspberry pi.
* The code would send the MIDI messages through the virtual channel which could be picked up in reaper but the audio monitoring (realtime playback) in reaper was not working with the virtual MIDI channel.
* Got rtmidi to work without reaper and just outputting to a virtual MIDI channel that went directly to the speaker connected to the pi.
* Went on to research python libraries made for outputting MIDI messages directly to speakers(fluidsynth and tinysoundfont) These libraries are python wrappers for existing C/C++ libraries. The libraries were very similar to rtmidi but did not need to open a midi port.

### Monday, March 31 from 12:00pm - 4:00pm

Attempted to figure out and troubleshoot why installation of mediapipe was failing on the 8GB memory Raspberry Pi, as well as test fluidsynth and tinysoundfont libraries for MIDI communication. 
* Figured out that an older version of python was running on it (python 3.9), and attempted to install a newer version, python3.13. 
* Installation took up a majority of class time for some reason, and once downloaded we realized that some libraries and installations would not work on that new of a version, so we had to downgrade to python3.10 and redownload.
* In the process, most of our installations got erased from the device, so we will have to redownload them if we want to continue using it. 
* Downgrading to python3.10 still did not let us install the libraries. we will have to try again with rtmidi or downgrade back to python3.9

### Challenges Faced This Week
- MediaPipe installation issues on 8GB Raspberry Pi caused us to switch to the 4GB version temporarily.
- MIDI output to Reaper was inconsistent — MIDI messages worked through loopback but audio monitoring in Reaper did not.
- Python version upgrades broke previous installations, forcing us to reinstall dependencies.

### Next Steps
- Get Reaper working with Raspberry Pi MIDI output or find a workaround using FluidSynth or tinysoundfont.
- Finalize hand gestures and label training data using MediaPipe + Jupyter Notebook.
- Map recognized gestures to corresponding MIDI notes and test real-time playback.
- Continue working on integrating gesture detection with music output for a live demo.
