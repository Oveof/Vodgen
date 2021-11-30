import json
from PIL import ImageColor
class Thumbnail:
    def __init__(self, player1Name, player2Name, player1Character, player2Character, tournamentRound, gameName, barColor):
        self.player1Name = player1Name
        self.player2Name = player2Name
        self.player1Character = player1Character
        self.player2Character = player2Character
        
        #Convert "R1" for example to "Round 1"
        r = tournamentRound.split(" ")
        self.tournamentRound = r[0] + " " + r[1].replace("R", "Round ")

        self.gameName = gameName
        self.barColor = ImageColor(barColor, "RGB")

        #Constants?
        header = 128
        self.resolution = (1280, 720)
        self.player1Box = (0, 0, 640, header)
        self.playerFontSize = 60
        self.vsFontSize = 120
        self.player2Box = (640, 0, 1280, header)
        self.roundBox = (0, 592, 640, 720)
        self.gameBox = (640, 592, 1280, 720)
        self.vsbox = (580, 239, 580+120, 239+110)

    def setLogoDir(self, logoDir):
        self.logoDir = logoDir
    def setbaseDir(self, baseDir):
        self.baseDir = baseDir
    def setFontDir(self, fontDir):
        self.fontDir = fontDir
    def setVsFontDir(self, vsFontDir, size):
        self.vsFontDir = vsFontDir
    def setCharacterImageDir(self, characterImageDir):
        self.characterImageDir = characterImageDir

    
    def readConfigFile(self):
        self.characterInfo = json.load(open('../assets/characterinfo.json'))

    def centerText(self, box, textWidth, textHeight):
        yoffset = 8
        x1, y1, x2, y2 = box
        boxWidth = x2 - x1
        boxHeight = y2 - y1
        textCoords = ((boxWidth-textWidth)/2+x1,(boxHeight-textHeight)/2+y1-yoffset)
        return textCoords
    

    def printAll(self):
        pass