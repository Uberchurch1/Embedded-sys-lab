#### Modes:
Each hand symbol or mode can change 3 effects which are defined by their Main Function, Horizontal Function, and Vertical Function.
- **Open:** MFunc -> NoteOn, HFunc -> Reverb, VFunc -> Pedal Bend
- **Closed:** MFunc -> NoteOff, HFunc -> null, VFunc -> null
- **Pointer:** MFunc -> null, HFunc -> Change Octave, VFunc -> Change Note
- **OK:** MFunc -> null, HFunc -> Aftertouch, VFunc -> Volume

UI text[showHandedness, showSign, showPos, showVals, Pos, ValH, ValV]
Pos[x, y]
ValH and ValV[ValID, Value]
ValID["Reverb", "Pedal Bend", "Octave", "Note", "Aftertouch", "Volume"]
