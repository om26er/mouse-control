import asyncio

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner

import x11_input

PROCEDURE_MOVE = 'com.om26er.mouse.move'


class ClientSession(ApplicationSession):

    def __init__(self, config=None):
        super().__init__(config)
        self.mouse = x11_input.Mouse()

    async def onJoin(self, details):
        self.log.info("Successfully joined session {}".format(details.session))
        self.register(self.mouse.move, PROCEDURE_MOVE)

    def onLeave(self, details):
        self.log.info("session closed: {details}", details=details)
        self.disconnect()

    def onDisconnect(self):
        self.log.info("connection to router closed")
        asyncio.get_event_loop().stop()


def main():
    runner = ApplicationRunner(url="ws://localhost:8080/ws", realm="realm1")
    runner.run(ClientSession)


if __name__ == '__main__':
    main()
