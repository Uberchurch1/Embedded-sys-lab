import time
import rtmidi
import time
import os
import threading

My_Cmmnd = "sh fs-run.sh"
os.system("gnome-terminal -e 'bash -c \"" + My_Cmmnd + ";bash\"'")
midiout= rtmidi.MidiOut()
available_ports = midiout.get_ports()
if available_ports:
#    print(available_ports)
#    port = input("Choose a port number")
#    midiout.open_port(int(port))
#    print(f"Opened port {port}")
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

midiout.send_message([0xB0, 65, 127])
midiout.send_message([0xB1, 65, 127])


global chanVol
chanVol = [0,0]

#sends a note of pitch Note to Channel (written as a hex value)
def SendNote(Note: int, Velocity: int = 100, Channel: int = 0x00, Duration: int = 1) -> None:
    noteOn = [0x90 | Channel, Note, Velocity]
    noteOff = [0x80 | Channel, Note, Velocity]
    midiout.send_message(noteOn)
    time.sleep(Duration)
    midiout.send_message(noteOff)
    
def sendControlChange(cc, value, channel = 0x00):
    midiout.send_message([0xb0 | channel, cc, value])
    
def PedalBend(value, channel = 0x00):
    lsb = value & 0x7F
    msb = (value >> 7) & 0x7F
    midiout.send_message([0xE0 | channel, lsb, msb])
    
def StartNote(Note: int, Velocity: int = 127, Channel: int = 0x00) -> None:
    noteOn = [0x90 | Channel, Note, Velocity]
    midiout.send_message(noteOn)

def StopNote(Note: int, Velocity: int = 100, Channel: int = 0x00) -> None:
    noteOff = [0x80 | Channel, Note, Velocity]
    midiout.send_message(noteOff)

def Reverb(value, Channel = 0x00) -> None:
    midiout.send_message([0xB0 | Channel, 91, value])

def Aftertouch(value, Channel = 0x00) -> None:
    midiout.send_message([0xD0 | Channel, value, 0])

def Volume(value, Channel = 0x00) -> None:
    global chanVol
    midiout.send_message([0xB0 | Channel, 7, value])
    chanVol[Channel] = value

def TremoloLoop(frequency, depth=64, Channel = 0x00) -> None:
    global chanVol
    curVol = chanVol[Channel]
    period = 1/frequency
    stepTime = 0.05
    step = depth*2/(period/stepTime)
    while True:
        if curVol >= chanVol[Channel]:
            increase = -1
        elif curVol <= max(0, chanVol[Channel]-depth):
            increase = 1
        curVol += step*increase
        midiout.send_message([0xB0 | Channel, 7, max(0,min(127,curVol))])



def Tremolo(value, Channel = 0x00) -> None:
    if value >= 24:
        t0 = threading.Thread(target=TremoloLoop, args=(value, 127, Channel))
        t0.start()
    elif t0 != None:
        t0.join(timeout=0.1)


def AllNotesOff() -> None:
    midiout.send_message([0xB0 | 0, 123, 0])
    midiout.send_message([0xB0 | 1, 123, 0])

def Expression(value, Channel=0x00):
    midiout.send_message([0xB0 |Channel, 11, value])

def DelMIDI():
    return None
    del midiout

#with midiout:
#    Reverb(0)
#    sendControlChange(64, 127)
#     SendNote(67)
#     
#     for bend in range(start, end + 1, step):
#         sendPB(bend)
#         time.sleep(delay)
#    StartNote(60)
#    time.sleep(0.5)
#    StartNote(72)
#    time.sleep(0.5)
#    StartNote(84)
#    time.sleep(3)
#    Expression(127)
#    Reverb(50)
#   midiout.send_message([0xB0, 77, 0])
#    StartNote(60)
#    time.sleep(3)
#    StopNote(60)
#    midiout.send_message([0xB0, 77, 32])
#    StartNote(60)
#    time.sleep(3)
#    StopNote(60)
#    midiout.send_message([0xB0, 77, 64])
#    StartNote(60)
#    time.sleep(3)
#    StopNote(60)
#    midiout.send_message([0xB0, 77, 127])
#    StartNote(60)
#    time.sleep(3)
#    StopNote(60)


#    Expression(10)
#    time.sleep(3)
#    StopNote(60)
#    StopNote(72)
#    StopNote(84)
#    time.sleep(1)
#    
#del midiout
