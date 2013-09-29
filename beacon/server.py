# Need to import this first to get twisted to play nice with gevent
try:
    import geventreactor; geventreactor.install()
except ImportError:
    print "gevent not available"

from twisted.internet import protocol, reactor, endpoints, interfaces

class BeaconServer(protocol.Protocol):
    def __init__(self, mock):
        if mock:
            import mockproducer 
            self._producer = mockproducer.MockProducer(self, 17*2)
        else:
            import emotivproducer
            self._producer = emotivproducer.EmotivProducer(self)
        
    def connectionMade(self):
        self.transport.registerProducer(self._producer, True)
        self._producer.resumeProducing()
        self.transport.loseConnection()

class BeaconServerFactory(protocol.Factory):
    def __init__(self, mock):
        self._mock = mock
        
    def buildProtocol(self, addr):
        return BeaconServer(self._mock)
        
def start_beacon_server(port, mock_data = None):
    if mock_data is None: mock_data = False
    
    endpoint = endpoints.TCP4ServerEndpoint(reactor, port, mock_data)
    endpoint.listen(BeaconServerFactory(mock_data))
    reactor.run() 


