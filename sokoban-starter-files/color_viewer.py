# color_viewer.py

from cmu_graphics import *
from urllib.request import urlopen
from PIL import Image

def onAppStart(app, path):
    app.path = path
    app.PILImage = Image.open(app.path)
    app.PILImageWidth = app.PILImage.width
    app.PILImageHeight = app.PILImage.height
    app.width = app.PILImageWidth + 20
    app.height = app.PILImageHeight + 80
    app.CMUImage = CMUImage(app.PILImage)
    app.imageTopLeft = (10, 80)
    app.imageBottomLeft = (app.width - 15, app.height)

    app.mouseX = 'N/A'
    app.mouseY = 'N/A'
    app.r = 'N/A'
    app.g = 'N/A'
    app.b = 'N/A'

def onMouseMove(app, mouseX, mouseY):
    if not ((mouseX < app.imageTopLeft[0]) or 
            (mouseX > app.imageBottomLeft[0] + 4) or 
            (mouseY < app.imageTopLeft[1] + 10) or 
            (mouseY > app.imageBottomLeft[1])):
        app.r, app.g, app.b = app.PILImage.getpixel((mouseX - 10, mouseY - 90))
        app.mouseX = mouseX - 10
        app.mouseY = mouseY - 90
    else:
        app.r, app.g, app.b = 'N/A', 'N/A', 'N/A'
        app.mouseX = 'N/A'
        app.mouseY = 'N/A'

def redrawAll(app):
    drawLabel('Color Viewer', app.width/2, 20, size=16, bold=True)
    drawLabel(f'file = {app.path}', app.width/2, 35, size=14)
    drawLabel(f'({app.mouseX}, {app.mouseY}): ({app.r}, {app.g}, {app.b})', app.width/2, 60, size=14)
    drawLine(10, 80, app.width - 10, 80, lineWidth=2)
    drawImage(app.CMUImage, (app.PILImageWidth + 20)/2, (app.PILImageHeight + 80)/2 + 50, align='center')

runApp(path='level3-8x6.png')