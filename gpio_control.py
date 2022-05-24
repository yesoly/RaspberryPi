import PWM_Ri.GPIO as GPIO        
import time

# SPEED
speed = 30

# GPIO PIN NUMBER
##### motor #####
R1 = 13
R2 = 19
Ren = 3
L1 = 5
L2 = 6
Len = 26
##### ultra #####
GPIO_TRIGGER = 4
GPIO_ECHO = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor Setting
GPIO.setup(R1,GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(R2,GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(L1,GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(L2,GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Ren,GPIO.OUT)
GPIO.setup(Len,GPIO.OUT)
PWM_R = GPIO.PWM(Ren, 1000)
PWM_L = GPIO.PWM(Len, 1000)
PWM_R.start(speed)
PWM_L.start(speed)

# UltraSonic Setting
GPIO.setup(GPIO_TRIGGER, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(GPIO_ECHO, GPIO.IN)
time.sleep(2)

class move():
    def __init__(self):
        print("starting motor sensor")
        
    def Rspeed(self,val):
        PWM_R.ChangeDutyCycle(speed + val)
 
    def Lspeed(self,val):
        PWM_L.ChangeDutyCycle(speed + val)

    def forward(self):
        GPIO.output(R1, True)
        GPIO.output(R2, False)
        GPIO.output(L1, False)
        GPIO.output(L2, True)

    def cleanup():
        GPIO.output(R2, False)
        GPIO.output(R1, False)
        GPIO.output(L1, False)
        GPIO.output(L2, False)
        PWM_L.stop()
        PWM_R.stop()
        GPIO.cleanup()

class ultrasonic():    
    def __init__ (self):
        print("starting ultrasonic sensor")

    def Distance(self):
        #trigger the ultrasonic sensor for a very short period (10us).
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        
        while GPIO.input(GPIO_ECHO) == 0:
            pass
        StartTime = time.time() #start timer once the pulse is sent completely and echo becomes high or 1
        while GPIO.input(GPIO_ECHO) == 1:
            pass
        StopTime = time.time() #stop the timer once the signal is completely received  and echo again becomes 0

        TimeElapsed = StopTime - StartTime # This records the time duration for which echo pin was high 
        speed=34300 #speed of sound in air 343 m/s  or 34300cm/s
        twicedistance = (TimeElapsed * speed) #as time elapsed accounts for amount of time it takes for the pulse to go and come back  
        distance=twicedistance/2  # to get actual distance simply divide it by 2
        time.sleep(.01)
        return round(distance,2) # round off upto 2 decimal points