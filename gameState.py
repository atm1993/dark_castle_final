import re
import os
import shutil
from room import Room
from obj import Obj

class gameState:
    def __init__(self, name='', currentRoom='', inventory=''):
        self.name = name
        self.currentRoom = currentRoom
        self.inventory = inventory
    
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def loadGame(self, gameName):
        gamePath = './saved_games/' + gameName +'/game_state.txt'
        if os.path.exists(gamePath) == False:
            return -1
        inputGame = open(gamePath, 'r')
        for line in inputGame:
            if 'currentRoom' in line:
                words = re.split("[:]+", line)
                words = [x.strip() for x in words]
                gameStateData = Room()
                gameStateData.loadRoom(gameName, words[1])
            elif 'inventory' in line:
                words = re.split("[:,]+", line)
                words = [x.strip() for x in words]
                gameStateData = []
                if len(words) > 1 and words[1] != '':
                    for x in words[1:]:
                        myObject = Obj()
                        myObject.loadObject(gameName, x)
                        gameStateData.append(myObject)
            else:
                words = re.split("[:]+", line)
                words = [x.strip() for x in words]
                gameStateData = words[1]
            setattr(self, words[0], gameStateData)
    
    def saveGame(self):
        gamePath = './saved_games/' + self.name +'/game_state.txt'
        if os.path.exists(gamePath) == False:
            return -1
        with open(gamePath, 'r') as gameStateData:
            data = gameStateData.readlines()
            data[0] = "name: " + self.name + '\n'
            data[1] = "currentRoom: " + self.currentRoom.name + '\n'
            data[2] = 'inventory:'
            count = 0
            for x in self.inventory:
                if count == len(self.inventory) - 1:
                    data[2] += ' ' + x.name
                else:
                    data[2] += ' ' + x.name + ','
        with open(gamePath, 'w') as gameStateFile:
            gameStateFile.writelines(data)
        
    def newGame(self, gameName):
        gamePath = './saved_games/' + gameName +'/game_state.txt'
        if os.path.exists(gamePath) == True:
            return -1
        src = './data_files/'
        dst = './saved_games/' + gameName
        shutil.copytree(src, dst)
        with open(gamePath, 'r') as gameStateFile:
            data = gameStateFile.readlines()
            data[0] = "name: " + gameName + '\n'
            data[1] = "currentRoom: castle_gate" + '\n'
        with open(gamePath, 'w') as gameStateFile:
            gameStateFile.writelines(data)
        self.loadGame(gameName)


    
    def dropItemInRoom(self, objectName):
        roomPath = './saved_games/' + self.name + '/rooms/' + self.currentRoom.name + '.txt'
        objectPath = './saved_games/' + self.name + '/objects/' + objectName + '.txt'
        if os.path.exists(roomPath) == False or os.path.exists(objectPath) == False or any(x.name == objectName for x in self.inventory) == False:
            return -1
        else:
            for x in self.inventory:
                if x.name == objectName:
                    x.dropped = True
                    self.currentRoom.pickupObjects.append(x)
                    self.inventory.remove(x)
            with open(roomPath, "a") as roomFile:
                addObject = ' ' + objectName + ","
                roomFile.write(addObject)
            with open(objectPath, 'r') as objectFile:
                data = objectFile.read()
                data = data.replace("False", "True")
                outputObjectFile = open(objectPath, 'w')
                outputObjectFile.write(data)
            self.saveGame()


    def pickupItemInRoom(self, objectName):
        roomPath = './saved_games/' + self.name + '/rooms/' + self.currentRoom.name + '.txt'
        if os.path.exists(roomPath) == False:
            return -1
        elif any(x.name == objectName for x in self.currentRoom.pickupObjects):
            with open(roomPath, 'r') as inputRoom:
                lines = inputRoom.readlines()
            with open(roomPath, "w") as inputRoom:
                for line in lines:
                    words = re.split("[:,]+", line)
                    words = [x.strip() for x in words]
                    if words[0] == 'pickupObjects':
                        words.remove(objectName)
                        newline = words[0] + ':'
                        count = 1
                        for item in words[1:]:
                            if item != '':
                                if count == len(words) - 1:
                                    newline += ' ' + item
                                else:
                                    newline += ' ' + item + ','
                            count += 1
                        inputRoom.write(newline)
                    else:
                        inputRoom.write(line)
            for x in self.currentRoom.pickupObjects:
                if x.name == objectName:
                    self.inventory.append(x)
                    self.currentRoom.pickupObjects.remove(x)
            self.saveGame()
        else:
            return -1

    def checkHiddenChamberStatus(self):
        gamePath = './saved_games/' + self.name +'/game_state.txt'
        if os.path.exists(gamePath) == False:
            return -1
        if self.currentRoom.name == 'throne_room':
            counter = 0
            for x in self.inventory:
                if x.name == 'mirror' or x.name == 'jeweled_pendant' or x.name == 'royal_crown':
                    counter = counter + 1
            if counter == 3:
                return 1
        else:
            return -1
