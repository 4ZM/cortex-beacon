from twisted.internet import protocol, reactor, endpoints, interfaces
from random import random
import math

class MockProducer:
    """Sends an infinit stream of mocked data in the the cortext-beacon format"""
    __implements__ = interfaces.IPushProducer

    def __init__(self, proto, nfields):
        self._proto = proto
        self._paused = False
        self._nfields = nfields
        self._phase = 0
        
    def pauseProducing(self):
        self._paused = True

    def resumeProducing(self):
        self._paused = False
        while not self._paused:
            # Harmonic  noise at an offset
            # 8000 +/- 1000 sin + [0,100) rnd
            values = [str(int(8000 + 1000 * math.sin(self._phase) + 100 * random()))
                      for i in range(self._nfields)]
            self._proto.transport.write(",".join(values) + '\n')
            self._phase += (2 * math.pi / 100) % (2 * math.pi);

    def stopProducing(self):
        pass
