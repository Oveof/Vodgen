"""Module to create a thumbnail, given enough information"""

import json
#from PIL import ImageColor

class Thumbnail:
    """The thumbnail class, containing all necessary information to create a thumbnail,
     and methods to actually create a png"""
    def __init__(self, players, match, image_info, config):
        self.players = players
        self.match = match
        self.image_info = image_info
        self.config = config

    """Create all the thumbnails for comparison between left-right"""
    def print_all(self, players):
        self.players = players

class ImageInfo:
    """Contains image on how to image is going to look,
     and how big the different elements are going to be in the image"""
     # pylint: disable=too-few-public-methods
    def __init__(self):
        header = 128
        self.resolution = (1280, 720)
        self.player1_box = (0, 0, 640, header)
        self.player_font_size = 60
        self.vs_font_size = 120
        self.player2_box = (640, 0, 1280, header)
        self.round_box = (0, 592, 640, 720)
        self.game_box = (640, 592, 1280, 720)
        self.vs_box = (580, 239, 580+120, 239+110)
class MatchInfo:
    """Contains info about the match which the thumbnail is for"""
    def __init__(self, game_name):
        self.tournament_round = None
        self.game_name = game_name

    def set_tournament_round(self, tournament_string):
        """Set the tournament around,
         and parse it for a more condensed title suitable for sites like YouTube"""
        string_array = tournament_string.split(" ")
        tournamnet_round = string_array[0] + " " + string_array[1].replace("R", "Round ")
        self.tournament_round = tournamnet_round

    def set_game_name(self, game_name):
        """Set the game name for the match"""
        self.game_name = game_name


class Player:
    """
    Contains player information
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, player_name, character):
        self.player_name = player_name
        self.character = character


class Config:
    """Contains information about directories, and reads the config.json to get this info"""
    # pylint: disable=too-few-public-methods
    def __init__(self):
        self.logo_dir = None
        self.base_dir = None
        self.font_dir = None
        self.vs_font_dir = None
        self.character_image_dir = None
        self.bar_color = None
    """Reads through the config.json and sets the appropriate values"""
    def read_config(self):
        self.character_info = json.load(open('../assets/characterinfo.json', encoding="utf-8"))
        #ImageColor(bar_color, "RGB")

def center_text(box, text_width, text_height):
    """Centers text, given dimensions and width and height"""
    y_offset = 8
    x_1, y_1, x_2, y_2 = box
    box_width = x_2 - x_1
    box_height = y_2 - y_1
    text_coords = ((box_width-text_width)/2+x_1,(box_height-text_height)/2+y_1-y_offset)
    return text_coords
