import collections
import random

JUMP = 0
PAUSE = 1

class EpsilonGreedy:
    def takeAction(self, actions):
        #summation = sum(actions)
        return actions.index(min(actions))

class Agent:
    def __init__(self, policy):
        # (dx, dy) -> [award of jump, award of do nothing]
        self.__Qtable = {}
        self.__award = 1
        self.__penalty = -100
        self.__policy = policy
        self.__prevAction = PAUSE

    # jump returns true if decide to jump this moment
    def jump(self, player, upipe, lpipe):
        dx = upipe['x'] - player['x']
        dy = (lpipe['y'] + upipe['y'])/2.0 - player['y']
        if (dx, dy) not in self.__Qtable:
            self.__Qtable[(dx, dy)] = [1.0, 1.0]
        action = self.__policy.takeAction(self.__Qtable[(dx, dy)])
        self.__prevAction = action
        return action == JUMP

    # feeback gives feedback of previous action
    def feedback(self):
        pass
