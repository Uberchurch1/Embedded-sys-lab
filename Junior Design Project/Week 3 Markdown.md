## Project: Gesture Controlled Music
### Team: Jayden Okorougo, Anthony Hernandez, Gulliver Brower
### Date: April 9 - April 14

#### Project Focus This Week
*This week was mainly all coding and tweaking our main code, app.py, to function properly and match gestures to certain MIDI notes adn effects. We also started planning and talking about preparing for demo day; making the poster, how we would want to set it up, writing instructions, etc.*

## Wednesday, April 9 from 12:45pm - 3:35pm
#### 12:45-1:45pm
Researched and experimented with positions; trying to see if we can track the position of the hand to potentially change the pitch and/or other effects.
* fluidsynth works successfully and is able to play a continuous note
* Currently attempting to adjust the pitch on the y-axis, using up and down movement

Midifunc.py pitch code:
```python
def PedalBend(value, channel = 0x00):
    lsb = value & 0x7F
    msb = (value >> 7) & 0x7F
    midiout.send_message([0xE0 | channel, lsb, msb])
```

app.py pitch code:
```python
def PBend(self, value, rel=False):
        if rel==True:
            val = int(16384*value)
        mf.PedalBend(val, self.chan)

	#--Open--
	if hand_sign_id == 0:
	    RightHand.NoteOn()
	    RightHand.PBend(relVPos, rel=True)
```

Continued working on jupyter notebook to fix model training issues.

Also thinking about whether to stick with having a continuous note and adjusting the effects with distance and gestures, using gestures to play different notes, or some combination of both.
* How to incorporate the second hand? The code is able to differentiate pretty well between left and right hands, so we could do something different in each hand.

Started figuring out and planning what gestures will be used to play which notes. Currently, the gestures we have are as follows:
* Open hand: Note on
* Closed hand: Note off
* Pointer: unregistered
* OK sign: unregisterd
* Peace sign: unregistered
#### 1:45 - 3:35pm
Successfully implemented the pitch bend on the y-axis during our test.
Continued planning on what we would want the gestures to mean.
* We could have a set of gestures to change the note, and another set of gestures to change the mode.
* The mode would grant access to different effects on the channel. Since we only have the x and y axis to change, we can have these different modes so that each mode has a different effect on the x and y axis.
* For example, you could have pitch on the x axis and volume on the y axis for one mode, and then another mode could have reverb on the y axis and aftertouch on the x axis, etc. 

MIDI CC List for Continuous Controllers
https://anotherproducer.com/online-tools-for-musicians/midi-cc-list/
* Control Change is able to change the pitch, volume, etc. Useful for a variety of effects.

## Friday, April 11 from 12:15pm - 4:15pm

Continued working on the app.py code to integrate midi communication with gesture recognition
* Made the video window bigger for better clarity (fullscreen), but this increasing the resolution has a noticeable impact on the frame rate. Unless we can reduce the frame rate elsewhere, the video will probably remain 1280x720 or lower.
* Reverb did not have much effect on the audio, so looked into and tried to implement aftertouch/tremolo effect to replace it.
* Started implementing UI features to show the user what is being changed and how
	* Added labels to show the horizontal and vertical functions of the gesture and their current values
	* Added arrows to show the bounding box of value selection for both hands

## Monday, April 14 from 12:45pm - 3:35pm

Continued working on the the app.py code to integrate midi communication with gesture recognition, which is essentially all we have left to fully complete. 
* Once we are able to get all the effects and "modes" working on each hand gesture, we will be able to tweak and add extra things


Added Note Change and Octave Change
* Vertical: 1-12
	* Selects the key (A-G#) 
* Horizontal: 0-9
  	* Selects the ocatave 0-9
	* Multiply this number by 12 and add it to the vertical number
 	* Add base 20 since the first 20 does not hold a note

app.py Note and Octave change code:

  ```python
      def ChangeNote(self, Note):
        if (Note != self.note):
            self.NoteOff()
            self.note = Note
            self.NoteOn()
	
 	#--Pointer--
  	if hand_sign_id == 2:
  	    key = (invrelVPos * 11) + 1
            octave = relHPos * 9
  	    Note = key + (octave * 12) + 20
   	    RightHand.ChangeNote(Note)
	
  ```

Worked on Aftertouch/Tremolo Effect
* Fluidsynth does not support Tremolo effect, so we might try and implement our own tremolo effect using control change and adjusting the volume on and off.

Also started early thinking/planning on how we want to demo our project
* Need to write instructions for other people to try
* Write the poster explaining our project (could include instructions on the poster)
* Camera set-up/positioning (Needs to be away from hands so that the camera does not pick up background hands)
* Use of a monitor
* Practice demo
