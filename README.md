# Vodgen
Generate VoDs and thumbnails based on timestamp and YouTube title

## Setup
Config files required:
- config.json
- characterinfo.json

To create thumbnails, Vodgen requires a few different images to build the thumbnail. 

- Character portraits, located in `./assets/characters/{GAME_NAME}`
- Base/background image located in `./assets/background/{GAME_NAME}_bg.png`
- Banner to place the text like round name and player names located in `assets/banners`. 
- Custom fonts are stored in `./assets/fonts`
- Logos are stored in `./assets/logos`. Note: make sure logos especially are stored in a format which supports transparency, like the `png` format.

After all these requirements are met, run the `vodgen.exe` executable.

## Usage
After selecting the necessary files, the the timestamps and what set was played is next. Each new line contains a new set with the format.
```
hh:mm:ss.ms hh:mm:ss.ms {Name of tournament}: {Game name in shorthand} {Round} - {Player 1 name} ({Player 1 character}) vs {Player 2 name} (Player 2 character)
```
test
