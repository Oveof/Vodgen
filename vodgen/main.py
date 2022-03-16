"""Vodgen app"""
import sys
import json
import re
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox,
    QFileDialog, QLabel, QLineEdit, QMainWindow, QPlainTextEdit, QPushButton, QVBoxLayout, QWidget)
from videocutter import create_video
from thumbnail import Thumbnail, Player, Config, ImageInfo, MatchInfo

class Error(Exception):
    pass
class InvalidRoundName(Error):
    pass
class MissingPlayer1Character(Error):
    pass
class MissingPlayer2Character(Error):
    pass

def formatTitle(title):
    game_info = title.split(": ")[1].split(" - ")[0]
    tournament_round = ' '.join(game_info.split(' ')[-2:])
    #gameRound = gameInfo.split(' ', 2)
    game_name = game_info.split(' ')[0]
    if "Winners" in game_info:
        game_name = game_info.split(' Winners')[0]
    elif "Losers" in game_info:
        game_name = game_info.split(' Losers')[0]
    elif "Grand Finals" in game_info:
        game_name = game_info.split(' Grand')[0]
    else:
        raise InvalidRoundName()

    player_info = title.split("-")[1]
    team1 = player_info.split("vs")[0].strip()
    team1_players = team1.split("(")[0].split(" + ")
    team1_characters_search = re.search(r"\(([A-Za-z0-9_, .é+]+)\)", team1)
    if team1_characters_search == None:
        raise MissingPlayer1Character()
    team1_characters = team1_characters_search.group(1).split(", ")[0].split(" + ")

    team2 = player_info.split("vs")[1].strip()
    team2_players = team2.split("(")[0].split(" + ")
    team2_characters_search = re.search(r"\(([A-Za-z0-9_, .é+]+)\)", team2)
    if team2_characters_search == None:
        raise MissingPlayer2Character
    team2_characters = team2_characters_search.group(1).split(", ")[0].split(" + ")
    
    player_names = team1_players + team2_players
    player_characters = team1_characters + team2_characters

    player_list = []
    for x in range(len(player_names)):
        if len(player_names) / 2 > x:
            team_num = 0
        else:
            team_num = 1
        player_list.append(Player(player_names[x], player_characters[x], team_num, x+1))

    
    return player_list, tournament_round, game_name






class MainWindow(QMainWindow):
    """Main UI window"""
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Vodgen")
        layout = QVBoxLayout()

        self.choose_stream = QPushButton("Choose stream file")
        self.choose_stream.clicked.connect(self.choose_video_file)
        self.choose_region = QComboBox()
        self.choose_game = QComboBox()
        self.choose_banner = QPushButton("Choose Banner")
        self.choose_banner.clicked.connect(self.choose_banner_file)

        #Adds regions form config to dropdown menu
        with open('config.json', encoding="utf-8") as file:
            config = json.load(file)
            for attribute, _ in config["tournament"].items():
                self.choose_region.addItem(attribute)
            for attribute, _ in config["game"].items():
                self.choose_game.addItem(attribute)

        self.only_thumbnails = QCheckBox("Only thumbnails")
        self.create_videos_button = QPushButton("Generate VoDs and thumbnails")
        self.create_videos_button.clicked.connect(self.create_all)
        self.textbox = QPlainTextEdit()
        self.textbox.resize(280,40)
        self.choose_codec = QComboBox()
        self.choose_codec.addItem("")
        self.choose_codec.addItem("h264_nvenc")
        self.choose_codec.addItem("AMF")
        self.choose_stream_label = QLabel("")
        self.choose_banner_label = QLabel("")

        layout.addWidget(self.choose_region)
        layout.addWidget(self.choose_game)
        layout.addWidget(self.choose_stream)
        layout.addWidget(self.choose_stream_label)
        layout.addWidget(self.choose_banner)
        layout.addWidget(self.choose_banner_label)
        layout.addWidget(self.textbox)
        layout.addWidget(self.only_thumbnails)
        layout.addWidget(self.choose_codec)
        layout.addWidget(self.create_videos_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def choose_video_file(self):
        """Choose file helper method"""
        self.video_path = QFileDialog.getOpenFileName(self, "Select File")
        self.choose_stream_label.setText(self.video_path[0])
    def choose_banner_file(self):
        """Choose file helper method"""
        self.banner_path = QFileDialog.getOpenFileName(self, "Select File")
        self.choose_banner_label.setText(self.banner_path[0])
    def choose_dir(self):
        """Choose directory helper method"""
        return QFileDialog.getExistingDirectory(self, "Select Directory")
    
    def create_all(self):
        user_input = self.textbox.toPlainText().split("\n")
        for line in user_input:
            #start_time = line.split(" ")[0]
            #end_time = line.split(" ")[1]
            title = line.split(" ", 2)[2]
            start_time = line.split(" ")[0]
            end_time = line.split(" ")[1]
            try:
                player_list, tournament_round, game_name, = formatTitle(title)
            except InvalidRoundName:
                print("Invalid tournament round name on line: " + line )
                return 0
            except MissingPlayer1Character:
                print("Missing player 1 character name on line: " + line)
                return 0
            except MissingPlayer2Character:
                print("Missing player 2 character name on line: " + line)
                return 0
            
            match = MatchInfo(str(self.choose_game.currentText()), tournament_round)
            image_info = ImageInfo()
            config = Config(str(self.choose_game.currentText()), str(self.choose_region.currentText()))
            windows_title = title.replace("|", "¤")
            windows_title = windows_title.replace(":", "#")
            new_thumbnail = Thumbnail(player_list, match, image_info, config, windows_title)
            new_thumbnail.create_thumbnail()
            create_video(self.video_path[0], start_time, end_time, "./results/" + windows_title + ".mp4", self.choose_region.currentText())


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
