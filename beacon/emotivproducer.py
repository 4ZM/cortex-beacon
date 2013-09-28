from twisted.internet import protocol, reactor, endpoints, interfaces

class EmotivProducer:
    """Sends an infinit stream of emotiv data in the the cortext-beacon format"""
    __implements__ = interfaces.IPushProducer

    def __init__(self, proto):
        self._proto = proto
        self._paused = False

    def pauseProducing(self):
        self._paused = True

    def resumeProducing(self):
        self._paused = False
        while not self._paused:
            self._proto.transport.write("whee e ")

    def stopProducing(self):
        pass
