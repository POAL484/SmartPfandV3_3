import RPi.GPIO as GPIO
import time
import threading as thrd

class Servo:
    def __init__(self, cfg: dict, logger):
        self.logger = logger

        self.pin = cfg['servo']['pin']
        self.min_degree = cfg['servo']['min_degree']
        self.max_degree = cfg['servo']['max_degree']

        self.enabled = False
        self.isOn = False
        self.startDelta = time.time()

        self.openingTime = 2.5

        self.last_com_time = time.time()

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.PWM = GPIO.PWM(self.pin, 50)
        self.PWM.start(0)

        self.logger("servo inited")

    def __call__(self): #deprecated
        if self.enabled:
            #self.isOn = True
            angle = self.min_degree + (((time.time() - self.startDelta) / self.openingTime) * (self.max_degree - self.min_degree))
            if angle >= self.max_degree:
                self.enabled = False
                thrd.Thread(target=self.timer).start()
                return
            duty = angle / 18 + 2
            GPIO.output(self.pin, 1)
            self.PWM.ChangeDutyCycle(duty)
        elif self.isOn:
            GPIO.output(self.pin, 0)
            self.PWM.ChangeDutyCycle(0)
            self.isOn = False
            self.logger("servo stopped")

    #def open(self):
    #    self.enabled = True
    #    self.logger("servo is opening now")

    def open_bank(self):
        GPIO.output(self.pin, 1)
        self.PWM.ChangeDutyCycle(180 / 18 + 2)
        thrd.Thread(target=self.promisePowerOff).start()
        thrd.Thread(target=self.promiseClose).start()

    def open_bottle(self):
        GPIO.output(self.pin, 1)
        self.PWM.ChangeDutyCycle(0)
        thrd.Thread(target=self.promisePowerOff).start()
        thrd.Thread(target=self.promiseClose).start()

    def timer(self):
        time.sleep(5)
        self.close()

    #def close(self):
    #    self.isOn = True
    #    GPIO.output(self.pin, 1)
    #    self.PWM.ChangeDutyCycle(self.min_degree / 18 + 2)
    #    self.logger("servo closing")

    def close(self):
        GPIO.output(self.pin, 1)
        self.PWM.ChangeDutyCycle(90 / 18 + 2)
        thrd.Thread(target=self.promisePowerOff).start()

    def powerOff(self):
        self.PWM.ChangeDutyCycle(0)

    def promisePowerOff(self, time_to_sleep: float = 3.5):
        time.sleep(time_to_sleep)
        self.powerOff()

    def promiseClose(self, time_to_sleep: float = 5):
        time.sleep(time_to_sleep)
        self.close()