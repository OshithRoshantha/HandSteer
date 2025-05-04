import pyautogui
import time
from pynput import keyboard
import threading

class KeyLogger:
    def __init__(self):
        self.listener = None
        self.isRunning = False
        self.lastKeys = set()
        self.keyState = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }
    
    def onPress(self, key):
        try:
            keyChar = key.char.lower()
        except AttributeError:
            keyChar = str(key).lower()
        
        if keyChar in ['up', 'w']:
            self.keyState['up'] = True
        elif keyChar in ['down', 's']:
            self.keyState['down'] = True
        elif keyChar in ['left', 'a']:
            self.keyState['left'] = True
        elif keyChar in ['right', 'd']:
            self.keyState['right'] = True
    
    def onRelease(self, key):
        try:
            keyChar = key.char.lower()
        except AttributeError:
            keyChar = str(key).lower()
        
        if keyChar in ['up', 'w']:
            self.keyState['up'] = False
        elif keyChar in ['down', 's']:
            self.keyState['down'] = False
        elif keyChar in ['left', 'a']:
            self.keyState['left'] = False
        elif keyChar in ['right', 'd']:
            self.keyState['right'] = False
    
    def start(self):
        self.isRunning = True
        self.listener = keyboard.Listener(
            on_press=self.onPress,
            on_release=self.onRelease)
        self.listener.start()
    
    def stop(self):
        self.isRunning = False
        if self.listener:
            self.listener.stop()
    
    def getKeyState(self):
        return self.keyState.copy()

def testKeyLogger():
    logger = KeyLogger()
    logger.start()
    
    try:
        while True:
            state = logger.getKeyState()
            print(f"\rCurrent keys - Up: {state['up']}, Down: {state['down']}, Left: {state['left']}, Right: {state['right']}", end='')
            time.sleep(0.1)
    except KeyboardInterrupt:
        logger.stop()
        print("\nStopped key logger")

if __name__ == "__main__":
    testKeyLogger()
