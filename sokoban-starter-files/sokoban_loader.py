# sokoban_loader.py

# level files are lightly-edited screenshots from here:
# https://www.sokobanonline.com/play/community/bjertrup/sokomind-plus

from PIL import Image
from cmu_graphics import CMUImage
import pickle, os

COLORS = {
    'red':    (175,  71,  68),
    'green':  (114, 187, 81),
    'blue':   (67, 82, 182),
    'violet': (149, 69, 183),
    'cyan':   (101, 186, 187),
    'brown':  (147, 110, 47),
    'tan':    (245, 218, 131)
}

PIECE_COLORS = [ 'red', 'green', 'blue', 'violet', 'cyan' ]

def readPickleFile(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def writePickleFile(path, contents):
    with open(path, 'wb') as f:
        pickle.dump(contents, f)

def loadLevel(path):
    # first return a hardcoded level for testing purposes
    if path == None:
        return loadHardcodedLevel()
    elif os.path.exists(f'{path}.pickle'):
        return readPickleFile(f'{path}.pickle')
    else:
        level = []
        imageDict = {'w': None, 'p': None, 'r': None, 'g': None, 'b': None,
                     'v': None, 'c': None, 'R': None, 'G': None, 'B': None, 
                     'V': None, 'C': None, '-': None}

        levelNumber, levelRows, levelCols = readFileName(path)
        image = Image.open(path)
        width = image.width
        height = image.height
        cellLength = (width // levelCols) 
        for row in range(levelRows):           
            newRow = []                        
            for col in range(levelCols):
                pixelCount = {'red': 0, 'green': 0, 'blue': 0, 'violet': 0,
                              'cyan': 0, 'brown': 0, 'tan': 0}

                for pixRow in range(cellLength - 5):
                    for pixCol in range(cellLength - 5):
                        r, g, b = image.getpixel((cellLength * col + pixCol,
                                                  cellLength * row + pixRow))
                        for key in COLORS:
                            if isWithinEucDist((r, g, b), COLORS[key]):
                                pixelCount[key] += 1
                if pixelCount['brown'] > 500:
                    newRow.append('w')
                elif pixelCount['tan'] > 50 and pixelCount['blue'] > 50:
                    newRow.append('p')
                else:
                    foundColor = False
                    for color in PIECE_COLORS:
                        if pixelCount[color] > 2000: #appends capital letter
                            newRow.append(color[0])
                            foundColor = True
                            break
                        elif pixelCount[color] > 600: #appends lowercase letter
                            newRow.append(chr(ord(color[0]) - 32))
                            foundColor = True
                            break
                    if foundColor == False:
                        newRow.append('-') 
            level.append(newRow)

        for row in level:
            for col in row:
                if imageDict[col] == None:
                    rowI = level.index(row)
                    colI = row.index(col)
                    subImage = image.crop((cellLength * colI + 3, cellLength * rowI + 3,
                                          cellLength * colI + cellLength - 1,
                                          cellLength * rowI + cellLength - 1)) #used to be - 3
                    imageDict[col] = CMUImage(subImage)

    writePickleFile(f'{path}.pickle', (level, imageDict))

    return (level, imageDict)

def isWithinEucDist(rgb, color):
    r1, g1, b1 = rgb
    r2, g2, b2 = color 
    if (((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2) <= 20**2):
        return True
    else:
        return False

def readFileName(name):
    currNumberType = 0
    lastChar = None
    levelNumber = ''
    levelRows = ''
    levelCols = ''
    for c in name:
        if c.isdigit():
            if currNumberType == 0:
                levelNumber += c 
            elif currNumberType == 1:
                levelRows += c 
            elif currNumberType == 2:
                levelCols += c   
            lastChar = c
        elif lastChar != None and lastChar.isdigit():
            currNumberType += 1
    return int(levelNumber), int(levelRows), int(levelCols)

def loadHardcodedLevel():
    level = [ [ '-', '-', '-', '-', '-', '-', 'w', 'w', 'w', 'w' ],
          [ '-', '-', '-', '-', 'w', 'w', 'w', 'R', 'R', 'w' ],
          [ '-', '-', '-', '-', 'w', '-', '-', 'G', 'B', 'w' ],
          [ '-', '-', '-', '-', 'w', '-', 'r', 'R', 'R', 'w' ],
          [ 'w', 'w', 'w', 'w', 'w', 'w', '-', '-', 'w', 'w' ],
          [ 'w', 'p', '-', '-', '-', '-', '-', 'w', 'w', 'w' ],
          [ 'w', 'w', '-', 'g', '-', 'r', '-', 'r', '-', 'w' ],
          [ '-', 'w', '-', 'b', 'r', 'w', '-', 'w', '-', 'w' ],
          [ '-', 'w', '-', '-', '-', 'w', '-', '-', '-', 'w' ],
          [ '-', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w' ] ]
    images = {'w': 'w', '-': '-'}
    return level, images

def testSokobanLoader():
    print('Testing sokoban_loader...')
    files = ['level1-10x10.png',
             'level2-7x9.png',
             'level3-8x6.png',
             'level4-8x6.png']
    
    correctLevels = [
        # level1-10x10.png
        [ [ '-', '-', '-', '-', '-', '-', 'w', 'w', 'w', 'w' ],
          [ '-', '-', '-', '-', 'w', 'w', 'w', 'R', 'R', 'w' ],
          [ '-', '-', '-', '-', 'w', '-', '-', 'G', 'B', 'w' ],
          [ '-', '-', '-', '-', 'w', '-', 'r', 'R', 'R', 'w' ],
          [ 'w', 'w', 'w', 'w', 'w', 'w', '-', '-', 'w', 'w' ],
          [ 'w', 'p', '-', '-', '-', '-', '-', 'w', 'w', 'w' ],
          [ 'w', 'w', '-', 'g', '-', 'r', '-', 'r', '-', 'w' ],
          [ '-', 'w', '-', 'b', 'r', 'w', '-', 'w', '-', 'w' ],
          [ '-', 'w', '-', '-', '-', 'w', '-', '-', '-', 'w' ],
          [ '-', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w' ] ],

        # level2-7x9.png
        [ [ 'w', 'w', 'w', 'w', 'w', 'w', '-', '-', '-' ],
          [ 'w', 'R', 'G', 'B', 'V', 'w', 'w', 'w', 'w' ],
          [ 'w', 'p', '-', 'r', 'g', 'b', '-', '-', 'w' ],
          [ 'w', 'w', '-', '-', 'v', '-', '-', '-', 'w' ],
          [ '-', 'w', 'w', 'w', 'w', '-', 'w', '-', 'w' ],
          [ '-', '-', '-', '-', 'w', '-', '-', '-', 'w' ],
          [ '-', '-', '-', '-', 'w', 'w', 'w', 'w', 'w' ] ],
        
        # level3-8x6.png
        [ [ 'w', 'w', 'w', 'w', 'w', 'w' ],
          [ 'w', '-', '-', 'p', '-', 'w' ],
          [ 'w', '-', 'r', '-', '-', 'w' ],
          [ 'w', 'w', '-', 'w', 'g', 'w' ],
          [ 'w', '-', 'b', 'v', '-', 'w' ],
          [ 'w', '-', '-', 'c', 'B', 'w' ],
          [ 'w', 'C', 'R', 'V', 'G', 'w' ],
          [ 'w', 'w', 'w', 'w', 'w', 'w' ] ],
        
        # level4-8x6.png
        [ [ 'w', 'w', 'w', 'w', 'w', 'w' ],
          [ 'w', 'B', 'G', 'p', 'R', 'w' ],
          [ 'w', '-', '-', 'r', '-', 'w' ],
          [ 'w', 'w', 'g', 'w', 'w', 'w' ],
          [ 'w', '-', '-', 'b', '-', 'w' ],
          [ 'w', '-', '-', '-', '-', 'w' ],
          [ 'w', '-', '-', '-', '-', 'w' ],
          [ 'w', 'w', 'w', 'w', 'w', 'w' ] ]

    ]

    for i in range(len(files)):
        file = files[i]
        correctLevel = correctLevels[i]
        level, images = loadLevel(file)
        if level != correctLevel:
            print(f'{file} is incorrect!')
            print('Correct result:')
            print(correctLevel)
            print('Your result:')
            print(level)
            assert(False)
        print(f'  {file} is correct')
    print('Passed!')

if __name__ == '__main__':
    testSokobanLoader()