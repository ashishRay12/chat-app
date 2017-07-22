from __future__ import print_function
import json
import txredisapi as redis

from twisted.application import internet
from twisted.application import service


class myProtocol(redis.SubscriberProtocol):

    def connectionMade(self):
        # print("waiting for messages...")
        # print("use the redis client to send messages:")
        # print("$ redis-cli publish zz test")
        # print("$ redis-cli publish foo.bar hello world")

        #self.auth("foobared")

        self.subscribe(self.factory.channel)
        self.webs = self.factory.webs
        # self.psubscribe("foo.*")

    def messageReceived(self, pattern, channel, message):
        print("pattern=%s, channel=%s message=%s" % (pattern, channel, message))
        rd_message = json.loads(message)
        message = message.encode('utf8')
        self.webs.sendMessage(message, isBinary=False)

    def connectionLost(self, reason):
        print("lost connection:", reason)


class myFactory(redis.SubscriberFactory):
    # SubscriberFactory is a wapper for the ReconnectingClientFactory
    def __init__(self, webs):
        self.webs = webs
        self.channel = webs.channel
        print("channel :{}".format(self.channel))
        redis.SubscriberFactory.__init__(self)

    maxDelay = 120
    continueTrying = True
    protocol = myProtocol


# application = service.Application("subscriber")
# srv = internet.TCPClient("127.0.0.1", 6379, myFactory('foo'))
# srv.setServiceParent(application)
