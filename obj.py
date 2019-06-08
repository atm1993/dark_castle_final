import re
import os
from colorFixer import fixColor

class Obj:
    def __init__(self, name='', roomText='', obvsText='', effectText='', roomWithEffect='', actionText='', allowedActions='', dropped=''):
        self.name = name
        self.roomText = roomText
        self.obvsText = obvsText
        self.effectText = effectText
        self.roomWithEffect = roomWithEffect
        self.actionText = actionText
        self.allowedActions = allowedActions
        self.dropped = dropped
    
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __eq__(self, other):
        self.name == other
    
    def loadObject(self, gameName, objectName):
        objectPath = './saved_games/' + gameName + '/objects/' + objectName + '.txt'
        if os.path.exists(objectPath) == False:
            return -1
        else:
            inputObject = open(objectPath, 'r')
            for line in inputObject:
                objectData = ''
                if 'actionText' in line:
                    words = re.split("[:]+", line)
                    words = [x.strip() for x in words]
                    counter = 1
                    objectData = []
                    if len(words) > 1 and words[1] != '':
                        for x in words[1:]:
                            if counter & 1:
                                objectData.append((x, words[counter+1]))
                            counter += 1
                elif 'allowedActions' in line:
                    words = re.split("[:,]+", line)
                    words = [x.strip() for x in words]
                    objectData = []
                    if len(words) > 1 and words[1] != '':
                        for x in words[1:]:
                            objectData.append(x)
                elif 'dropped' in line:
                    words = re.split("[:,]+", line)
                    words = [x.strip() for x in words]
                    if(words[1] == 'True'):
                            objectData = True
                    else:
                            objectData = False
                else:
                    words = re.split("[:]+", line)
                    words = [x.strip() for x in words]
                    if len(words) > 1:
                        objectData = fixColor(words[1])
                setattr(self, words[0], objectData)
