from time import sleep
from gpiozero import Button, LED
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
        print(f"Right LED state: {self.Rbool}")
        
    def toggleL(self):
        self.Lbool = self.toggleLED(self.Lbool)
        print(f"Left LED state: {self.Lbool}")
        
    def toggleH(self):
        # Toggle hazard state (if it's already on, turn it off; if it's off, turn it on)
        if self.Hbool:
            self.Hbool = False
            self.Rbool = False
            self.Lbool = False
            print(f"Hazard state: {self.Hbool} (Off)")
        else:
            self.Hbool = True
            self.Rbool = True
            self.Lbool = True
            print(f"Hazard state: {self.Hbool} (On)")

    def toggleLED(self, LEDbool):
        return not LEDbool
    
    def blinkLEDs(self):
        print("blink ON")
        if self.Rbool:
            print("Right LED ON")
            self.Rled.on()
        if self.Lbool:
            print("Left LED ON")
            self.Lled.on()

        # Hazard light check: If both LEDs are on, consider hazard lights
        if self.Hbool:
            print("Hazard lights ON")
            self.Rled.on()
            self.Lled.on()


        sleep(1)
        print("blink OFF")
        self.Rled.off()
        self.Lled.off()
        sleep(1)
        
    def run(self):
        print("run")
        self.Rbut.when_pressed = self.toggleR
        self.Lbut.when_pressed = self.toggleL
        self.Hbut.when_pressed = self.toggleH  # Add handler for hazard button

# Initialize the system
print("Start")
MyCar = CarSys(17, 27, 22, 23, 24)
MyCar.run()

# Keep the program running and processing button presses
while True:
    MyCar.blinkLEDs()
pause()
