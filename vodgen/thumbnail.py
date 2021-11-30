import json
from PIL import ImageColor
class Thumbnail:
    def __init__(self, player1Name, player2Name, player1Character, player2Character, tournamentRound, gameName, barColor):
        self.player1_name = player1Name
        self.player2_name = player2Name
        self.player1_character = player1Character
        self.player2_character = player2Character
        
        #Convert "R1" for example to "Round 1"
        r = tournamentRound.split(" ")
        self.tournament_round = r[0] + " " + r[1].replace("R", "Round ")

        self.game_name = gameName
        self.bar_color = ImageColor(barColor, "RGB")

        #Constants?
        header = 128
        self.resolution = (1280, 720)
        self.player1_box = (0, 0, 640, header)
        self.player_font_size = 60
        self.vs_font_size = 120
        self.player2_box = (640, 0, 1280, header)
        self.round_box = (0, 592, 640, 720)
        self.game_box = (640, 592, 1280, 720)
        self.vs_box = (580, 239, 580+120, 239+110)

    def setLogoDir(self, logoDir):
        self.logo_dir = logoDir
    def setbaseDir(self, baseDir):
        self.base_dir = baseDir
    def setFontDir(self, fontDir):
        self.font_dir = fontDir
    def setVsFontDir(self, vsFontDir, size):
        self.vs_font_dir = vsFontDir
    def setCharacterImageDir(self, characterImageDir):
        self.character_image_dir = characterImageDir

    
    def readConfigFile(self):
        self.character_info = json.load(open('../assets/characterinfo.json'))

    def centerText(self, box, textWidth, textHeight):
        yoffset = 8
        x1, y1, x2, y2 = box
        box_width = x2 - x1
        box_height = y2 - y1
        text_coords = ((box_width-textWidth)/2+x1,(box_height-textHeight)/2+y1-yoffset)
        return text_coords
    

    def printAll(self):
        pass