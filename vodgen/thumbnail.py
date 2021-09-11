import json
class Thumbnail:
    def __init__(self, player1Name, player2Name, player1Character, player2Character, tournamentRound, gameName, resultFile):
        self.player1Name = player1Name
        self.player2Name = player2Name
        self.player1Character = player1Character
        self.player2Character = player2Character
        self.tournamentRound = tournamentRound
        self.gameName = gameName
        self.resultFile = resultFile

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
        
        #Read config file
        characterInfo = json.load(open('../assets/characterinfo.json'))
        config = json.load(open('../assets/config.json'))
    


    

    def centerText(self, box, textWidth, textHeight):
        yoffset = 8
        x1, y1, x2, y2 = box
        boxWidth = x2 - x1
        boxHeight = y2 - y1
        textCoords = ((boxWidth-textWidth)/2+x1,(boxHeight-textHeight)/2+y1-yoffset)
        return textCoords