from game.card import Card, CardType
from game.choices import Choice
from utils.log import logError

cardNameDict = {}
######################### Essentials ###############################

def estate():
    def estate_vsteps(player, board):
        player.vp += 1
    return Card("Estate", 2, [CardType.VICTORY], None, estate_vsteps)
cardNameDict['Estate'] = estate


def duchy():
    def duchy_vsteps(player, board):
        player.vp += 3
    return Card("Duchy", 5, [CardType.VICTORY], None, duchy_vsteps)
cardNameDict['Duchy'] = duchy

def province():
    def province_vsteps(player, board):
        player.vp += 6
    return Card("Province", 8, [CardType.VICTORY], None, province_vsteps)
cardNameDict['Province'] = province

def copper():
    def copper_steps(player, board):
        player.money += 1
    return Card("Copper", 0, [CardType.TREASURE], copper_steps, None)
cardNameDict['Copper'] = copper

def silver():
    def silver_steps(player, board):
        player.money += 2
    return Card("Silver", 3, [CardType.TREASURE], silver_steps, None)
cardNameDict['Silver'] = silver

def gold():
    def gold_steps(player, board):
        player.money += 3
    return Card("Gold", 6, [CardType.TREASURE], gold_steps, None)
cardNameDict['Gold'] = gold

def curse():
    def curse_vsteps(player, board):
        player.vp -= 1
    return Card("Curse", 0, [CardType.CURSE], None, curse_vsteps)
cardNameDict['Curse'] = curse


######################### Base Set 2ed ############################

def artisan():
    def artisan_steps(player, board):
        # Gain card costing up to 5
        gainChoice = player.bot.choose(Choice.ARTISAN1, player, board)
        if (board.shop[gainChoice].cost > 5):
            logError("Cheater! Invalid artisan gain choice")
        gainedCard = board.gain(gainChoice, player)
        player.gain(gainedCard)

        # Put a card from your hand onto your deck
        topdeckChoice = player.bot.choose(Choice.ARTISAN2, player, board)
        topdeckCard = player.hand.pop(topdeckChoice)
        player.deck.append(topdeckCard)
    return Card("Artisan", 6, [CardType.ACTION], artisan_steps, None)
cardNameDict['Artisan'] = artisan

def bandit():
    def bandit_steps(player, board):
        goldCard = board.gain(6, player)
        player.gain(goldCard)

        for opponent in board.otherPlayers(player):
            topTwoCards = []
            topTwoCards.append(opponent.deck.pop())
            topTwoCards.append(opponent.deck.pop())
            trashCandidates = []
            trashCandidatesMap = {} # maps trashCandidates indices to topTwoCards indices
            for i in range(topTwoCards):
                card = topTwoCards[i]
                if (CardType.TREASURE in card.types and card.name != "Copper"):
                    trashCandidatesMap[len(trashCandidates)] = i
                    trashCandidates.append(card)
            if (len(trashCandidates) > 0):
                trashChoice = 0
                if (len(trashCandidates) > 1):
                    trashChoice = player.bot.choose(Choice.BANDIT, opponent, board, trashCandidates)
                board.trash.append(topTwoCards[trashCandidatesMap[trashChoice]])
                trashCandidates.remove(trashChoice)
            opponent.discard += trashCandidates # discard the rest
    return Card("Bandit", 5, [CardType.ACTION], bandit_steps, None)
cardNameDict['Bandit'] = bandit
                    

def bureaucrat():
    def bureaucrat_steps(player, board):
        silverCard = board.gain(5, player)
        player.deck.append(silverCard) # not being logged as a gain for player?

        for opponent in board.otherPlayers(player):
            topDeckCandidates = []
            topDeckCandidatesMap = {} # maps topDeckCoices indices to hand indices
            for i in range(opponent.hand):
                card = opponent.hand[i]
                if CardType.VICTORY in card.types:
                    topDeckCandidatesMap[len(topDeckCandidates)] = i
                    topDeckCandidates.append(card)
            if (topDeckCandidates > 0):
                topDeckChoice = 0
                if (topDeckCandidates > 1):
                    topDeckChoice = player.bot.choose(Choice.BUREAUCRAT, opponent, board)
                topDeckCard = opponent.hand.pop(topDeckCandidatesMap[topDeckChoice])
                opponent.deck.append(topDeckCard)
    return Card("Bureaucrat", 4, [CardType.ACTION], bureaucrat_steps, None)
cardNameDict['Bureaucrat'] = bureaucrat

def cellar():
    def cellar_steps(player, board):
        player.actions += 1
        discardChoices = player.bot.choose(Choice.CELLAR, player, board)
        numDiscarded = len(discardChoices)
        for i in sorted(discardChoices, reverse=True):
            player.discard.append(player.hand.pop(i))
        player.draw(numDiscarded)
    return Card("Cellar", 2, [CardType.ACTION], cellar_steps, None)
cardNameDict['Cellar'] = cellar

def chapel():
    def chapel_steps(player, board):
        trashChoices = player.bot.choose('chapel', player, board)
        for i in sorted(trashChoices, reverse=True):
            board.trash.append(player.hand.pop(i))

    return Card("Chapel", 2, [CardType.ACTION], chapel_steps, None)
cardNameDict['Chapel'] = chapel

def councilRoom():
    def councilRoom_steps(player, board):
        player.draw(4)
        player.buys += 1
        for opponent in board.otherPlayers(player):
            opponent.draw(1)
    return Card("Council Room", 5, [CardType.ACTION], councilRoom_steps, None)
cardNameDict['Council Room'] = councilRoom

def festival():
    def festival_steps(player, board):
        player.actions += 2
        player.buys += 1
        player.money += 2
    return Card("Festival", 5, [CardType.ACTION], festival_steps, None)
cardNameDict['Festival'] = festival

def gardens():
    def garden_vsteps(player, board):
        player.vp += len(player.totalDeck) / 10
    return Card("Gardens", 4, [CardType.VICTORY], None, garden_vsteps)
cardNameDict['Gardens'] = gardens

# def harbinger():

def laboratory():
    def laboratory_steps(player, board):
        player.draw(2)
        player.actions += 1
    return Card("Laboratory", 5, [CardType.ACTION], laboratory_steps, None)
cardNameDict['Laboratory'] = laboratory

# def library():

def market():
    def market_steps(player, board):
        player.draw(1)
        player.actions += 1
        player.buys += 1
        player.money += 1
    return Card("Market", 5, [CardType.ACTION], market_steps, None)
cardNameDict['Market'] = market

# def merchant():

# def militia():

# def mine():

# def moat():

# def moneylender():

# def poacher():

# def remodel():

# def sentry():

def smithy():
    def smithy_steps(player, board):
        player.draw(3)
    return Card("Smithy", 4, [CardType.ACTION], smithy_steps, None)
cardNameDict['Smithy'] = smithy

# def throneRoom():

# def vassal():

def village():
    def village_steps(player, board):
        player.draw(1)
        player.actions += 2
    return Card("Village", 3, [CardType.ACTION], village_steps, None)
cardNameDict['Village'] = village

# def witch():

# def workshop():

def getCard(name):
    if (name not in cardNameDict):
        logError("Name %s not found in cardNameDict")
    return cardNameDict[name]()