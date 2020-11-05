import boto3
import json
import mmap
import re
import urllib.request
import zipfile

def read_webpage():

    twic_url = 'https://theweekinchess.com/twic'
    str_source = urllib.request.urlopen(twic_url).read().decode('utf-8')
    last_link = re.findall(r'The latest issue.*\n', str_source)[0].split('=')[1].split(' ')[0].strip('\"')
    return last_link
    
def download_games():

    # define zip filename
    working_dir = '/tmp/'
    input_zip_filename = '%slast_twic.zip' % working_dir

    # download latest TWIC
    last_twic_zip_url = read_webpage().replace('.html', 'g.zip').replace('html', 'zips')
    urllib.request.urlretrieve(last_twic_zip_url, input_zip_filename)

    # handle zip file
    with zipfile.ZipFile(input_zip_filename, 'r') as zip_ref:
        zip_ref.extractall(working_dir)
        input_pgn_filename = working_dir + zip_ref.namelist()[0]

    return input_pgn_filename
    
def send_email(games):
    # Create an SNS client
    sns = boto3.client('sns')

    # Publish a simple message to the specified SNS topic
    response = sns.publish(
        TopicArn='arn:aws:sns:REGION:AWS_ACCOUNT:TWIC',
        Message=games,
    )

    
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

def is_game_relevant(pgn_game):

    # rating and ECO conditions are satisfied: game is relevant
    return is_rating_relevant(pgn_game) and is_eco_relevant(pgn_game)

def lambda_handler(event, context):

    # define names of input and output files
    output_pgn_filename = '/tmp/relevant.pgn'

    input_pgn_filename = download_games()
    all_games = open(input_pgn_filename, 'r').read()

    # separate games
    games = re.split(r'\n(?=\[Event  *)', all_games)

    # filter relevant games
    relevant_games = list(filter(is_game_relevant, games))

    # write output PGN file
    # output_pgn_file = open(output_pgn_filename, 'w')
    # for game in relevant_games:
    #    output_pgn_file.write(game+'\n')
    str_output = '%d games have been e-mailed to you!' % len(relevant_games)

    # send e-mail
    send_email('\n'.join(relevant_games))
    
    return {
        'statusCode': 200,
        'body': json.dumps(str_output)
    }
