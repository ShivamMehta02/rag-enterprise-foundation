import time

class Metrics:

    def __init__(self):
        self.start_times = {}

    def start(self, name):
        self.start_times[name] = time.time()

    def end(self, name):
        if name in self.start_times:
            elapsed = time.time() - self.start_times[name]
            print(f"[METRIC] {name} took {elapsed:.4f} seconds")
            return elapsed