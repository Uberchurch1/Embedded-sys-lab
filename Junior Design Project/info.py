def Tremolo(value, Channel = 0x00) -> None:
    """
    Sends a Control Change (CC7) message for the tremolo effect.
    `value` is the volume (0 to 127) that determines the strength of the tremolo.
    """
    # CC7 is the standard MIDI control change for volume
    midiout.send_message([0xB0 | Channel, 7, value])

def applyTremolo(self, frequency, relHPos, depth=64):
        """
        Apply tremolo effect by adjusting volume based on horizontal hand position (relHPos).
        `frequency` controls the rate of modulation (how fast the tremolo oscillates).
        `relHPos` controls the strength of the tremolo effect (0 to 127).
        `depth` sets the maximum volume fluctuation range.
        """
        # Normalize the horizontal position (relHPos) to a MIDI volume range (0-127)
        tremolo_depth = int(relHPos * 127)  # Scale the hand position to MIDI depth (0-127)
        tremolo_depth = max(0, min(127, tremolo_depth))  # Clamp depth between 0 and 127

        # Modulate the volume for tremolo effect
        while True:
            Tremolo(tremolo_depth, self.chan)  # Send MIDI CC7 message to modulate volume
            time.sleep(1 / frequency)  # Control the speed of modulation

            Tremolo(0, self.chan)  # Set volume to 0 (off) for the "off" phase of the tremolo
            time.sleep(1 / frequency)  # Control the speed of modulation

