from game.card.gCard import CardType
from alchemist.card import getCard

def chooseAction(choice, gameState, choosingPlayerIndex):
    player = gameState.players[choosingPlayerIndex]
    actionPriorities = {}
    for i in range(len(player.hand)):
        if (CardType.ACTION in player.hand[i].types):
            actionPriorities[i] = actionPriority(player.hand[i].name)

    if (not actionPriorities): # None to choose.
        return -1
    bestChoice = max(actionPriorities, key=actionPriorities.get)
    if (bestChoice == 0): # 0 means it's not beneficial to play
        return -1
    else:
        return bestChoice  

def actionPriority(name):
    cardInfo = getCard(name)
    if not cardInfo.beneficial.value:
        return 0
    elif cardInfo.actions.value >= 1:
        return 2
    else:
        return 1 # TODO: should somehow tiebreak terminals when it matters