## Project: Gesture Controlled Music
### Team: Jayden Okorougo, Anthony Hernandez, Gulliver Brower
### Date: April 15 - April 20

#### Project Focus This Week
*As we near the end of the project, this week we will be focusing on completing the gesture recognition modes and effects, cleaning up the code so that labels, sizing, and other gui aspects are corrected, and planning for demo day.*

## Tuesday, April 15 from 3:00pm - 5:00pm
* Worked on project poster
* Will fill in any additional information and add a picture of screen with detection, labels and arrows once the project is closer to completion

![image](https://github.com/user-attachments/assets/968c0832-e7bb-43aa-8e38-1af2f2f43e18)

## Wednesday, April 16 from 12:45pm - 3:35pm

#### 12:45-2:30pm
Worked on getting the tremolo effect to work
* Since fluidsynth does not have a native tremolo effect (or aftertouch for that matter), we needed to manually implement it
* Tremolo is essentially created by quickly changing the volume up and down to produce a wavering sound
* Our original implementation tried to create multiple threads to adjust the volume, but this caused the frame rate to drop significantly.

We decided to look at and test other effects that could replace tremolo:
* Expression (which is a percentage of volume)
* Resonance

After trying and testing both of these, we did not hear much of a difference increasing or decreasing them, so they would not work well for our project. We may instead attempt the Tremolo effect again.

#### 2:30 - 3:35
Decided to move on to the UI design of the project. We focused on fixing the label that is displayed once your hand is detected. We want the user to be able to see and know the following information:

* What mode am I in?
* What note am I playing? (Inside pointer mode)
* What effects can I do in this mode?

![IMG_2301](https://github.com/user-attachments/assets/35c6d2e0-313d-48cb-b2a3-b923c1d62e7c)

*This image shows the effect in the black box above the gesture recognition box*


## Monday, April 21 from 11:45pm - 12:45pm

#### 11:45 - 12:45
Worked on fixing labels and improving fps; would drop to 5-6 fps when detecting hands and 8-10 without detecting hands. The original code had 15+ fps even when detecting hands.
* Most likely has to do with all the extra code (MIDI functions, etc.) that we added
* Changed the line `cv.waitKey(10)` to `cv.waitKey(1)`, which helped improve the fps slightly
* Changed the line `min_detection_confidence=0.5 and min_tracking_confidence=0.5` to `min_detection_confidence=0.7 and min_tracking_confidence=0.7` which also helped a little bit
* Will continue to look into other solutions , but for now I think it is still acceptable for the demo

#### 12:45 - 3:45

Worked on fixing labels for hand identification; being able to correctly label each gesture on each hand, even when both hands are on the screen:

Code section:
```python
if finger_gesture_text != "":
        if handedness.classification[0].index == 0:
            cv.putText(image, "Finger Gesture:" + hand_sign_text, (10, 100),
                    cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 4, cv.LINE_AA)
            cv.putText(image, "Finger Gesture:" + hand_sign_text, (10, 100),
                    cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2,
                    cv.LINE_AA)
        else:
            cv.putText(image, "Finger Gesture:" + hand_sign_text, (10, 60),
                    cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 4, cv.LINE_AA)
            cv.putText(image, "Finger Gesture:" + hand_sign_text, (10, 60),
                    cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2,
                    cv.LINE_AA)

    return image
```
![IMG_2305](https://github.com/user-attachments/assets/2eaa586d-383d-40a0-aebf-a7b54e5eb5fd)

*Top left corner shows both gestures that are being detected*


Also kept working on model training issues. We realized when labeling that the left hand for some reason is not able to detect the "OK" symbol; this is the only issue we have with the gestures. 
* Jupyter notebook, which is where the model training is done, continues to give errors when trying to train the model to add more data or gestures
* Worked on fixing this but with no luck
* Tried to redownload the files again from the github repo to see if our jupyter notebook was messed up from us trying to fix it, and to see if the original code did have the "OK" symbol on the left hand, but we realized that the original code also had this problem
* Will keep working on it, but it is not a major issue; the only function we have mapped to OK is volume, so we can just leave that as the only right hand function if need be.
