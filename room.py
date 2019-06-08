import re
import os
from feature import Feature
from obj import Obj
from colorFixer import fixColor

class Room:
    def __init__(self, name='', longForm='', shortForm='', north='', south='', east='', west='', up='', down='', visited='', features='', pickupObjects=''):
        self.name = name
        self.longForm = longForm
        self.shortForm = shortForm
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.up = up
        self.down = down
        self.visited = visited
        self.features = features
        self.pickupObjects = pickupObjects
    
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __eq__(self, other):
        self.name == other
    
    def loadRoom(self, gameName, roomName):
        roomPath = './saved_games/' + gameName + '/rooms/' + roomName + '.txt'
        if os.path.exists(roomPath) == False:
            return -1
        else:
            inputRoom = open(roomPath, 'r')
            for line in inputRoom:
                roomData = ''
                if 'features' in line:
                    words = re.split("[:,]+", line)
                    words = [x.strip() for x in words]
                    roomData = []
                    if len(words) > 1:
                        for x in words[1:]:
                            if x != '':
                                myFeature = Feature()
                                myFeature.loadFeature(gameName, x)
                                roomData.append(myFeature)
                elif 'pickupObjects' in line:
                    words = re.split("[:,]+", line)
                    words = [x.strip() for x in words]
                    roomData = []
                    if len(words) > 1:
                        for x in words[1:]:
                            if x != '':
                                myObject = Obj()
                                myObject.loadObject(gameName, x)
                                roomData.append(myObject)
                else:
                    words = re.split("[:]+", line)
                    words = [x.strip() for x in words]
                    if words[0] == 'visited':
                        if(words[1] == 'True'):
                            roomData = True
                        else:
                            roomData = False
                    elif len(words) > 1:
                        roomData = fixColor(words[1])
                setattr(self, words[0], roomData)
    
    def markVisited(self, gameName):
        roomPath = './saved_games/' + gameName + '/rooms/' + self.name + '.txt'
        if os.path.exists(roomPath) == False:
            return -1
        else:
            inputRoom = open(roomPath, 'r')
            data = inputRoom.read()
            data = data.replace("False", "True")
            outputRoom = open(roomPath, 'w')
            outputRoom.write(data)
            self.visited = True






