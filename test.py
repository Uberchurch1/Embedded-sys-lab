#!/usr/bin/env python3
import serial
import time
import pyaudio
import sys
import wave
from pydub import AudioSegment
import threading
from scipy.io.wavfile import write

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()

    startPos = 0
    global curChunk
    global data
    global saveLoop
    saveLoop = False
    global loopData
    loopData = []
    global playLoop
    playLoop = False
    chunk = 1024
    curChunk = startPos * chunk

    startTime = time.time()
    curTime = time.time() - startTime
    fn = ' '.join(sys.argv[1:])

    pd = AudioSegment.from_file(fn)
    p = pyaudio.PyAudio()

    stream = p.open(format=
                    p.get_format_from_width(pd.sample_width),
                    channels=pd.channels,
                    rate=pd.frame_rate,
                    output=True)


    def playData():
        while True:
            global curChunk
            global data
            global saveLoop
            global loopData
            stream.write(data)
            curChunk += chunk
            data = pd[curChunk:curChunk + chunk]._data
            curPos = curChunk / chunk
            curTime = time.time() - startTime
            print(f"{curPos} -> {curTime}")
            if saveLoop:
                loopData.append(data)

    def writeLoop():
        global loopData
        global saveLoop
        write("loop.wav", pd.frame_rate, loopData)
        saveLoop = False

    def clearLoop():
        global loopData
        loopData = []

    def reset():
        ser.write(offsetCom.encode('utf-8'))
        curChunk = startPos * chunk
        data = pd[curChunk:curChunk + chunk]._data
        startTime = time.time()
        curTime = time.time() - startTime

    # commands
    encCom = "/EC"
    offsetCom = "/SO"
    readCom = "/LR"
    writeCom = "/LW"
    loopCom = "/LP"

    encSpeed = 1
    enc2sec = 1 / 330

    newPos = 0.0
    oldPos = 0.0

    reset()
    t1 = threading.Thread(target=playData)
    t1.start()
    while True:
        curPos = curChunk / chunk
        curTime = time.time() - startTime
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            if line[:3] == encCom:
                newPos = int(line[3:])
                if (newPos == oldPos):
                    curChunk = (newPos * enc2sec) * chunk
            elif line[:3] == readCom:
                saveLoop = True
                clearLoop()
            elif line[:3] == writeCom:
                writeLoop()
            elif line[:3] == loopCom:
                playLoop = not playLoop
            oldPos = newPos