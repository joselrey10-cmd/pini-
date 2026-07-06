
from dataclasses import dataclass
from threading import Event, Thread
import time

@dataclass
class ContinuousOptimizationState:
    iterations:int=0
    best_score:float=0.0
    running:bool=False

class ContinuousOptimizer:
    def __init__(self, step_callback=None):
        self._stop=Event()
        self.state=ContinuousOptimizationState()
        self._cb=step_callback

    def start(self):
        if self.state.running:
            return
        self.state.running=True
        Thread(target=self._loop,daemon=True).start()

    def _loop(self):
        while not self._stop.is_set():
            self.state.iterations+=1
            self.state.best_score=min(100.0,self.state.best_score+0.5)
            if self._cb:
                self._cb(self.state)
            time.sleep(0.05)
        self.state.running=False

    def stop(self):
        self._stop.set()
