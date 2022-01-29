"""Module to create a thumbnail, given enough information"""

import json
from PIL import ImageColor
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageOps
from PIL import ImageChops
import numpy as np

class Thumbnail:
    """The thumbnail class, containing all necessary information to create a thumbnail,
     and methods to actually create a png"""
     # pylint: disable=too-few-public-methods
    def __init__(self, players, match, image_info, config, title):
        self.players = players
        self.match = match
        self.image_info = image_info
        self.config = config
        self.title = title

    def print_all(self, players):
        """Create all the thumbnails for comparison between left-right"""
        self.players = players
    def create_thumbnail(self):
        base_image = Image.open(self.config.base_dir).convert("RGBA")
        banner = Image.open(self.config.banner_dir).convert("RGBA")
        if len(self.players) == 4:
            font_size = 35
        else:
            font_size = 60
        font = ImageFont.truetype(self.config.font_dir, 60)
        vs_font = ImageFont.truetype(self.config.vs_font_dir, 120)
        player_font = ImageFont.truetype(self.config.font_dir, font_size)
        game_name = self.match.game_name
        draw = ImageDraw.Draw(base_image)
        boxes = [self.image_info.player1_box, self.image_info.player2_box, self.image_info.round_box, self.image_info.game_box]
        #for box in boxes:
        #    draw.rectangle(box, fill=self.config.bar_color, outline=self.config.bar_color)
        
        with open('./characterinfo.json', encoding="utf-8") as file:
            character_info = json.load(file)
            print(self.players)
            player_names = []
            for player in self.players:
                img = Image.open(player.characterDir).convert("RGBA")
                offset = 0
                
                if len(self.players) == 4:
                    if not "head" in character_info[game_name][player.character]:
                        if character_info[game_name][player.character]["placement"] == "forward":
                            width, height = img.size
                            newWidth = round(width / 2)
                            img.crop((0,0, newWidth, height))
                        elif character_info[game_name][player.character]["placement"] == "backward":
                            width, height = img.size
                            img.crop((width*2,0, width, height))
                        else:
                            width, height = img.size
                            img.crop((int(width * 0.25),0, int(width * 0.75), height))
                    else:
                        if character_info[game_name][player.character]["head"] == "right":
                            width, height = img.size
                            img = img.crop((int(width * 0.3), 0, int(width * 0.80), height))
                        elif character_info[game_name][player.character]["head"] == "left":
                            width, height = img.size
                            img = img.crop((0, 0, int(width * 0.75), height))
                        else:
                            print("fuck")
                
                img = resizeCrop(img, player.character, game_name, len(self.players))
                if player.character in character_info[game_name]:
                    if character_info[game_name][player.character]["looking"] == "left" and player.number <= len(self.players)/2:
                        img = ImageOps.mirror(img)
                        print("mirroring left")
                    elif character_info[game_name][player.character]["looking"] == "right" and int(player.number) > len(self.players)/2:
                        img = ImageOps.mirror(img)
                        print("mirroring right side ")
                    if character_info[game_name][player.character]["placement"] == "forward":
                        if player.number % 2 == 0:
                            offset = round(320 * 0.15)
                        else:
                            offset = -round(320 * 0.15)
                    elif character_info[game_name][player.character]["placement"] == "backward":
                        if player.number % 2 == 0:
                            offset = -round(320 * 0.15)
                        else:
                            offset = round(320 * 0.15)
                

                print(offset)                        
                if len(self.players) == 4:
                    player_map = {
                        1: (0 - offset, 128, int(640/2) - offset, 464 + 128),
                        2: (int(640/2) - offset, 128, 640 - offset, 464 + 128),
                        3: (640, 128, (640+int(640/2)), 464 + 128),
                        4: ((640+int(640/2)), 128, 1280, 464 + 128)
                    }
                else:
                    player_map = {
                        1: (0 - offset, 128, 640 - offset, 464 + 128),
                        2: (640, 128, 1280, 464 + 128)
                    }
                if len(self.players) == 4:
                    box_map = {
                        1: (0, 0, int(640/2), 128),
                        2: (int(640/2), 0, 640, 128),
                        3: (640, 0, int(640*1.5), 128),
                        4: (int(640*1.5), 0, 1280, 128)
                    }
                else:
                    box_map = {
                        1: (0, 0, 640, 128),
                        2: (640, 0, 1280, 128)
                    }
                base_image.paste(img, player_map[player.number], img)
                player_text = player.name.upper()
                text_width, text_height = draw.textsize(player_text, font=player_font)
                text_coordinates = center_text(box_map[player.number], text_width, text_height)
                player_names.append({
                    "name": player_text,
                    "coords": text_coordinates
                })


            
            base_image.paste(banner, (0,0), banner)
            for entry in player_names:
                draw.text(entry["coords"], entry["name"], self.config.font_color, font=player_font)
            
            text = "VS"
            shadow_color = "black"
            text_width, text_height = draw.textsize(text, font=vs_font)
            text_coords = center_text(self.image_info.vs_box, text_width, text_height)
            draw.text(((text_coords[0]-1, text_coords[1]-1)), text, font=vs_font, fill=shadow_color)
            draw.text(((text_coords[0]+1, text_coords[1]-1)), text, font=vs_font, fill=shadow_color)
            draw.text(((text_coords[0]-1, text_coords[1]+1)), text, font=vs_font, fill=shadow_color)
            draw.text(((text_coords[0]+1, text_coords[1]+1)), text, font=vs_font, fill=shadow_color)
            draw.text(text_coords, text, self.config.font_color, font=vs_font)
            
            text = self.match.tournament_round.upper()
            text_width, text_height = font.getsize(text)
            text_coords = center_text(self.image_info.round_box, text_width, text_height)
            draw.text(text_coords, text, self.config.font_color, font=font)
            
            text = self.match.game_name_thumbnail.upper()
            text_width, text_height = font.getsize(text)
            text_coords = center_text(self.image_info.game_box, text_width, text_height)
            draw.text(text_coords, text, self.config.font_color, font=font)

            logo = Image.open(self.config.logo_dir).convert("RGBA")
            logo = logo.resize((182, 181))
            width, height = logo.size
            coords = (547, 380, width+547, height+380)
            base_image.paste(logo, coords, logo)
            
            base_image.save(self.config.output_dir + self.title + ".png")
            


class ImageInfo:
    """Contains image on how to image is going to look,
     and how big the different elements are going to be in the image"""
     # pylint: disable=too-few-public-methods
     # pylint: disable=too-many-instance-attributes
    def __init__(self):
        self.resolution = (1280, 720)
        self.header = int(self.resolution[1] / 5.625)
        self.player1_box = (0, 0, 640, self.header)
        self.player_font_size = 60
        self.vs_font_size = 120
        self.player2_box = (640, 0, 1280, self.header)
        self.round_box = (0, 592, 640, 720)
        self.game_box = (640, 592, 1280, 720)
        self.vs_box = (580, 239, 580+120, 239+110)
class MatchInfo:
    """Contains info about the match which the thumbnail is for"""
    def __init__(self, game_name, tournament_string):
        string_array = tournament_string.split(" ")
        tournament_round = string_array[0] + " " + string_array[1].replace("R", "Round ")
        
        self.tournament_round = tournament_round
        with open('./config.json', encoding="utf-8") as file:
            config = json.load(file)
            self.game_name_thumbnail = config["game"][game_name]["title"]
        self.game_name = game_name

    def set_tournament_round(self, tournament_string):
        """Set the tournament around,
         and parse it for a more condensed title suitable for sites like YouTube"""
        string_array = tournament_string.split(" ")
        tournament_round = string_array[0] + " " + string_array[1].replace("R", "Round ")
        self.tournament_round = tournament_round

    def set_game_name(self, game_name):
        """Set the game name for the match"""
        self.game_name = game_name


class Player:
    """
    Contains player information
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, player_name, character, team, number):
        self.name = player_name
        self.character = character
        self.characterDir = None
        self.team = team
        self.number = number
        fileName = self.character.lower().replace(" ", "_") + "_00.png"
        self.characterDir = f"./assets/characters/ssbm/{self.character}/{fileName}"

    def setCharacterDir(self, imageDir):
        fileName = self.character.lower().replace(" ", "_") + "_00.png"
        self.characterDir = f"{imageDir}/{self.character}/{fileName}"



class Config:
    """Contains information about directories, and reads the config.json to get this info"""
    def __init__(self, game_name, tournament_name):
        self.logo_dir = None
        self.base_dir = None
        self.font_dir = None
        self.vs_font_dir = None
        self.font_color = None
        self.banner_dir = None
        self.character_image_dir = None
        self.bar_color = None
        self.output_dir = None

        self.read_config(game_name, tournament_name)

    def read_config(self, game_name, tournament_name):
        """Reads through the config.json and sets the appropriate values"""
        with open('./config.json', encoding="utf-8") as file:
            config = json.load(file)
            self.base_dir = config["game"][game_name]["background_image_dir"]
            self.character_image_dir = config["game"][game_name]["character_images"]
            
            self.logo_dir = config["tournament"][tournament_name]["logo_dir"]
            print(self.logo_dir)
            self.banner_dir = config["tournament"][tournament_name]["banner_dir"]
            self.output_dir = config["tournament"][tournament_name]["output_dir"]
            self.font_dir = config["tournament"][tournament_name]["main_font"]
            self.vs_font_dir = config["tournament"][tournament_name]["vs_font"]
            self.bar_color = ImageColor.getcolor(config["tournament"][tournament_name]["thumbnail_primary_color"], "RGB")
                
def center_text(box, text_width, text_height):
    """Centers text, given dimensions and width and height"""
    y_offset = 8
    x_1, y_1, x_2, y_2 = box
    box_width = x_2 - x_1
    box_height = y_2 - y_1
    text_coords = ((box_width-text_width)/2+x_1,(box_height-text_height)/2+y_1-y_offset)
    return text_coords



def resizeCrop(img, character, game, player_num):
    portraitHeight = 464
    portraitWidth = 1280 / player_num
    #Resize image based on max height in template
    aspectRatio = img.size[0] / img.size[1]
    portraitResolution = (round(portraitHeight * 1.3 * aspectRatio), round(1.3 * portraitHeight))
    characterInfo = json.load(open("characterinfo.json"))
    
    img = img.resize(portraitResolution)

    width, height = img.size
    offsetWidth = (width - portraitWidth)
    if character in characterInfo[game]:
        if characterInfo[game][character]["placement"] == "center":
            offsetWidth /= 2
            coords = (offsetWidth, 0, width - offsetWidth, portraitHeight)
        elif characterInfo[game][character]["placement"] == "forward":
            coords = (offsetWidth, 0, width, portraitHeight)
        elif characterInfo[game][character]["placement"] == "backward":
            coords = (0, 0, width - offsetWidth, portraitHeight)
        elif characterInfo[game][character]["placement"] == "upward":
            offsetHeight = round(portraitHeight * 0.2)
            offsetWidth /= 2
            coords = (offsetWidth, offsetHeight, width - offsetWidth, portraitHeight + offsetHeight)
        elif characterInfo[game][character]["placement"] == "downward":
            offsetHeight = round(portraitHeight * 0.4)
            print("test")
            offsetWidth /= 2
            coords = (offsetWidth, 0, width - offsetWidth, portraitHeight)
        else: 
            offsetWidth /= 2
            coords = (offsetWidth, 0, width - offsetWidth, portraitHeight)
        #If nothing is specified in file, just center the image
    else:
        offsetWidth /= 2
        coords = (offsetWidth, 0, width - offsetWidth, portraitHeight)

    img = img.crop(coords)
    return img


if __name__ == '__main__':
    players = [Player("ove", "Sheik", 0, 1), Player("Kise Seryuu", "Fox", 0, 2), Player("Class Ganon", "Snake", 1, 3), Player("Juice Nasty", "K Rool", 1, 4)]
    match = MatchInfo("SSBM", "Winners R1")
    image_info = ImageInfo()
    config = Config()
    thumbnail = Thumbnail(players, match, image_info, config)
    thumbnail.create_thumbnail()