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
        self.qtable = {}
        self.award = 1
        self.penalty = -100
        self.policy = policy
        self.prevAction = PAUSE

    # jump returns true if decide to jump this moment
    def jump(self, player, upipe, lpipe):
        dx = upipe['x'] - player['x']
        dy = (lpipe['y'] + upipe['y'])/2.0 - player['y']
        if (dx, dy) not in self.qtable:
            self.qtable[(dx, dy)] = [1.0, 1.0]
        action = self.policy.takeAction(self.qtable[(dx, dy)])
        self.prevAction = action
        return action == JUMP

    # feeback gives feedback of previous action
    def feedback(self):
        pass
