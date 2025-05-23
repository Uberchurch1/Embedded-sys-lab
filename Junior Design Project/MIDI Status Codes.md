http://www.opensound.com/pguide/midi/midi5.html

Listing of MIDI Status Codes

TABLE 1: Summary of MIDI Status & Data Bytes

(adapted from "MIDI by the Numbers" by D. Valenti, Elec Musician mag 2/88)

```
            STATUS BYTE                        |          DATA BYTES
------------------------------------------------------------------------------
   1st Byte Value |  Function                  |    2nd        |    3rd
 - - - - - - - - -|                            |    Byte       |    Byte
  Binary |Hex| Dec|                            |               |
 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
 10000000= 80= 128| Chan 1      Note off       |  Note Number  | Note Velocity
 10000001= 81= 129| Chan 2         "           |   (0-127)     |   (0-127)
 10000010= 82= 130| Chan 3         "           |     see       |      "
 10000011= 83= 131| Chan 4         "           |    Table      |      "
 10000100= 84= 132| Chan 5         "           |      2        |      "
 10000101= 85= 133| Chan 6         "           |      "        |      "
 10000110= 86= 134| Chan 7         "           |      "        |      "
 10000111= 87= 135| Chan 8         "           |      "        |      "
 10001000= 88= 136| Chan 9         "           |      "        |      "
 10001001= 89= 137| Chan 10        "           |      "        |      "
 10001010= 8A= 138| Chan 11        "           |      "        |      "
 10001011= 8B= 139| Chan 12        "           |      "        |      "
 10001100= 8C= 140| Chan 13        "           |      "        |      "
 10001101= 8D= 141| Chan 14        "           |      "        |      "
 10001110= 8E= 142| Chan 15        "           |      "        |      "
 10001111= 8F= 143| Chan 16        "           |      "        |      "
 10010000= 90= 144| Chan 1      Note on        |      "        |      "
 10010001= 91= 145| Chan 2         "           |      "        |      "
 10010010= 92= 146| Chan 3         "           |      "        |      "
 10010011= 93= 147| Chan 4         "           |      "        |      "
 10010100= 94= 148| Chan 5         "           |      "        |      "
 10010101= 95= 149| Chan 6         "           |      "        |      "
 10010110= 96= 150| Chan 7         "           |      "        |      "
 10010111= 97= 151| Chan 8         "           |      "        |      "
 10011000= 98= 152| Chan 9         "           |      "        |      "
 10011001= 99= 153| Chan 10        "           |      "        |      "
 10011010= 9A= 154| Chan 11        "           |      "        |      "
 10011011= 9B= 155| Chan 12        "           |      "        |      "
 10011100= 9C= 156| Chan 13        "           |      "        |      "
 10011101= 9D= 157| Chan 14        "           |      "        |      "
 10011110= 9E= 158| Chan 15        "           |      "        |      "
 10011111= 9F= 159| Chan 16        "           |      "        |      "
 10100000= A0= 160| Chan 1     Polyphonic      |      "        |  Aftertouch
 10100001= A1= 161| Chan 2     aftertouch      |      "        |   pressure
 10100010= A2= 162| Chan 3         "           |      "        |    (0-127)
 10100011= A3= 163| Chan 4         "           |      "        |      "
 10100100= A4= 164| Chan 5         "           |      "        |      "
 10100101= A5= 165| Chan 6         "           |      "        |      "
 10100110= A6= 166| Chan 7         "           |      "        |      "
 10100111= A7= 167| Chan 8         "           |      "        |      "
 10101000= A8= 168| Chan 9         "           |      "        |      "
 10101001= A9= 169| Chan 10        "           |      "        |      "
 10101010= AA= 170| Chan 11        "           |      "        |      "
 10101011= AB= 171| Chan 12        "           |      "        |      "
 10101100= AC= 172| Chan 13        "           |      "        |      "
 10101101= AD= 173| Chan 14        "           |      "        |      "
 10101110= AE= 174| Chan 15        "           |      "        |      "
 10101111= AF= 175| Chan 16        "           |      "        |      "
 10110000= B0= 176| Chan 1      Control/       |     See       |     See
 10110001= B1= 177| Chan 2     Mode change     |    Table      |    Table
 10110010= B2= 178| Chan 3         "           |    three      |    three
 10110011= B3= 179| Chan 4         "           |      "        |      "
 10110100= B4= 180| Chan 5         "           |      "        |      "
 10110101= B5= 181| Chan 6         "           |      "        |      "
 10110110= B6= 182| Chan 7         "           |      "        |      "
 10110111= B7= 183| Chan 8         "           |      "        |      "
 10111000= B8= 184| Chan 9         "           |      "        |      "
 10111001= B9= 185| Chan 10        "           |      "        |      "
 10111010= BA= 186| Chan 11        "           |      "        |      "
 10111011= BB= 187| Chan 12        "           |      "        |      "
 10111100= BC= 188| Chan 13        "           |      "        |      "
 10111101= BD= 189| Chan 14        "           |      "        |      "
 10111110= BE= 190| Chan 15        "           |      "        |      "
 10111111= BF= 191| Chan 16        "           |      "        |      "
 11000000= C0= 192| Chan 1      Program        |  Program #    |     NONE
 11000001= C1= 193| Chan 2       change        |   (0-127)     |      "
 11000010= C2= 194| Chan 3         "           |      "        |      "
 11000011= C3= 195| Chan 4         "           |      "        |      "
 11000100= C4= 196| Chan 5         "           |      "        |      "
 11000101= C5= 197| Chan 6         "           |      "        |      "
 11000110= C6= 198| Chan 7         "           |      "        |      "
 11000111= C7= 199| Chan 8         "           |      "        |      "
 11001000= C8= 200| Chan 9         "           |      "        |      "
 11001001= C9= 201| Chan 10        "           |      "        |      "
 11001010= CA= 202| Chan 11        "           |      "        |      "
 11001011= CB= 203| Chan 12        "           |      "        |      "
 11001100= CC= 204| Chan 13        "           |      "        |      "
 11001101= CD= 205| Chan 14        "           |      "        |      "
 11001110= CE= 206| Chan 15        "           |      "        |      "
 11001111= CF= 207| Chan 16        "           |      "        |      "
 11010000= D0= 208| Chan 1      Channel        |  Aftertouch   |      "
 11010001= D1= 209| Chan 2     aftertouch      |   pressure    |      "
 11010010= D2= 210| Chan 3         "           |   (0-127)     |      "
 11010011= D3= 211| Chan 4         "           |      "        |      "
 11010100= D4= 212| Chan 5         "           |      "        |      "
 11010101= D5= 213| Chan 6         "           |      "        |      "
 11010110= D6= 214| Chan 7         "           |      "        |      "
 11010111= D7= 215| Chan 8         "           |      "        |      "
 11011000= D8= 216| Chan 9         "           |      "        |      "
 11011001= D9= 217| Chan 10        "           |      "        |      "
 11011010= DA= 218| Chan 11        "           |      "        |      "
 11011011= DB= 219| Chan 12        "           |      "        |      "
 11011100= DC= 220| Chan 13        "           |      "        |      "
 11011101= DD= 221| Chan 14        "           |      "        |      "
 11011110= DE= 222| Chan 15        "           |      "        |      "
 11011111= DF= 223| Chan 16        "           |      "        |      "
 11100000= E0= 224| Chan 1       Pitch         |    Pitch      |    Pitch
 11100001= E1= 225| Chan 2       wheel         |    wheel      |    wheel
 11100010= E2= 226| Chan 3       range         |     LSB       |     MSB
 11100011= E3= 227| Chan 4         "           |   (0-127)     |   (0-127)
 11100100= E4= 228| Chan 5         "           |      "        |      "
 11100101= E5= 229| Chan 6         "           |      "        |      "
 11100110= E6= 230| Chan 7         "           |      "        |      "
 11100111= E7= 231| Chan 8         "           |      "        |      "
 11101000= E8= 232| Chan 9         "           |      "        |      "
 11101001= E9= 233| Chan 10        "           |      "        |      "
 11101010= EA= 234| Chan 11        "           |      "        |      "
 11101011= EB= 235| Chan 12        "           |      "        |      "
 11101100= EC= 236| Chan 13        "           |      "        |      "
 11101101= ED= 237| Chan 14        "           |      "        |      "
 11101110= EE= 238| Chan 15        "           |      "        |      "
 11101111= EF= 239| Chan 16        "           |      "        |      "
 11110000= F0= 240| System Exclusive           |      **       |      **
 11110001= F1= 241| System Common - undefined  |      ?        |      ?
 11110010= F2= 242| Sys Com Song Position Pntr |     LSB       |     MSB
 11110011= F3= 243| Sys Com Song Select(Song #)|   (0-127)     |     NONE
 11110100= F4= 244| System Common - undefined  |      ?        |      ?
 11110101= F5= 245| System Common - undefined  |      ?        |      ?
 11110110= F6= 246| Sys Com tune request       |     NONE      |     NONE
 11110111= F7= 247| Sys Com-end of SysEx (EOX) |      "        |      "
 11111000= F8= 248| Sys real time timing clock |      "        |      "
 11111001= F9= 249| Sys real time undefined    |      "        |      "
 11111010= FA= 250| Sys real time start        |      "        |      "
 11111011= FB= 251| Sys real time continue     |      "        |      "
 11111100= FC= 252| Sys real time stop         |      "        |      "
 11111101= FD= 253| Sys real time undefined    |      "        |      "
 11111110= FE= 254| Sys real time active sensing|     "        |      "
 11111111= FF= 255| Sys real time sys reset    |      "        |      "

 ** Note: System Exclusive (data dump) 2nd byte= Vendor ID followed by more
          data bytes and ending with EOX.
```

https://learn.sparkfun.com/tutorials/midi-tutorial/all
![image](https://github.com/user-attachments/assets/1fbfd302-f6ac-4594-b883-ef7f88864648)

