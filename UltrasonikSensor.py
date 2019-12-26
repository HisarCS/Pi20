import RPi.GPIO as GPIO
from time import sleep, time
from threading import Thread


class UltrasonikSensor:

    def __init__(self, echo, trig, setup=GPIO.BOARD):
        self.echo = echo
        self.trig = trig

        self.sure = 0

        self.ankikOlcum = 0

        GPIO.setmode(setup)

        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

        GPIO.output(trig, False)

    def mesafeOlcmeyeBasla(self):

        Thread(target=self.__mesafeOlc__).start()
        sleep(0.2)

    def mesafeOku(self):
        return self.anlikOlcum

    def __mesafeOlc__(self):

        while True:
            GPIO.output(self.trig, True)
            sleep(0.0001)
            GPIO.output(self.trig, False)

            sinyal_baslangic = time()

            while GPIO.input(self.echo) == 1:
                sinyal_bitis = time()

                self.sure = sinyal_bitis - sinyal_baslangic
                self.anlikOlcum = self.sure * 17150