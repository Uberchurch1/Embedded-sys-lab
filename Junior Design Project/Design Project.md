Tues 3/25: read rtmidi documentation
## rtmidi
#### Ports/Outputs
get MIDI output channels with ``out = rtmidi.MidiOut()`` ``ports = out.get_ports()``. Then the ports can be opened with ``out.open_port(<port ID>)``.
#### Writing Signals
Use ``with out`` to send messages to the open port.
Notes are defined as a 1x3 array of numbers ``[<Status|Channel>, <Pitch>, <Velocity>]``

**Status | Channel:** Should be written as Hex to make it more readable (0xNibbles).
The Nibbles are written as two numbers 0-F and represent the command to be sent(Status) and on what channel(Channel). A list of all commands can be found [Here](https://www.songstuff.com/recording/article/midi-message-format/#elementor-toc__heading-anchor-0)

**Pitch:** Notes are in semitones so octaves are separated by 12 int (60 is middle C).

**Velocity: ** Velocity changes how 'hard' the key is pressed.

Wed 3/26: Tested rtmidi on windows laptop
``` python
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

Fri 3/28: Tested rtmidi code on raspberry pi
The code would send the MIDI messages through the virtual channel which could be picked up in reaper but the audio monitoring (realtime playback) in reaper was not working with the virtual MIDI channel.
Got rtmidi to work without reaper and just outputting to a virtual MIDI channel that went directly to the speaker connected to the pi.
Went on to research python libraries made for outputting MIDI messages directly to speakers(fluidsynth and tinysoundfont) These libraries are python wrappers for existing C/C++ libraries. The libraries were very similar to rtmidi but did not need to open a midi port.

Mon 3/31: Tested fluidsynth and tinysoundfont libraries.
We needed to update python for the libraries to work but updating to V 3.13 did not work with the libraries. Downgrading to python V 3.10 still did not let us install the libraries. we will have to try again with rtmidi or downgrade back to python V 3.9