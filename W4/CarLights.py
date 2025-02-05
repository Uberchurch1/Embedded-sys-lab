from time import sleep
from gpiozero import Button,LED
from signal import pause

class CarSys:
    def __init__(self, rled, lled, rbut, lbut, hbut):
        self.Rled = LED(rled)
        self.Rbool = False
        self.Lled = LED(lled)
        self.Lbool = False
        self.Hbool = False
        self.Rbut = Button(rbut)
        self.Lbut = Button(lbut)
        self.Hbut = Button(hbut)
    
    def toggleR(self):
        self.Rbool = self.toggleLED(self.Rbool)
        print(self.Rbool)
        
    def toggleL(self):
        self.Lbool = self.toggleLED(self.Lbool)
        print(self.Lbool)
        
    def toggleH(self):
        self.Hbool = self.toggleLED(self.Lbool and self.Rbool)
        print(self.Hbool)
    
    def toggleLED(self, LEDbool):
        return not LEDbool
    
    def blinkLEDs(self):
        print("blink ON")
        if(self.Rbool):
            print("R ON")
            self.Rled.on()
        if(self.Lbool):
            print("L ON")
            self.Lled.on()
        if(self.Lbool):
            print("Hazard ON")
            self.Lled.on() and self.Rled.on()
        sleep(1)
        print("blink OFF")
        self.Rled.off()
        self.Lled.off()
        sleep(1)
        
    def run(self):
        print("run")
        self.Rbut.when_pressed = self.toggleR
        self.Lbut.when_pressed = self.toggleL
        
        #blinkLEDs()
print("start")
MyCar = CarSys(17, 27,22,23, 24)
MyCar.run()

while(True):
    MyCar.blinkLEDs()
pause()