# sokoban_player.py

from cmu_graphics import *
from sokoban_loader import *
import copy

COLORS = {
    'red':    (175,  71,  68),
    'green':  (114, 187, 81),
    'blue':   (67, 82, 182),
    'violet': (149, 69, 183),
    'cyan':   (101, 186, 187),
    'brown':  (147, 110, 47),
    'tan':    (245, 218, 131)
}

def onAppStart(app, useHardcodedLevel):
	app.useHardcodedLevel = useHardcodedLevel
	app.path = 'level1-10x10.png'
	app.currLevel = 1
	app.destDict = dict()
	app.moves = []
	app.level, app.image = loadLevel(app.path)
	loadLevelImages(app, app.path)
	app.levelCenterX = 300
	app.levelCenterY = 350

	if app.useHardcodedLevel == True:
		app.level, app.image = loadLevel(None)
		print(app.image)

def loadLevelImages(app, path):
	app.destDict = dict()
	app.moves = []
	app.levelNum, app.rows, app.cols = readFileName(path)
	app.win = False
	aspectRatio = (15/12)
	if (app.cols / app.rows) > aspectRatio: #if the level is fat
		app.cellSize = 580 // app.cols
		app.levelLeft = 10
		app.levelTop = (480 - app.cellSize * app.rows)//2 + 110
	else:
		app.cellSize = 480 // app.rows
		app.levelLeft = (600 - app.cellSize * app.cols)//2
		app.levelTop = 110

	for rowI in range(len(app.level)):
		for colI in range(app.cols):
			if app.level[rowI][colI] == 'p':
				app.playerIndex = [rowI, colI]
			elif app.level[rowI][colI] in 'RGBVC':
				app.destDict[str((rowI, colI))] = app.level[rowI][colI]

	app.moves.append((copy.deepcopy(app.level), copy.deepcopy(app.playerIndex)))

def onKeyPress(app, key):
	if ((key == 'up') or (key == 'right') or 
	    (key == 'down') or (key == 'left')):
		movePlayer(app, key)
	elif key == '1':
		app.currLevel = 1
		app.path = 'level1-10x10.png'
		app.level, app.image = loadLevel(app.path)
		loadLevelImages(app, app.path)
	elif key == '2':
		app.currLevel = 2
		app.path = 'level2-7x9.png'
		app.level, app.image = loadLevel(app.path)
		loadLevelImages(app, app.path)
	elif key == '3':
		app.currLevel = 3
		app.path = 'level3-8x6.png'
		app.level, app.image = loadLevel(app.path)
		loadLevelImages(app, app.path)
	elif key == '4':
		app.currLevel = 4
		app.path = 'level4-8x6.png'
		app.level, app.image = loadLevel(app.path)
		loadLevelImages(app, app.path)
	elif key == 'u' and len(app.moves) > 1:
		app.moves.pop()
		app.level = copy.deepcopy(app.moves[-1][0])
		app.playerIndex = copy.deepcopy(app.moves[-1][1])
	elif key == 'r':
		onKeyPress(app, str(app.currLevel))
	elif key == 'a' and app.levelNum == 1:
		app.playerIndex = [2, 5]
		app.level =  [ [ '-', '-', '-', '-', '-', '-', 'w', 'w', 'w', 'w' ],
	          			   [ '-', '-', '-', '-', 'w', 'w', 'w', 'r', 'r', 'w' ],
	          			   [ '-', '-', '-', '-', 'w', 'p', 'g', 'G', 'b', 'w' ],
	          			   [ '-', '-', '-', '-', 'w', '-', '-', 'r', 'r', 'w' ],
	          			   [ 'w', 'w', 'w', 'w', 'w', 'w', '-', '-', 'w', 'w' ],
	          			   [ 'w', '-', '-', '-', '-', '-', '-', 'w', 'w', 'w' ],
	          			   [ 'w', 'w', '-', '-', '-', '-', '-', '-', '-', 'w' ],
	          			   [ '-', 'w', '-', '-', '-', 'w', '-', 'w', '-', 'w' ],
	          			   [ '-', 'w', '-', '-', '-', 'w', '-', '-', '-', 'w' ],
	          			   [ '-', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w' ] ]

	app.win = True
	for row in app.level:
		for col in row:
			if col in 'RGBVC':
				app.win = False

def movePlayer(app, key): #This is not repeated code. It must be written like this. I tried for about an hour to rewrite it, but it doesn't work.
	if key == 'up':  
		if app.level[app.playerIndex[0] - 1][app.playerIndex[1]] in '-RGBVC':
			if str((app.playerIndex[0], app.playerIndex[1])) in app.destDict:
				app.level[app.playerIndex[0]][app.playerIndex[1]] = (
					app.destDict[str((app.playerIndex[0], app.playerIndex[1]))])
			else:
				app.level[app.playerIndex[0]][app.playerIndex[1]] = '-'
			app.level[app.playerIndex[0] - 1][app.playerIndex[1]] = 'p'
			app.playerIndex[0] -= 1
			app.moves.append((copy.deepcopy(app.level), copy.deepcopy(app.playerIndex)))

		elif (app.level[app.playerIndex[0] - 1][app.playerIndex[1]] in 'rgbvc' and
			app.level[app.playerIndex[0] - 2][app.playerIndex[1]] in '-RGBVC'):
			app.level[app.playerIndex[0] - 2][app.playerIndex[1]] = (
				app.level[app.playerIndex[0] - 1][app.playerIndex[1]])

			if str((app.playerIndex[0], app.playerIndex[1])) in app.destDict:
				app.level[app.playerIndex[0]][app.playerIndex[1]] = (
					app.destDict[str((app.playerIndex[0], app.playerIndex[1]))])
			else:
				app.level[app.playerIndex[0]][app.playerIndex[1]] = '-'
			app.level[app.playerIndex[0] - 1][app.playerIndex[1]] = 'p'
			app.playerIndex[0] -= 1
			app.moves.append((copy.deepcopy(app.level), copy.deepcopy(app.playerIndex)))

	elif key == 'down':
		if app.level[app.playerIndex[0] + 1][app.playerIndex[1]] in '-RGBVC':
			if str((app.playerIndex[0], app.playerIndex[1])) in app.destDict:
				app.level[app.playerIndex[0]][app.playerIndex[1]] = (
					app.destDict[str((app.playerIndex[0], app.playerIndex[1]))])
			else:
				app.level[app.playerIndex[0]][app.playerIndex[1]] = '-'
			app.level[app.playerIndex[0] + 1][app.playerIndex[1]] = 'p'
			app.playerIndex[0] += 1
			app.moves.append((copy.deepcopy(app.level), copy.deepcopy(app.playerIndex)))

		elif (app.level[app.playerIndex[0] + 1][app.playerIndex[1]] in 'rgbvc' and
			app.level[app.playerIndex[0] + 2][app.playerIndex[1]] in '-RGBVC'):
			app.level[app.playerIndex[0] + 2][app.playerIndex[1]] = (
				app.level[app.playerIndex[0] + 1][app.playerIndex[1]])
			if str((app.playerIndex[0], app.playerIndex[1])) in app.destDict:
				app.level[app.playerIndex[0]][app.playerIndex[1]] = (
					app.destDict[str((app.playerIndex[0], app.playerIndex[1]))])
			else:
				app.level[app.playerIndex[0]][app.playerIndex[1]] = '-'
			app.level[app.playerIndex[0] + 1][app.playerIndex[1]] = 'p'
			app.playerIndex[0] += 1
			app.moves.append((copy.deepcopy(app.level), copy.deepcopy(app.playerIndex)))

	if key == 'right':
		if app.level[app.playerIndex[0]][app.playerIndex[1] + 1] in '-RGBVC':
			if str((app.playerIndex[0], app.playerIndex[1])) in app.destDict:
				app.level[app.playerIndex[0]][app.playerIndex[1]] = (
					app.destDict[str((app.playerIndex[0], app.playerIndex[1]))])
			else:
				app.level[app.playerIndex[0]][app.playerIndex[1]] = '-'
			app.level[app.playerIndex[0]][app.playerIndex[1] + 1] = 'p'
			app.playerIndex[1] += 1
			app.moves.append((copy.deepcopy(app.level), copy.deepcopy(app.playerIndex)))

		elif (app.level[app.playerIndex[0]][app.playerIndex[1] + 1] in 'rgbvc' and
			app.level[app.playerIndex[0]][app.playerIndex[1] + 2] in '-RGBVC'):
			app.level[app.playerIndex[0]][app.playerIndex[1] + 2] = (
				app.level[app.playerIndex[0]][app.playerIndex[1] + 1])
			if str((app.playerIndex[0], app.playerIndex[1])) in app.destDict:
				app.level[app.playerIndex[0]][app.playerIndex[1]] = (
					app.destDict[str((app.playerIndex[0], app.playerIndex[1]))])
			else:
				app.level[app.playerIndex[0]][app.playerIndex[1]] = '-'
			app.level[app.playerIndex[0]][app.playerIndex[1] + 1] = 'p'
			app.playerIndex[1] += 1
			app.moves.append((copy.deepcopy(app.level), copy.deepcopy(app.playerIndex)))

	elif key == 'left':
		if app.level[app.playerIndex[0]][app.playerIndex[1] - 1] in '-RGBVC':
			if str((app.playerIndex[0], app.playerIndex[1])) in app.destDict:
				app.level[app.playerIndex[0]][app.playerIndex[1]] = (
					app.destDict[str((app.playerIndex[0], app.playerIndex[1]))])
			else:
				app.level[app.playerIndex[0]][app.playerIndex[1]] = '-'
			app.level[app.playerIndex[0]][app.playerIndex[1] - 1] = 'p'
			app.playerIndex[1] -= 1
			app.moves.append((copy.deepcopy(app.level), copy.deepcopy(app.playerIndex)))

		elif (app.level[app.playerIndex[0]][app.playerIndex[1] - 1] in 'rgbvc' and
			app.level[app.playerIndex[0]][app.playerIndex[1] - 2] in '-RGBVC'):
			app.level[app.playerIndex[0]][app.playerIndex[1] - 2] = (
				app.level[app.playerIndex[0]][app.playerIndex[1] - 1])
			if str((app.playerIndex[0], app.playerIndex[1])) in app.destDict:
				app.level[app.playerIndex[0]][app.playerIndex[1]] = (
					app.destDict[str((app.playerIndex[0], app.playerIndex[1]))])
			else:
				app.level[app.playerIndex[0]][app.playerIndex[1]] = '-'
			app.level[app.playerIndex[0]][app.playerIndex[1] - 1] = 'p'
			app.playerIndex[1] -= 1
			app.moves.append((copy.deepcopy(app.level), copy.deepcopy(app.playerIndex)))

	

def redrawAll(app):
	drawLabel('Sokoban!', app.width/2, 20, size=16, bold=True)
	drawLabel('Use arrow keys to solve the puzzle', app.width/2, 35, size=14)
	drawLabel('Press u to undo moves, r to reset level', app.width/2, 50, size=14)
	drawLabel('Press 1,2,3,4 to play different levels', app.width/2, 65, size=14)
	drawLabel(f'Level {app.currLevel}', app.width/2, 80, size=14)
	drawLine(10, 95, app.width - 10, 95, lineWidth=3)

	for rowI in range(app.rows):
		for colI in range(app.cols):
			drawn = False
			if app.useHardcodedLevel == True:
				drawLabel(app.level[rowI][colI],
					      app.cellSize * colI + app.levelLeft,
					      app.cellSize * rowI + app.levelTop, 
					      size=24)
			elif ((str((rowI, colI)) in app.destDict) and
				(app.level[rowI][colI] in 'rgbvc')):
				if (app.level[rowI][colI] == 'r' and
					app.destDict[str((rowI, colI))] == 'R' ):
					color = COLORS['red']
					drawRect(app.cellSize * colI + app.levelLeft,
						     app.cellSize * rowI + app.levelTop, 
						     app.cellSize, app.cellSize, 
						     fill=rgb(color[0], color[1], color[2]))
					drawn = True
				elif (app.level[rowI][colI] == 'g' and
					app.destDict[str((rowI, colI))] == 'G' ):
					color = COLORS['green']
					drawRect(app.cellSize * colI + app.levelLeft,
						     app.cellSize * rowI + app.levelTop, 
						     app.cellSize, app.cellSize, 
						     fill=rgb(color[0], color[1], color[2]))
					drawn = True
				elif (app.level[rowI][colI] == 'b' and
					app.destDict[str((rowI, colI))] == 'B' ):
					color = COLORS['blue']
					drawRect(app.cellSize * colI + app.levelLeft,
						     app.cellSize * rowI + app.levelTop, 
						     app.cellSize, app.cellSize, 
						     fill=rgb(color[0], color[1], color[2]))
					drawn = True
				elif (app.level[rowI][colI] == 'v' and
					app.destDict[str((rowI, colI))] == 'V' ):
					color = COLORS['violet']
					drawRect(app.cellSize * colI + app.levelLeft,
						     app.cellSize * rowI + app.levelTop, 
						     app.cellSize, app.cellSize, 
						     fill=rgb(color[0], color[1], color[2]))
					drawn = True
				elif (app.level[rowI][colI] == 'c' and
					app.destDict[str((rowI, colI))] == 'C' ):
					color = COLORS['cyan']
					drawRect(app.cellSize * colI + app.levelLeft,
						     app.cellSize * rowI + app.levelTop, 
						     app.cellSize, app.cellSize, 
						     fill=rgb(color[0], color[1], color[2]))
					drawn = True
			if drawn != True and app.useHardcodedLevel == False:
				drawImage(app.image[app.level[rowI][colI]], 
					      app.cellSize * colI + app.levelLeft,
					      app.cellSize * rowI + app.levelTop, 
					      width=app.cellSize, height=app.cellSize)

		if app.win == True:
			drawRect(10, 110, 580, 480, fill='green')
			drawLabel('You win!', app.width/2, 350, size=72, align='center')

runApp(600, 600, useHardcodedLevel=False)