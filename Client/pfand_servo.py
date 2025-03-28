import RPi.GPIO as GPIO
import time
import threading as thrd

class Servo:
    def __init__(self, cfg: dict, logger):
        self.logger = logger

        self.pin = cfg['servo']['pin']
        self.min_degree = cfg['servo']['min_degree']
        self.max_degree = cfg['servo']['max_degree']

        self.bank_degree = cfg['servo']['bank_degree']
        self.bottle_degree = cfg['servo']['bottle_degree']
        self.middle_degree = cfg['servo']['middle_degree']

        self.enabled = False
        self.isOn = False
        self.startDelta = time.time()

        self.openingTime = 2.5

        self.safetyFIRST = False

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
        safetyFIRST = True
        GPIO.output(self.pin, 1)
        self.PWM.ChangeDutyCycle(self.bank_degree / 18 + 2)
        thrd.Thread(target=self.promisePowerOff).start()
        thrd.Thread(target=self.promiseClose).start()

    def open_bottle(self):
        GPIO.output(self.pin, 1)
        self.PWM.ChangeDutyCycle(self.bottle_degree / 18 + 2)
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
        self.PWM.ChangeDutyCycle(self.middle_degree / 18 + 2)
        thrd.Thread(target=self.promisePowerOff, args=(1.5, False)).start()

    def powerOff(self):
        self.PWM.ChangeDutyCycle(0)

    def promisePowerOff(self, time_to_sleep: float = 1.5, sf = True):
        self.safetyFIRST = sf
        time.sleep(time_to_sleep)
        self.powerOff()

    def promiseClose(self, time_to_sleep: float = 5):
        time.sleep(time_to_sleep)
        self.close()