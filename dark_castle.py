import feature
import gameState 
import room 
import obj 
import sys 
from parser import Parse
playerIsAlive = True 
gameWon = False 

def printScreen(screen_file):
	with open(screen_file) as input_file:
		for line in input_file:
			sys.stdout.write(line)

def getGametype():

	while 1:
		game_type = input("(N)ew game or (L)oad game > ")
		game_type = game_type.upper()

		if game_type == "QUIT" or game_type == "Q":
			exit()
		elif game_type == "N":
			gameName = input("Enter a new game name: ")
			myGameState = gameState.gameState()
			if myGameState.newGame(gameName) == -1:
				print("A game with that name already exists!")
				print("Please try again.")
				continue
			else:
				return myGameState
		elif game_type == "L":
			gameName = input("Enter the saved game name to load: ")
			myGameState = gameState.gameState()
			if myGameState.loadGame(gameName) == -1:
				print("No game with that name exists!")
				print("Please try again")
				continue
			else:
				return myGameState
		else:
			print("I don't understand that command.")
			print("Please try again!") 

def moveRoom(roomName):
	myGameState.currentRoom.loadRoom(myGameState.name, roomName)

	if myGameState.checkHiddenChamberStatus() == 1:
		print("You enter the throne room...")
		print("The mirror, jeweled pendnant, and royal crown are urging you towards the statue near the head of the room.")
		print("You realize what the depressions in the statue are for. You play the three objects in their rightful place on the state.")
		print("The statue begins to glow a magnificent blue, and suddenly a ray of light shoots towards the northern wall. A passageway opens to a \033[92mhidden chamber\033[0m.")
		print("Will you enter?")
		return
	
	if myGameState.currentRoom.visited == False:
		print(myGameState.currentRoom.longForm)
	else:
		print(myGameState.currentRoom.shortForm)

	if myGameState.currentRoom.name == 'hidden_chamber':
		printScreen('treasure.txt')
	
	for i in myGameState.inventory:
		if i.roomWithEffect == myGameState.currentRoom.name:
			print(i.effectText)

	for i in myGameState.currentRoom.pickupObjects:
		if i.name != '' and i.dropped == True:
			print("The \033[93m" + i.name + "\033[0m you left is still here.")
		elif i.name != '' and i.dropped == False and i.roomText != '':
			print(i.roomText)

	myGameState.currentRoom.markVisited(myGameState.name)
	myGameState.saveGame()

def goToRoom(direction, room):
	if direction is not None:
		if getattr(myGameState.currentRoom, direction.lower()) == "none":
			print("You can't go that way")
			return
		else:
			moveRoom(getattr(myGameState.currentRoom, direction))
			return
	elif room is not None:
		if room == myGameState.currentRoom.name:
			print("You're already there!")
			return
		directionList = ['north', 'south', 'east', 'west']
		for i in directionList:
			if getattr(myGameState.currentRoom, i ) == room:
				moveRoom(getattr(myGameState.currentRoom, i))
				return
		print("You can't go there from here")
	else:
		print("You can't go to that room")	
	

def look():
	print(myGameState.currentRoom.longForm)

	for i in myGameState.inventory:
		if i.roomWithEffect == myGameState.currentRoom.name:
			print(i.effectText)

	for i in myGameState.currentRoom.pickupObjects:
		if i.name != '' and i.dropped == True:
			print("The \033[93m" + i.name + "\033[0m you left is still here.")
		elif i.name != '' and i.dropped == False and i.roomText != '':
			print(i.roomText)

def take(objects):

	if objects == None or objects == "":
		print("You must enter something to take")
		return

	for i in myGameState.currentRoom.pickupObjects:
		if i.name == objects:
			myGameState.pickupItemInRoom(objects)
			print("You take the " + objects)
			return
	
	for j in myGameState.currentRoom.features:
		
		if objects in parser.items and j.name == parser.items[objects]:
			print("You can't take that")
			return 

	
	if objects[-1] != 's':
		print ("There is no " + str(objects) + " to take")
	else:
		print ("There are no " + str(objects) + " to take")

def drop(objects):
	
	if objects == None or objects == "":
		print("You must enter something to drop")
		return 

	for i in myGameState.inventory:
		if i.name == objects:
			myGameState.dropItemInRoom(objects)
			print(objects + " dropped")
			return 
	print("You aren't carrying that")

def inventory():
	print("Your inventory:")
	for i in range(len(myGameState.inventory)):
		print(myGameState.inventory[i].name)

def lookAt(items):
	for i in myGameState.currentRoom.features:
		if i.name == items:
			#featureWItem = i.obvsText
			for obj in parser.objects:
				if obj in i.obvsText and getattr(myGameState.currentRoom, 'pickupObjects') == [] and myGameState.currentRoom.name !='great_hall':
					print("There is nothing else interesting there")
					return 
			#print(getattr(myGameState.currentRoom, 'pickupObjects'))
			print(i.obvsText)
			return
	if items == '':
		print("Look at what?")
	else:
		print("There is nothing interesting about that.")

def performAction(action, item):
	if item is None or item == '':
		print(action + " what?")
		return

	for i in myGameState.currentRoom.features:
		if i.name == item:
			if action in i.allowedActions:
				for x, y in i.actionText:
					if x == action:
						for obj in parser.objects:
							if obj in y and getattr(myGameState.currentRoom, 'pickupObjects') == []:
								print("There is nothing else interesting there")
								return 
						print(y)

				return
			else:
				print("You can't " + action + " that!")
				return
	for i in myGameState.currentRoom.pickupObjects:
		if i.name == item:
			print("Add this item to your inventory before you mess around with it!")
			return
	for i in myGameState.inventory:
		if i.name == item:
			if action in i.allowedActions:
				for x, y in i.actionText:
					if x == action:
						print(y)
						return
			else:
				print("You can't " + action + " that!")
				return
		
	print("You don't have " + item )
	return

def help():
	print("Here are some things you can try:")
	print("go to, go, east, north, west, south, up, down")
	print("look, look at")
	print("push")
	print("read")
	print("take, grab, pick up")
	print("There are more actions, try thinking what seems logical for the feature you are looking at!")
	print("Good luck!")


### MAIN GAME ### 

title_screen = "dark_castle_title.txt"

printScreen(title_screen)

myGameState = getGametype()

moveRoom(myGameState.currentRoom.name)

while (playerIsAlive == True and gameWon == False): 

	command = input("> ")
	parser = Parse()
	action, room, direction, item, objects = parser.parse_user_input(command)

	if (action is not None):
		action = action.lower()
	if (action == 'go') :
		if (room is not None or direction is not None):
			goToRoom(direction, room)
		else:
			print("I need a room or a direction!")

	elif (action == 'look'):
		look()

	elif (action == 'look at'):
		lookAt(item)

	elif (action == 'take'):
		take(objects)

	elif (action == 'drop'):
		drop(objects)

	elif (action == 'inventory'):
		inventory()
	
	elif (action == 'help'):
		help()
	
	elif action == 'quit':
		exit()

	elif action is not None:
		performAction(action, item)

	else:
		print("I don't understand what you want to do. Type help for more information.")


