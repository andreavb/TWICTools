import re
import zipfile

import platform
if platform.python_version().startswith('2'):
    import urllib as ul
else:
    import urllib.request as ul

def read_webpage():

    # read through TWIC page and find the link that stands for the latest issue
    twic_url = 'https://theweekinchess.com/twic'
    str_source = ul.urlopen(twic_url).read().decode('utf-8')
    last_link = re.findall(r'The latest issue.*\n', str_source)[0].split('=')[1].split(' ')[0].strip('\"')
    return last_link

def download_games():

    # define zip filename
    input_zip_filename = 'last_twic.zip'

    # download latest TWIC
    last_twic_zip_url = read_webpage().replace('.html', 'g.zip').replace('html', 'zips')
    ul.urlretrieve(last_twic_zip_url, input_zip_filename)

    # handle zip file
    with zipfile.ZipFile(input_zip_filename, 'r') as zip_ref:
        zip_ref.extractall()
        input_pgn_filename = zip_ref.namelist()[0]

    return input_pgn_filename

def is_rating_relevant(pgn_game):

    # define rating relevance threshold
    rating_threshold = 2300

    # find both ratings in the game
    test = re.findall(r'\n\[.*Elo.*', pgn_game)

    # at least one player was unrated: ratings are not relevant
    if test is None or len(test) != 2:
        return False

    # find numeric values for each rating
    white_elo = int(test[0][12:16])
    black_elo = int(test[1][12:16])

    # both ratings are above threshold: ratings are relevant
    if white_elo > rating_threshold and black_elo > rating_threshold:
        return True

    # otherwise: ratings are irrelevant
    return False

def is_eco_relevant(pgn_game):

    # define list of interesting ECO codes
    my_repertoire_list = ['A00', 'A01']

    # join them into a regular expression
    my_repertoire_re = re.compile("|".join(my_repertoire_list))

    # game used one of those ECO codes: ECO is relevant
    if my_repertoire_re.search(pgn_game):
        return True

    # otherwise: ECO is irrelevant
    return False

def is_player_relevant(pgn_game):

    # define players to stalk
    my_stalk_list = ['Carlsen', 'Caruana']

    my_stalk_re = re.compile("|".join(my_stalk_list))

    if my_stalk_re.search(pgn_game):
        return True

def is_game_relevant(pgn_game):

    # rating and ECO conditions are satisfied: game is relevant
    return (is_rating_relevant(pgn_game) and is_eco_relevant(pgn_game)) or is_player_relevant(pgn_game)

def main():
    # define names of input and output files
    output_pgn_filename = 'relevant.pgn'

    input_pgn_filename = download_games()
    all_games = open(input_pgn_filename, 'r').read()

    # read input PGN file
    # all_games = open(input_pgn_filename, 'r').read()

    # separate games
    games = re.split(r'\n(?=\[Event  *)', all_games)

    # filter relevant games
    relevant_games = list(filter(is_game_relevant, games))

    # write output PGN file
    output_pgn_file = open(output_pgn_filename, 'w')
    for game in relevant_games:
        output_pgn_file.write(game+'\n')

main()
