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

# with midiout:
#     sendControlChange(64, 127)
# #     SendNote(67)
# #     
# #     for bend in range(start, end + 1, step):
# #         sendPB(bend)
# #         time.sleep(delay)
#     StartNote(60)
#     time.sleep(0.5)
#     StartNote(72)
#     time.sleep(0.5)
#     StartNote(84)
#     time.sleep(1)
# #     StopNote(60)
#     StopNote(72)
#     StopNote(84)
#     time.sleep(1)
#     
# del midiout

