from random import random, randint
from time import sleep
from functools import reduce

packetSize = 24
channelLength = 48


class transmitError(Exception):
    pass


def createChannel(length):
    return list(None for _ in range(length))


def showElement(element):
    if element is None:
        return "-"
    else:
        return element[0]


class Channel:
    def __init__(self, length):
        self.length = length
        self.channel = createChannel(length)

    def __str__(self):
        return reduce(lambda message, order: message + showElement(order), self.channel, " ")

    def clear(self):
        self.channel = createChannel(self.length)

    def removeLeft(self):
        return self.channel[0] is None

    def removeRight(self):
        return self.channel[-1] is None

    def pushLeft(self, message):
        self.channel[0] = message, 1

    def pushRight(self, message):
        self.channel[-1] = message, -1

    def channelManager(self):
        newChannel = createChannel(self.length)

        receiveLeft = False
        receiveRight = False

        for i, element in enumerate(self.channel):
            if element is not None:
                message, directory = element
                position = i + directory
                if 0 <= position <= self.length - 1:
                    if newChannel[position] is None:
                        if self.channel[position] is None:
                            newChannel[position] = message, directory
                        else:
                            msg1, dir1 = self.channel[position]
                            if directory == dir1:
                                newChannel[position] = message, directory
                            else:
                                raise transmitError()
                    else:
                        raise transmitError()
                elif position < 0:
                    receiveLeft = True
                elif position >= self.length:
                    receiveRight = True
        self.channel = newChannel
        return receiveLeft, receiveRight


class Machine:
    def __init__(self, empty, push, message):
        self.empty = empty
        self.push = push
        self.message = message

        self.wait = 0
        self.sent = 0
        self.remove = 0
        self.collide = 0

    def channelManager(self):
        if self.remove > 0:
            self.push(self.message)
            self.remove -= 1
            self.sent += 1
        elif self.sent > 0:
            return
        elif self.wait == 0:
            if self.empty and random() < 0.01:
                self.push(self.message)
                self.remove = packetSize - 1
                self.sent = 1
        else:
            self.wait -= 1

    def collision(self):
        self.remove = 0
        self.collide += 1
        self.sent = 0
        if self.collide < 10:
            self.wait = randint(1, 2 ** self.collide)
        else:
            print("Can't send packet ", self.message)
            self.collide = 0
            self.wait = 0

    def received(self):
        self.sent -= 1
        if self.sent == 0:
            self.collide = 0
            print("Packet delivered by", "right machine" if self.message == "<" else "left machine")


def main():
    channel = Channel(channelLength)

    leftMachine = Machine(channel.removeLeft, channel.pushLeft, ">")
    rightMachine = Machine(channel.removeRight, channel.pushRight, "<")

    while True:
        try:
            leftMachine.channelManager()
            rightMachine.channelManager()
            print(channel)
            left, right = channel.channelManager()

            if left:
                rightMachine.received()
            if right:
                leftMachine.received()
            sleep(0.1)

        except transmitError:
            print("Packets had been collided")
            channel.clear()
            leftMachine.collision()
            rightMachine.collision()


if __name__ == "__main__":
    main()
