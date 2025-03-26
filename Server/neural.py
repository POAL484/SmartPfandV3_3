#from keras.models import load_model
#import numpy as np

class Neural:
    def __init__(self):
        self.model = ''#load_model("model.h5", compile=False)
        
    def predict(self, frameBytesHexString):
        '''frame = [[['']]]
        frameBytesHex = []
        for i in range(0, len(frameBytesHexString), 2):
            frameBytesHex.append(frameBytesHexString[i:i+2])
        #print(frameBytesHex)
        for byte in frameBytesHex:
            if byte == "1b":
                frame[-1][-1].remove(frame[-1][-1][-1])
                frame[-1].append([''])
            elif byte == "1f":
                frame[-1][-1].remove(frame[-1][-1][-1])
                frame[-1].remove(frame[-1][-1])
                frame.append([['']])
            elif byte == "1a":
                frame[-1][-1][-1] = int(frame[-1][-1][-1])
                frame[-1][-1].append('')
            else:
                frame[-1][-1][-1] += bytes.fromhex(byte).decode("ascii")
        frame.remove(frame[-1])
        frame = (np.asarray(frame).astype('float32')/127.5)-1
        frameArray = np.asarray([frame.tolist()])
        #preds = round(np.argmax(self.model.predict(np.asarray(frameArray))))
        m = self.model.predict(np.asarray(frameArray))
        print(m)
        print(np.argmax(m))
        print(round(np.argmax(m)))
        preds = round(np.argmax(m))
        print(preds)
        print(len(str(preds)))
        return preds'''
        return 0