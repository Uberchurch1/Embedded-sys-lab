#!/usr/bin/env python3
import serial
import time
import pyaudio
import sys
import wave
from pydub import AudioSegment
import threading
from scipy.io.wavfile import write
import os

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
    gain = 20

    startTime = time.time()
    curTime = time.time() - startTime
    songs = os.listdir("music/")
    for i in range(len(songs)):
        print(f"{i}) {songs[i]}")
    index = int(input("select song: "))
    song = songs[index]
    print(f"song chosen: {song}")
    fn = 'music/'+''.join(song)

    pd = AudioSegment.from_file(fn)
    pd -= gain
    p = pyaudio.PyAudio()
    r = pyaudio.PyAudio()

    stream = p.open(format=
                    p.get_format_from_width(pd.sample_width),
                    channels=pd.channels,
                    rate=pd.frame_rate,
                    output=True)
    
    record = r.open(format=
                    p.get_format_from_width(pd.sample_width),
                    channels=pd.channels,
                    rate=pd.frame_rate,
                    input=True)

    def playData():
        while True:
            global curChunk
            global data
            global saveLoop
            global loopData
            global loopBytes
            curChunk += chunk
            if playLoop:
                print("loop")
                data = loopBytes[curChunk:curChunk + chunk]
            else:
                data = pd[curChunk:curChunk + chunk]._data
            curPos = curChunk / chunk
            curTime = time.time() - startTime
            #print(f"global: {curPos} -> {curTime}")
            if data == b'':
                reset()
            stream.write(data)
    
    def recordData():
        global saveLoop
        while record.get_read_available() > 0:
            record.read(record.get_read_available())
        wf = wave.open('loop.wav','wb')
        wf.setnchannels(pd.channels)
        wf.setsampwidth(pd.sample_width)
        wf.setframerate(pd.frame_rate)
        while saveLoop:
             recData = record.read(chunk)
             print(f"recording...")
             loopData.append(recData)
             wf.writeframes(recData)



    def writeLoop():
        global loopData
        global saveLoop
        global loopBytes
        loopBytes = b''.join(loopData)
        #write("loop.wav", pd.frame_rate, loopBytes)
        saveLoop = False
        tr.join()

    def clearLoop():
        global loopData
        global loopBytes
        loopData = []
        loopBytes = b''
        try:
            os.remove('loop.wav')
        except FileNotFoundError:
            print("no current loop.wav file")
        except:
            print("other error")


    def reset():
        global curChunk
        global data
        ser.write(offsetCom.encode('utf-8'))
        curChunk = startPos * chunk
        if playLoop:
            print("loop")
            data = loopBytes[curChunk:curChunk + chunk]
        else:
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
    enc2sec = 1 / 300

    newPos = 0.0
    oldPos = 0.0

    reset()
    clearLoop()
    tw = threading.Thread(target=playData)
    tw.start()
    tr = threading.Thread(target=recordData)

    while True:
        curPos = curChunk / chunk
        curTime = time.time() - startTime
        #print(f"local: {curPos} -> {curTime}")
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
                tr.start()
            elif line[:3] == writeCom:
                writeLoop()
            elif line[:3] == loopCom:
                reset()
                playLoop = not playLoop
            oldPos = newPos
