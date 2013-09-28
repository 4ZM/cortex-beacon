from twisted.internet import protocol, reactor, endpoints, interfaces
from emokit import emotiv
import gevent
import time

sensor_names = { 'X', 'Y',
                 'F3', 'FC5', 'AF3', 'F7', 'T7', 'P7',
                 'O1', 'O2', 'P8', 'T8', 'F8', 'AF4',
                 'FC6', 'F4', 'Unknown' }

class EmotivProducer:

    """Sends an infinit stream of emotiv data in the the cortext-beacon format"""

    __implements__ = interfaces.IPushProducer

    def __init__(self, proto):
        self._proto = proto
        self._paused = False

        self._headset = emotiv.Emotiv()

        # Start the emotiv data grabbing in a separate thread
        gevent.spawn(self._headset.setup)
        gevent.sleep(1)

    def pauseProducing(self):
        self._paused = True

    def resumeProducing(self):
        self._paused = False
        while not self._paused:
            try:
                packet = self._headset.dequeue()
            except KeyboardInterrupt:
                print "Disconnected client. Ctrl-C again to stop the server."
                return
            sensors = packet.sensors
            data_str = ",".join(str(sensors[x]['value']) for x in sensor_names)
            self._proto.transport.write(data_str + '\n')

    def stopProducing(self):
        self._headset.close()
        self._headset = None
        gevent.shutdown()
