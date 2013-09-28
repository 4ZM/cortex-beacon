from twisted.internet import protocol, reactor, endpoints, interfaces

from mockproducer import MockProducer

class BeaconServer(protocol.Protocol):
    def __init__(self, mock):
        self._producer = MockProducer(self, 10) if mock else MockProducer(self, 2)
        
    def connectionMade(self):
        self.transport.write("An apple a day keeps the doctor away\r\n")
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


