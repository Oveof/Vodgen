import json
from PIL import ImageColor
class Thumbnail:
    def __init__(self, player1_name, player2_name, tournament_round, game_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_characters = None
        self.player2_characters = None

        r = tournament_round.split(" ")
        self.tournament_round = r[0] + " " + r[1].replace("R", "Round ")

        self.game_name = game_name
        self.bar_color = None

        header = 128
        self.resolution = (1280, 720)
        self.player1_box = (0, 0, 640, header)
        self.player_font_size = 60
        self.vs_font_size = 120
        self.player2_box = (640, 0, 1280, header)
        self.round_box = (0, 592, 640, 720)
        self.game_box = (640, 592, 1280, 720)
        self.vs_box = (580, 239, 580+120, 239+110)

        self.logo_dir = None
        self.base_dir = None
        self.font_dir = None
        self.vs_font_dir = None
        self.character_image_dir = None


    """
    Sets the logo directory
    """
    def set_logo_dir(self, logo_dir):
        self.logo_dir = logo_dir

    """
    Sets the base directory, which is the base image which gets modified for each thumbnail
    """
    def set_base_dir(self, base_dir):
        self.base_dir = base_dir

    """
    Sets the font directory
    """
    def set_font_dir(self, font_dir):
        self.font_dir = font_dir

    """
    Sets the vs font directory, which is usually in the middle of the screen
    """
    def set_vs_font_dir(self, vs_font_dir, size):
        self.vs_font_dir = vs_font_dir

    """"
    Sets the character image dir, where to look for all the character images
    """
    def set_character_image_dir(self, character_image_dir):
        self.character_image_dir = character_image_dir


    """
    Sets player 1 characters
    """
    def set_player1_characters(self, characters):
        self.player1_characters = characters


    """
    Sets the player 2 characters
    """
    def set_player2_characters(self, characters):
        self.player2_characters = characters


    #Reads the config again, and sets all the necessary properties
    def read_config(self):
        self.character_info = json.load(open('../assets/characterinfo.json'))
        #ImageColor(bar_color, "RGB")

    #Center the text
    def center_text(self, box, text_width, text_height):
        y_offset = 8
        x_1, y_1, x_2, y_2 = box
        box_width = x_2 - x_1
        box_height = y_2 - y_1
        text_coords = ((box_width-text_width)/2+x_1,(box_height-text_height)/2+y_1-y_offset)
        return text_coords


    def printAll(self):
        pass