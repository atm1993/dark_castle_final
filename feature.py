import re
import os
from colorFixer import fixColor

class Feature:
    def __init__(self, name='', obvsText='', actionText='', allowedActions=''):
        self.name = name
        self.obvsText = obvsText
        self.actionText = actionText
        self.allowedActions = allowedActions
    
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def __eq__(self, other):
        self.name == other

    def loadFeature(self, gameName, featureName):
        featurePath = './saved_games/' + gameName + '/features/' + featureName + '.txt'
        if os.path.exists(featurePath) == False:
            return -1
        else:
            inputFeature = open(featurePath, 'r')
            featureData = ''
            for line in inputFeature:
                if 'actionText' in line:
                    words = re.split("[:]+", line)
                    words = [x.strip() for x in words]
                    counter = 1
                    featureData = []
                    if len(words) > 1:
                        for x in words[1:]:
                            if counter & 1 and x != '':
                                featureData.append((x, fixColor(words[counter+1])))
                            counter += 1
                elif 'allowedActions' in line:
                    words = re.split("[:,]+", line)
                    words = [x.strip() for x in words]
                    featureData = []
                    if len(words) > 1:
                        for x in words[1:]:
                            if x != '':
                                featureData.append(x)
                else:
                    words = re.split("[:]+", line)
                    words = [x.strip() for x in words]
                    if len(words) > 1:
                        featureData = fixColor(words[1])
                setattr(self, words[0], featureData)
