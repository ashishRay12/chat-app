from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
from twisted.internet import reactor
import txredisapi as redis
import json
rc = redis.lazyConnection(host='127.0.0.1', port=6379, dbid=0)
from channelserver import myFactory


class Serverprotocol(WebSocketServerProtocol):

    def onConnect(self, request):
        try:
            self.userName = request.params['user'][0]
            self.channel = request.params['channel'][0]
            print("Client connecting: {0}".format(request.peer))
            reactor.connectTCP('127.0.0.1', 6379, myFactory(self))
        except KeyError as e:
            self.userName = None
            self.channel = None

    def onOpen(self):
        if self.userName is None or self.channel is None:
            self.sendClose()
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):

        message = json.dumps({"from": self.userName,
                              "message": payload.decode('utf8')})
        rc.publish(self.channel, message)

        # self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol = Serverprotocol
    # factory.setProtocolOptions(maxConnections=2)

    # note to self: if using putChild, the child must be bytes...

    reactor.listenTCP(9000, factory)
    reactor.run()
