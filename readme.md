# Board Game Library Generator
#### Video Demo:  https://youtu.be/otP8FtV0jTg
#### Description:
--the majority of this program has already been implemented in a python library called 'boardgamegeek2'. I decided to attempt to implement those features without the library to see what all goes into accessing the boardgamegeek.com API (or 2 API's, as is the case with boardgamegeek)--
Board Game Library Generator is a Python app that will prompt a user to input the title of a Boardgame and then populate a csv file with information about the game gathered by using the boardgamegeek API's.
The user will continue to be prompted for games to be added to the list until the user enters "Done" instead of the name of a boardgame.
Once the user has entered "Done", the application will generage a file called game_list.csv that has all of the information gathered from boardgamegeek.com. It will also generate a table in the terminal showing all of the games that were successfully entered.

## Boardgame Class
The Boardgame Class is how all of the information gets stored. The attributes are ass follows:
self.id:
The name of the game, as entered by the user
self.year:
The original year the game was published. This attribute is mostly used to help the user identify which version of the game they are looking for when more than one game has the exact title they entered.
self.publisher:
Another tool to help the user identify which version of the game. If there is more than one publisher for a game, this attribute is set to "Multiple Publishers" by the create_game() function.
self.min_player:
Minimum number of players as recommended by the publisher.
self.max_player:
Maximum number of players as recommended by the publisher.
self.rating:
The rating of the game on boardgamegeek.com on a scale of 1-10.
self.weight:
the complexity of the game on a scale of 1-5.

In addition to the attributes, the Boardgame Class has one built in funtion:
Boardgame.make_dict():
This function takes no arguments and returns a dictionary of all of the attributes currently assigned to the Boardgame object.

## search()
This function takes a single argument- a string, and query's boardgamegeek via their api2 to generate an id of the game that exactly matches the query.
If no games match the string the function returns "None"
If multipe games match the string exactly, this function uses the get_version() function to clarify with the user which version they are intending.

## get_game()
This function asks the user for the name of a game. It will continue to ask the user for a game title until a match is found in the boardgamegeek database or the user enters "Done"
The function then either returns the unique id of the game or "Done.

## create_game()
The create_game function takes an int (that must be previously identified as an id of a game on boardgamegeek.com) and returns a Boardgame object with the relevant iformation about the game.
There are several tries in this function due to the fact that occasionally certain information will be in list and other times it is a key/value pair. This is due to the game possibly having multiple values for certain information such as publisher.

## print_games()
This function takes as it's only argument a list of dictionaries that have been created by the Boardgame.make_dict() funciton. It returns a table with the given games and their information for the user to see.
This table is created with the tabulate library.

## export_games()
This funciton takes a list of dictionaries just like the print_games function, but instead of creating a table, it generates a csv file called "game_list.csv"

## get_version()
In general, this program leaves it up to the user to correctly enter the title of the game. It simply states that no games exist of the matching title if there are no exact results, leaving it to the user to troubleshoot exact naming as it appears on boardgamegeek.com.
Occasionally, though, there are multiple games with the exact same title. This function creates a table with those titles and displays it for the user, asking them to choose which version they intend.
In the future, this function can be used to expand the search to something beyond an exact match. The API's involved are rather slow when performing searches and at this time it seemed more user friendly to simply put the onus on the user to enter the data correctly.
This function will either return the id of the chosen game or "None" if none of the games are the game intended by the user.
