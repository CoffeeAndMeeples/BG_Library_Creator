import csv
import requests
import urllib.parse
import xmltodict

from tabulate import tabulate

class Boardgame:
    def __init__(self):
       ...

    def make_dict(self):
        # name - id - year - publisher - min_player - max_player - rating - weight
        d = {
            "name": self.name,
            "id": self.id,
            "year": self.year,
            "publisher": self.publisher,
            "min_player": self.min_player,
            "max_player": self.max_player,
            "rating": self.rating,
            "weight": self.weight
        }
        return d

    # name getter
    @property
    def name(self):
        return self._name

    # name setter
    @name.setter
    def name(self, name):
        self._name = name

    #id getter
    @property
    def id(self):
        return self._id

    #id setter
    @id.setter
    def id(self, id):
        self._id = id

    #year getter
    @property
    def year(self):
        return self._year

    #year setter
    @year.setter
    def year(self, year):
        self._year = year

    #publisher getter
    @property
    def publisher(self):
        return self._publisher

    #publisher setter
    @publisher.setter
    def publisher(self, publisher):
        self._publisher = publisher

    #min_player getter
    @property
    def min_player(self):
        return self._min_player

    #min_player setter
    @min_player.setter
    def min_player(self, min_player):
        self._min_player = min_player

    #max_player getter
    @property
    def max_player(self):
        return self._max_player

    #max_player setter
    @max_player.setter
    def max_player(self, max_player):
        self._max_player = max_player

    #rating getter
    @property
    def rating(self):
        return self._rating

    #rating setter
    @rating.setter
    def rating(self, rating):
        self._rating = rating

    #weight getter
    @property
    def weight(self):
        return self._weight

    #weight setter
    @weight.setter
    def weight(self, weight):
        self._weight = weight



def main():
    game_ids = []
    # returns a game name
    while True:
        game = get_game()
        if game == "Done":
            break
        else:
            game_ids.append(game)

    results = []
    for id in game_ids:
        game = create_game(id)
        results.append(game.make_dict())


    print_games(results)
    export_games(results)


def search(game):
    # returns an id of the searched game

    encoded_search = urllib.parse.quote_plus(game)

    thing = requests.get(f"https://boardgamegeek.com/xmlapi2/search?query={encoded_search}&type=boardgame&exact=1")

    root = xmltodict.parse(thing.content)

    if root["items"]["@total"] == "0":
        return None
    elif int(root["items"]["@total"]) > 1:
        version = get_version(root)
        return version
    else:
        try:
            return root["items"]["item"]["@id"]
        except TypeError:
            return root["items"]["item"][0]["@id"]


def get_game():
    game = ""
    while game != "Done":
        game = input("Game Name(Enter 'Done' when finished): ")

        if game == "Done":
            return game
        else:
            id = search(game)
            if not id:
                print("---Title not found, check for input errors---")
            else:
                return id



def create_game(id):
    bg = Boardgame()

    response = requests.get(f"https://boardgamegeek.com/xmlapi/boardgame/{id}?stats=1")

    d = xmltodict.parse(response.content)

    # name - id - year - publisher - min_player - max_player - rating - weight
    bg.id = id
    # check to find the name- if there's only one name it will trigger first KeyError and access dictionary
    # if there's more than one name- the first try will iterate through the list to find the name with the primary tag
    try:
        count = 0
        for i in d["boardgames"]["boardgame"]["name"]:
            try:
                if i["@primary"] == "true":
                    bg.name = d["boardgames"]["boardgame"]["name"][count]["#text"]
            except KeyError:
                count += 1

    except (KeyError, TypeError):
        bg.name = d["boardgames"]["boardgame"]["name"]["#text"]

    bg.year = d["boardgames"]["boardgame"]["yearpublished"]
    try:
        bg.publisher = d["boardgames"]["boardgame"]["boardgamepublisher"]["#text"]
    except (KeyError, TypeError):
        bg.publisher = "Multiple Publishers"
    bg.min_player = d["boardgames"]["boardgame"]["minplayers"]
    bg.max_player = d["boardgames"]["boardgame"]["maxplayers"]
    bg.rating = d["boardgames"]["boardgame"]["statistics"]["ratings"]["average"]
    bg.weight = d["boardgames"]["boardgame"]["statistics"]["ratings"]["averageweight"]

    return bg


def print_games(games):
    # games must be a list of dictionaries
    try:
        print(tabulate(games, headers="keys", tablefmt="rounded_outline"))
        return 0
    except ValueError:
        return 1


def export_games(games):
    with open('game_list.csv', 'w', newline='') as file:
        fields = ['name', 'min_player', 'max_player', 'weight', 'rating', 'publisher', 'id', 'year']
        writer = csv.DictWriter(file, fieldnames= fields)
        writer.writeheader()
        for i in games:
            writer.writerow(i)

        return 0

def get_version(results):
    # a script to take multiple matching results and have user select correct version

    games = []
    counter = 0
    for _ in results["items"]["item"]:
        games.append(results["items"]["item"][counter]["@id"])
        counter += 1

    results = []
    for id in games:
        game = create_game(id)
        results.append(game.make_dict())

    while True:
        try:
            print(tabulate(results, headers="keys", tablefmt="rounded_outline", showindex="always"))
            version = input("--Input index number from left-most column or 'None' if correct game is not listed.--\n Which version? ")
            if version == "None":
                return None
            else:
                try:
                    g = int(version)
                    return games[g]
                except ValueError:
                    pass
        except TypeError:
            print("--invalid input.-- \n --Enter index number or 'None'--")


if __name__=="__main__":
    main()
