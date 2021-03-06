from game.card.gCard import GCard, CardType
from game.choice import Choice, ChoiceID, getChoice
from game.gameState import GameState
from game.playerState import GainType
from game.card.gCardUtils import cardCountByName, cardCountByType
from utils.log import logError

# TODO: if we want gamestates to be continuable mid-choice then we need to break up card step fns before & after choices

cardNameDict = {}

def getGCard(name):
    if (name not in cardNameDict):
        logError("Name %s not found in cardNameDict")
    return cardNameDict[name]()
######################### Essentials ###############################

def estate():
    def estate_vsteps(player, game):
        player.vp += 1
    return GCard("Estate", 2, [CardType.VICTORY], None, estate_vsteps)
cardNameDict['Estate'] = estate


def duchy():
    def duchy_vsteps(player, game):
        player.vp += 3
    return GCard("Duchy", 5, [CardType.VICTORY], None, duchy_vsteps)
cardNameDict['Duchy'] = duchy

def province():
    def province_vsteps(player, game):
        player.vp += 6
    return GCard("Province", 8, [CardType.VICTORY], None, province_vsteps)
cardNameDict['Province'] = province

def copper():
    def copper_steps(player, game):
        player.money += 1
    return GCard("Copper", 0, [CardType.TREASURE], copper_steps, None)
cardNameDict['Copper'] = copper

def silver():
    def silver_steps(player, game):
        player.money += 2
    return GCard("Silver", 3, [CardType.TREASURE], silver_steps, None)
cardNameDict['Silver'] = silver

def gold():
    def gold_steps(player, game):
        player.money += 3
    return GCard("Gold", 6, [CardType.TREASURE], gold_steps, None)
cardNameDict['Gold'] = gold

def curse():
    def curse_vsteps(player, game):
        player.vp -= 1
    return GCard("Curse", 0, [CardType.CURSE], None, curse_vsteps)
cardNameDict['Curse'] = curse


######################### Base Set 2ed ############################


def artisan():
    def artisan_steps(playerIndex, game):
        player = game.players[playerIndex]

        # Gain card costing up to 5
        gainChoice = player.bot.choose(getChoice(ChoiceID.ARTISAN1), game.gameState, playerIndex)
        game.gain(gainChoice, playerIndex)

        # Put a card from your hand onto your deck
        topdeckChoice = player.bot.choose(getChoice(ChoiceID.ARTISAN2), game.gameState, playerIndex)
        player.deck.append(player.hand.pop(topdeckChoice))
    return GCard("Artisan", 6, [CardType.ACTION], artisan_steps, None)
cardNameDict['Artisan'] = artisan

def bandit():
    def bandit_steps(playerIndex, game):
        player = game.players[playerIndex]
        game.gain('Gold', playerIndex)
        for opponent in game.otherPlayers(player):
            topTwoCards = game.newCardStore()
            if cardCountByType(CardType.TREASURE, topTwoCards) > cardCountByName('Copper', topTwoCards):
                trashChoice = player.bot.choose(getChoice(ChoiceID.BANDIT), game.gameState, playerIndex)
                game.trash.append(topTwoCards.pop(trashChoice))
            opponent.discard += topTwoCards
            game.popCardStore()
    return GCard("Bandit", 5, [CardType.ACTION], bandit_steps, None)
cardNameDict['Bandit'] = bandit
                    

def bureaucrat():
    def bureaucrat_steps(playerIndex, game):
        player = game.players[playerIndex]

        game.gain('Silver', player, GainType.DECK)

        for opponent in game.otherPlayers(player):
            if cardCountByType(opponent.hand, CardType.VICTORY) >= 1:
                topDeckChoice = player.bot.choose(getChoice(ChoiceID.BUREAUCRAT), game.gameState, playerIndex)
                opponent.deck.append(opponent.hand.pop(topDeckChoice))
            # TODO: else reveal? Patron trigger
    return GCard("Bureaucrat", 4, [CardType.ACTION], bureaucrat_steps, None)
cardNameDict['Bureaucrat'] = bureaucrat

def cellar():
    def cellar_steps(playerIndex, game):
        player = game.players[playerIndex]
        
        player.actions += 1
        discardChoices = player.bot.choose(getChoice(ChoiceID.CELLAR), game.gameState, playerIndex)
        numDiscarded = len(discardChoices)
        # TODO: oh no this backward index loop is unsafe? this is used everywhere
        for i in sorted(discardChoices, reverse=True):
            player.discard.append(player.hand.pop(i))
        player.draw(numDiscarded)
    return GCard("Cellar", 2, [CardType.ACTION], cellar_steps, None)
cardNameDict['Cellar'] = cellar

def chapel():
    def chapel_steps(playerIndex, game):
        player = game.players[playerIndex]
        
        trashChoices = player.bot.choose(getChoice(ChoiceID.CHAPEL), game.gameState, playerIndex)
        for i in sorted(trashChoices, reverse=True):
            game.trash.append(player.hand.pop(i))

    return GCard("Chapel", 2, [CardType.ACTION], chapel_steps, None)
cardNameDict['Chapel'] = chapel

def councilRoom():
    def councilRoom_steps(playerIndex, game):
        player = game.players[playerIndex]
        
        player.draw(4)
        player.buys += 1
        for opponent in game.otherPlayers(player):
            opponent.draw(1)
    return GCard("Council Room", 5, [CardType.ACTION], councilRoom_steps, None)
cardNameDict['Council Room'] = councilRoom

def festival():
    def festival_steps(playerIndex, game):
        player = game.players[playerIndex]
        
        player.actions += 2
        player.buys += 1
        player.money += 2
    return GCard("Festival", 5, [CardType.ACTION], festival_steps, None)
cardNameDict['Festival'] = festival

def gardens():
    def garden_vsteps(playerIndex, game):
        player = game.players[playerIndex]

        player.vp += len(player.totalDeck) / 10
    return GCard("Gardens", 4, [CardType.VICTORY], None, garden_vsteps)
cardNameDict['Gardens'] = gardens

def harbinger():
    def harbinger_steps(playerIndex, game):
        player = game.players[playerIndex]

        player.draw(1)
        player.actions += 1

        topDeckChoice = player.bot.choose(getChoice(ChoiceID.HARBINGER), game.gameState, playerIndex)
        player.deck.append(player.discard.pop(topDeckChoice))

    return GCard("Harbinger", 3, [CardType.ACTION], harbinger_steps, None)
cardNameDict['Harbinger'] = harbinger

def laboratory():
    def laboratory_steps(playerIndex, game):
        player = game.players[playerIndex]

        player.draw(2)
        player.actions += 1
    return GCard("Laboratory", 5, [CardType.ACTION], laboratory_steps, None)
cardNameDict['Laboratory'] = laboratory

def library():
    def library_steps(playerIndex, game):
        player = game.players[playerIndex]

        cardsToDiscard = game.newCardStore()
        while len(player.hand < 7):
            drawnCard = player.deck.pop()
            if (CardType.ACTION in drawnCard.types):
                willDiscard = player.bot.choose(getChoice(ChoiceID.LIBRARY), game.gameState, playerIndex)
                if (willDiscard):
                    cardsToDiscard.append(drawnCard)
                else:
                    player.hand.append(drawnCard)
        player.discard += cardsToDiscard
        game.popCardStore()
    return GCard("Library", 5, [CardType.ACTION], library_steps, None)
cardNameDict['Library'] = library

def market():
    def market_steps(playerIndex, game):
        player = game.players[playerIndex]

        player.draw(1)
        player.actions += 1
        player.buys += 1
        player.money += 1
    return GCard("Market", 5, [CardType.ACTION], market_steps, None)
cardNameDict['Market'] = market

# TODO: For now, just +1 card&action. This one is trouble. Needs event triggers
def merchant():
    def merchant_steps(playerIndex, game):
        player = game.players[playerIndex]

        player.draw(1)
        player.actions += 1

    return GCard("Merchant", 3, [CardType.ACTION], merchant_steps, None)
cardNameDict['Merchant'] = merchant

def militia():
    def militia_steps(playerIndex, game):
        player = game.players[playerIndex]

        player.money += 2

        for opponent in game.otherPlayers(player):
            if (len(opponent.hand) > 3):
                discardChoices = opponent.bot.choose(getChoice(ChoiceID.MILITIA), game.gameState, opponent.playerIndex)
                for i in sorted(discardChoices, reverse=True):
                    player.discard.append(player.hand.pop(i))

    return GCard("Militia", 4, [CardType.ACTION, CardType.ATTACK], militia_steps, None)
cardNameDict['Militia'] = militia

def mine():
    def mine_steps(playerIndex, game):
        player = game.players[playerIndex]

        if cardCountByType(player.hand, CardType.TREASURE) >= 1:
            trashChoice = player.bot.choose(getChoice(ChoiceID.MINE1), game.gameState, playerIndex)
            if trashChoice:
                game.trash.append(player.hand.pop(trashChoice))
                gainChoice = player.bot.choose(getChoice(ChoiceID.MINE2), game.gameState, playerIndex)
                game.gain(gainChoice, playerIndex, GainType.HAND)

    return GCard("Mine", 5, [CardType.ACTION], mine_steps, None)
cardNameDict['Mine'] = mine

# TODO: for now, it's just +2 cards
def moat():
    def moat_steps(playerIndex, game):
        player = game.players[playerIndex]

        player.draw(2)

    return GCard("Moat", 2, [CardType.ACTION, CardType.REACTION], moat_steps, None)
cardNameDict['Moat'] = moat

def moneylender():
    def moneylender_steps(playerIndex, game):
        player = game.players[playerIndex]

        if cardCountByName(player.hand, 'Copper') >= 1:
            trashChoice = player.bot.choose(getChoice(ChoiceID.MONEYLENDER), game.gameState, playerIndex)
            if trashChoice:
                game.trash.append(player.hand.pop(trashChoice))
                player.money += 3

    return GCard("Moneylender", 4, [CardType.ACTION], moneylender_steps, None)
cardNameDict['Moneylender'] = moneylender

def poacher():
    def poacher_steps(playerIndex, game):
        player = game.players[playerIndex]

        player.draw(1)
        player.actions += 1
        player.money += 1

        if game.shop.numEmptySupplyPiles >= 1:
            discardChoices = player.bot.choose(getChoice(ChoiceID.POACHER), game.gameState, playerIndex)
            for i in sorted(discardChoices, reverse=True):
                player.discard.append(player.hand.pop(i))

    return GCard("Poacher", 4, [CardType.ACTION], poacher_steps, None)
cardNameDict['Poacher'] = poacher

def remodel():
    def remodel_steps(playerIndex, game):
        player = game.players[playerIndex]

        if (len(player.hand) > 0):
            trashChoice = player.bot.choose(getChoice(ChoiceID.REMODEL1), game.gameState, playerIndex)
            game.trash.append(player.hand.pop(trashChoice))
            gainChoice = player.bot.choose(getChoice(ChoiceID.REMODEL2), game.gameState, playerIndex)
            if gainChoice:
                game.gain(gainChoice, playerIndex)

    return GCard("Remodel", 4, [CardType.ACTION], remodel_steps, None)
cardNameDict['Remodel'] = remodel

def sentry():
    def sentry_steps(playerIndex, game):
        player = game.players[playerIndex]

        player.draw(1)
        player.actions += 1

        topTwoCards = game.newCardStore()
        topTwoCards = [player.deckPop(), player.deckPop()]

        if (len(topTwoCards) > 0):
            trashChoices = player.bot.choose(getChoice(ChoiceID.SENTRY1), game.gameState, playerIndex)
            for i in sorted(trashChoices, reverse=True):
                game.trash.append(topTwoCards.pop(i))
        if (len(topTwoCards) > 0):
            discardChoices = player.bot.choose(getChoice(ChoiceID.SENTRY2), game.gameState, playerIndex)
            for i in sorted(discardChoices, reverse=True):
                player.discard.append(topTwoCards.pop(i))
        if (len(topTwoCards) > 0):
            orderChoice = [0]
            if (len(topTwoCards) > 1):
                orderChoice = player.bot.choose(getChoice(ChoiceID.SENTRY3), game.gameState, playerIndex)
            # Thinkin bout having SENTRY3 (order choice) be 1 card choice at a time?
            for o in orderChoice:
                player.deck.append(topTwoCards[o])
        game.popCardStore()
    return GCard("Sentry", 5, [CardType.ACTION], sentry_steps, None)
cardNameDict['Sentry'] = sentry

def smithy():
    def smithy_steps(playerIndex, game):
        player = game.players[playerIndex]

        player.draw(3)
    return GCard("Smithy", 4, [CardType.ACTION], smithy_steps, None)
cardNameDict['Smithy'] = smithy

def throneRoom():
    def throneRoom_steps(playerIndex, game):
        player = game.players[playerIndex]

        if cardCountByType(player.hand, CardType.ACTION) >= 1:
            playChoice = player.bot.choose(getChoice(ChoiceID.THRONEROOM), game.gameState, playerIndex)
            if playChoice:
                player.play.append(player.hand.pop(playChoice))
                player.play[-1].steps() # TODO: unsafe, need instance reference eventually
                player.play[-1].steps() # TODO: unsafe, need instance reference eventually
    return GCard("Throne Room", 4, [CardType.ACTION], throneRoom_steps, None)
cardNameDict['Throne Room'] = throneRoom

def vassal():
    def vassal_steps(playerIndex, game):
        player = game.players[playerIndex]

        player.money += 2

        discardCard = player.deckPop()
        if discardCard:
            player.discard.append(discardCard)
            willPlay = player.bot.choose(getChoice(ChoiceID.VASSAL), game.gameState, playerIndex)
            if willPlay:
                player.play.append(player.discard.pop())
                discardCard.steps()
    return GCard("Vassal", 3, [CardType.ACTION], vassal_steps, None)
cardNameDict['Vassal'] = vassal

def village():
    def village_steps(playerIndex, game):
        player = game.players[playerIndex]

        player.draw(1)
        player.actions += 2
    return GCard("Village", 3, [CardType.ACTION], village_steps, None)
cardNameDict['Village'] = village

def witch():
    def witch_steps(playerIndex, game):
        player = game.players[playerIndex]

        player.draw(2)
        for opponent in game.otherPlayers(player):
            game.gain('Curse', opponent.playerIndex)
    return GCard("Witch", 5, [CardType.ACTION, CardType.ATTACK], witch_steps, None)
cardNameDict['Witch'] = witch

def workshop():
    def workshop_steps(playerIndex, game):
        player = game.players[playerIndex]

        gainChoice = player.bot.choose(getChoice(ChoiceID.WORKSHOP), game.gameState, playerIndex)
        game.gain(gainChoice, playerIndex)

    return GCard("Workshop", 3, [CardType.ACTION, CardType.ATTACK], workshop_steps, None)
cardNameDict['Workshop'] = workshop