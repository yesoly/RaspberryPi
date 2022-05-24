from time import sleep
import gpio_control
import ImageProcess
import cv2

# Camera Frame Setting
Frame_Width, Frame_Height = 640, 480
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, Frame_Width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, Frame_Height)

ultra = gpio_control.ultrasonic()
motor = gpio_control.move()
initial_speed = gpio_control.speed

def auto_drive(left, right, red):
    dis = ultra.Distance()

    print("distance=",dis)
    print("left=",left)
    print("right=",right)
    
    speedR, speedL, setback = 0,0,0

    if red or dis < 15 : 
        speedR = -1 * initial_speed
        speedL = -1 * initial_speed
    elif(left > right):
        speedR = 10
        speedL = -1 * initial_speed
    elif(right > left):
        speedL = 10
        speedR = -1 * initial_speed

    motor.Rspeed(speedR)
    motor.Lspeed(speedL)
    motor.forward()

try: 
    while True:
        _, frame = camera.read()
        frame, RED = ImageProcess.check_RED(frame)
        if RED:
            auto_drive(0,0,1) # left, right, red
        else:
            left, right, result = ImageProcess.line_detect() # left, right, img
            auto_drive(left, right, 0) # left, right, red

        cv2.imshow("Frame", result)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

finally:
    motor.cleanup()
    camera.release()
    cv2.destroyAllWindows()
