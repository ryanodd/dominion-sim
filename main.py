from bottle import route, run, template, response, request
import json
import os

from game.gameState import GameState
from utils.dominionOnlineLogParser.logParser import logToGameState
from utils.cardSorter import sortCardsByTypeThenCost
from bot.cardInfoSum import getCardInfoSumReport, CardInfoSumReport

# CORS decorator
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        if 'IS_PROD' in os.environ.keys():
            if request.get_header('Origin').startswith('https'):
                response.headers['Access-Control-Allow-Origin'] = 'https://councilroom.herokuapp.com'
            else:
                response.headers['Access-Control-Allow-Origin'] = 'http://councilroom.herokuapp.com'
        else:
            response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors

@route('/logParser', method=['POST', 'OPTIONS'])
@enable_cors
def parseThatLogBoi():
    payload = json.load(request.body)

    gameState = logToGameState(payload['logStr'])
    if False:
        response.status = 500

    deckInfos = []
    for player in gameState.players:
        deckInfo = {}
        deckInfo['playerName'] = player.name
        deckInfo['playerInitial'] = player.name[0]
        
        deckInfo['cardNameList'] = []
        player.deck = sortCardsByTypeThenCost(player.deck)
        for card in player.deck:
            deckInfo['cardNameList'].append(card.name)
        
        deckInfo['numCards'] = CardInfoSumReport(len(player.deck)).__dict__
        deckInfo['totalMoney'] = getCardInfoSumReport(player.deck, 'money').__dict__
        deckInfo['totalStops'] = getCardInfoSumReport(player.deck, 'stop').__dict__
        deckInfo['totalDraws'] = getCardInfoSumReport(player.deck, 'draws').__dict__
        deckInfo['totalExtraDraws'] = getCardInfoSumReport(player.deck, 'extraDraws').__dict__
        deckInfo['totalActions'] = getCardInfoSumReport(player.deck, 'actions').__dict__
        deckInfo['totalTerminals'] = getCardInfoSumReport(player.deck, 'terminal').__dict__
        deckInfo['totalExtraActions'] = getCardInfoSumReport(player.deck, 'extraActions').__dict__
        deckInfo['totalBuys'] = getCardInfoSumReport(player.deck, 'buys').__dict__

        deckInfos.append(deckInfo)

    response.headers['Content-Type'] = "application/json"
    return {'deckInfos': deckInfos}

if 'PORT' in os.environ.keys():
    run(host='0.0.0.0', port=os.environ['PORT'])
else:
    run(host='localhost', port=3993)
