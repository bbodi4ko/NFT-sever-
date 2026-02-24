import asyncio
import random

class Rocket:
    def __init__(self):
        self.multiplier = 1.0
        self.running = True
        self.callbacks = []

    def subscribe(self, callback):
        self.callbacks.append(callback)

    async def start(self):
        while self.running:
            step = random.uniform(0.05, 0.2)
            self.multiplier += step
            if self.multiplier >= 3.0:
                # пауза 5 секунд для ставок
                for cb in self.callbacks:
                    await cb(self.multiplier, True)
                await asyncio.sleep(5)
                self.multiplier = random.uniform(1.0, 1.5)
            else:
                for cb in self.callbacks:
                    await cb(self.multiplier, False)
                await asyncio.sleep(1)
