import time
import rtmidi

midiout= rtmidi.MidiOut()
available_ports = midiout.get_ports()
if available_ports:
    print(available_ports)
    port = input("Choose a port number")
    midiout.open_port(int(port))
    print(f"Opened port {port}")
#     midiout.open_port(1)
else:
    print("No port found")
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
