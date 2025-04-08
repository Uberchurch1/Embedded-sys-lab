## Project: Gesture Controlled Music
### Team: Jayden Okorougo, Anthony Hernandez, Gulliver Brower
### Date: April 2 - April 6

#### Project Focus This Week
*This week, our primary goal was to begin integrating the MIDI communication system with our gesture recognition code. After setting up the basic hand tracking and MIDI testing in the previous week, we shifted our focus toward linking specific gestures to musical outputs. This included experimenting with Python MIDI libraries (rtmidi), writing functions for various MIDI messages (Note On, Note Off, Control Change, Pitch Bend), and modifying our existing gesture detection code to trigger sounds based on recognized hand signs.*

## Wednesday, April 2 from 12:45pm - 3:35pm

#### 12:45-1:45pm
* Continued working on gesture recognition and fixing installations.
	* Collected data for new "peace sign" symbol that we need to input into the model for it to recognize
	* We decided to go with the original raspberry pi for now, as it has most of the correct installs and is not "broken"; we realized that trying to install a new python version directly into the system ended up erasing/breaking most of our previous installs. We probably should have installed it in a virtual environment instead, but for now the 4GB pi works just fine.
	* Installed rtmidi for MIDI communication library

#### 1:45-3:35pm
Continued conducting research and read documentation on how MIDI communication works; the different ports, effects, and syntax. Useful references and readings:
* https://midi.org/expanded-midi-1-0-messages-list
* https://learn.sparkfun.com/tutorials/midi-tutorial/all

MIDI Status codes: [http://www.opensound.com/pguide/midi/midi5.html](http://www.opensound.com/pguide/midi/midi5.html)

<img src="https://github.com/user-attachments/assets/c0fe040e-7e5d-4781-9908-3aa07fe64246" alt="pic1" width="800"/>

Also worked on integrating the gesture recognition code with MIDI communication.
* Our initial plan was to first write code to play a single note from a single gesture, and then work on playing around with MIDI and its effects
* There is a section of the code that outputs the "detection"; each gesture has a number, and we are able to write code that basically says "if the model recognizes gesture 1, play this sound"; we were able to successfully do this
* There are two problems that we need to fix with this implementation before we go further:
	* 1. The note plays for a certain duration, but no matter how long the duration is set (i.e. set to the max), the note will eventually fall off until there is no sound. We need to find a way for the note to last until the "stop" gesture is shown and detected.
	* 2. The code only works for a single note to play, and once the note is stopped we cannot play the note again.

Midifunc.py to test speaker output
```python
import time
import rtmidi

midiout= rtmidi.MidiOut()
available_ports = midiout.get_ports()
if available_ports:
#     print(available_ports)
#     port = input("Choose a port number")
#     midiout.open_port(int(port))
#     print(f"Opened port {port}")
    midiout.open_port(1)
else:
    print("No port found")
    midiout.open_virtual_port("My virtual output")
#sends a note of pitch Note to Channel (written as a hex value)
def SendNote(Note: int, Velocity: int = 100, Channel: int = 0x00, Duration: int = 1) -> None:
    noteOn = [0x90 | Channel, Note, Velocity]
    noteOff = [0x80 | Channel, Note, Velocity]
    midiout.send_message(noteOn)
    time.sleep(Duration)
    midiout.send_message(noteOff)
    
def sendControlChange(cc, value, channel = 0x00):
    midiout.send_message([0xb0 | channel, cc, value])
    
def sendPB(value, channel = 0x00):
    lsb = value & 0x7F
    msb = (value >> 7) & 0x7F
    midiout.send_message([0xE0 | channel, lsb, msb])
    
start = 8192
end = 16383
step = 128
delay = 0.01




def StartNote(Note: int, Velocity: int = 127, Channel: int = 0x00) -> None:
    with midiout:
        noteOn = [0x90 | Channel, Note, Velocity]
        midiout.send_message(noteOn)

def StopNote(Note: int, Velocity: int = 100, Channel: int = 0x00) -> None:
    with midiout:
        noteOff = [0x80 | Channel, Note, Velocity]
        midiout.send_message(noteOff)

def DelMIDI():
    return None
    del midiout

 with midiout:
     sendControlChange(64, 127)
     SendNote(67)
     
     for bend in range(start, end + 1, step):
         sendPB(bend)
         time.sleep(delay)
     StartNote(60)
     time.sleep(0.5)
     StartNote(72)
     time.sleep(0.5)
     StartNote(84)
     time.sleep(1)
     StopNote(60)
     StopNote(72)
     StopNote(84)
     time.sleep(1)
     
 del midiout

```

Updated app.py section with MIDI communication
```python
import MidiFunc as mf

class MIDImsg():
    def __init__(self, Note, Channel):
        self.note = Note
        self.chan = Channel
        self.status = False
    
    def NoteOn(self):
        if self.status == False:
            mf.StartNote(self.note)
            self.status = True
            return 0
        else:
            return 1
        
    def NoteOff(self):
        if self.status == True:
            self.status = False
            mf.StopNote(self.note)
            return 0
        else:
            return 1
        
    def ChangeNote(self, Note):
        self.NoteOff()
        self.note = Note
        self.NoteOn()
        
    def DelMIDI(self):
        mf.DelMIDI()

```

## Wednesday, April 2 from 5:00pm - 8:00pm

Continued research on MIDI communication to see the different effects we can do that will be useful to us. Essentially, there are only 8 main types of MIDI messages, but they are pretty versatile and allow for a wide range of expression. Reference: https://henrybalme.substack.com/p/all-8-midi-messages-explained?r=3qbno3&utm_campaign=post&utm_medium=web&triedRedirect=true
- **Note On/Note Off** – triggers sounds (for example, piano keys).
- **Control Change** – can control parameters like volume, pan, sustain, etc.
- **Pitch Bend** – changes pitch, allows smooth sliding between notes.
- **Channel Aftertouch** – allows modulation based on pressure applied.

Examples:

```python
sendControlChange(64, 127)  # Sustain pedal on
SendNote(67)                # Play G4
sendPB(14000)               # Bend pitch up
StartNote(60)               # Start C4
time.sleep(0.5)
StartNote(72)               # Start C5
StopNote(60)
StopNote(72)
```


Also looked into another potential problem, the frame rate.
* The frame rate is significantly reduced when two hands are on the screen. While it may not be a big issue, there may be even more of a reduction when we add new gestures for the model to recognize. Either way, the max number of hands we should do (and really need) is 2.
* Switching to the 8GB raspberry pi may slightly help this, since more RAM is better multitasking; MediaPipe + OpenCV + Python + camera feed + MIDI output = a lot going on.
* Could lower camera resolution slightly instead, or maybe even think about tracking one hand if it really becomes an issue.

## Monday, April 7 from 11:45pm - 3:45pm

#### 11:45-12:45pm

Installed necessary libraries for model training in jupyter notebook and worked with jupyter notebook to train the model with new data:
* Installed Jupyter Notebook for model training files, set up login : `pip install notebook`
* Installed tensorflow in virtual environment to complement tflite-runtime: `pip install tensorflow`
* Installed scikit-learn (sklearn): `pip install scikit-learn`

Continued MIDI research
* Looking for a way to play longer note (problem 1 from Wednesday: note trails off after playing, no matter if the "stop" gesture is detected)

#### 12:45pm - 2:00pm
Fixed problem 2 from Wednesday, where the note would only play once. 
* The problem was the while loop; once broken out of, you would not be able to enter it again. Removed the while to fix the problem.

Continued working on jupyter notebook for model training
* The jupyter notebook file came up with a lot of errors when trying to run it, a lot of them due to not having the correct installs. Worked on installing the necessary packages to get it running properly.
* Eventually, all jupyter notebook cells compiled properly, but the model training did not reflect the new dataset (i.e. did not add the new "peace sign" gesture) and was not able to detect the new gesture.
* Continued working on fixing this issue

Model training on jupyter notebook:

<img src="https://github.com/user-attachments/assets/a88352d8-4ca9-4884-a03b-c25b9cfd2bb5" alt="pic1" width="750"/>
<img src="https://github.com/user-attachments/assets/c027cd97-ba9b-4544-a14d-f36a81d9c507" alt="pic2" width="750"/>
<img src="https://github.com/user-attachments/assets/8583e4c7-4d5a-4544-baf7-5c1430e74635" alt="pic3" width="750"/>

#### 2:00pm - 7:35pm
Researched fluidsynth and soundfont libraries in order to play notes with no fading(envelope). The [Hs Synth Collection](https://musical-artifacts.com/artifacts/242) has a collection of instruments with no envelope. Researched how to change fluidsynth settings through the terminal.
Added code to call a shell script that automatically launches Fluidsynth and sets up the channels for MIDI output. 
``` python
import os

My_Cmmnd = "sh fs-run.sh"
os.system("gnome-terminal -e 'bash -c \"" + My_Cmmnd + ";bash\"'")
midiout= rtmidi.MidiOut()
available_ports = midiout.get_ports()
if available_ports:
    print("waiting for new fs port...")
    while True:
        try:
            midiout.open_port(2)
        except:
            continue
        else:
            print("connected to port 2")
            break
else:
    print("No port found")
    midiout.open_virtual_port("My virtual output")
```

```shell
fluidsynth -f fluidconfig.txt
```
The fluidconfig.txt file currently has 2 commands to load the soundfont and select an instrument: `load /home/Group6/Downloads/hand-gesture-recognition-mediapipe-main/SoundFonts/HS_Synth_Collection_I.sf2`
`select 0 2 000 055`

Added code to create the MIDImsg objects and call its functions.
```python
#                 handedness.classification[0].index
#                 if hand_sign_id == 0:
                #| setup hands to seperate channels |
                if handedness.classification[0].index == 0:
                    if LeftHand == None:
                        LeftHand = MIDImsg(60, 0)
                    if hand_sign_id == 0:
                        print(LeftHand.NoteOn())
                    if hand_sign_id == 1:
                        print(LeftHand.NoteOff())
                elif handedness.classification[0].index == 1:
                    if RightHand == None:
                        RightHand = MIDImsg(72, 1)
                    if hand_sign_id == 0:
                        print(RightHand.NoteOn())
                    if hand_sign_id == 1:
                        print(RightHand.NoteOff())
```
This code is at the end of the results handling section of the main function in app.py.
