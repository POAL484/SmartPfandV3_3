from pirc522 import RFID as rfid
import threading as thrd
import multiprocessing as mp

class RFID:
    def __init__(self, cfg: dict, logger):
        self.logger = logger
        self.device = rfid(pin_irq=None)
        thrd.Thread(target=self).start()
        self.logger("RFID main thread started")
        self.uuid = [False, ""]
        self._flagIsPresented = 0

    def make_req(self, r_dict):
        r_dict['val'] = self.device.request()

    def __call__(self):
        manager = mp.Manager()
        while 1:
            try:
                #(error, data) = self.device.request()
                #signal.signal(signal.SIGALRM, lambda _, __: print(end=''))
                #signal.alarm(10)
                #try:
                #    (error, data) = self.make_req()
                #except Exception:
                #    signal.alarm(0)
                #    continue
                r_dict = manager.dict()
                p = mp.Process(target=self.make_req, args=(r_dict, ))
                p.start()
                p.join(timeout=10)
                if p.is_alive():
                    p.terminate()
                    continue
                (error, data) = r_dict['val']
                if not error:
                    if self._flagIsPresented: self._flagIsPresented = 5
                    (error, uuid) = self.device.anticoll()
                    if not self._flagIsPresented:
                        self._flagIsPresented = 5
                        self.uuid = [True, uuid]
                        self.logger(f"new card presented: {uuid}")
                else:
                    if self._flagIsPresented: self._flagIsPresented -= 1
            except Exception as e:
                self.logger(f"ERROR --- in RFID main thread: {e}")

    def presentedCard(self):
        val = self.uuid.copy()
        self.uuid[0] = False
        return val

if __name__ == "__main__":
    from pfand_types import Logger
    from time import sleep
    rc522 = RFID({}, Logger())
    while 1:
        sleep(1.5)
        print(rc522.presentedCard())