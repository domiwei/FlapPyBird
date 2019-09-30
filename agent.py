import random

JUMP = 0
PAUSE = 1

class EpsilonGreedy:
    def __init__(self):
        self.epsilon = 0.1

    def takeAction(self, actions):
        if random.random() > self.epsilon:
            return actions.index(max(actions))
        return random.randint(0, len(actions)-1)

class Agent:
    def __init__(self, policy):
        # (dx, dy) -> [award of jump, award of do nothing]
        self.qtable = {}
        self.award = {True: 1, False: -100}
        self.discountFactor = 0.5
        self.learnRate = 0.6
        self.policy = policy
        self.prevAction = PAUSE
        self.prevState = None

    # jump returns true if decide to jump this moment
    def jump(self, player, upipe, lpipe):
        dx = int(upipe['x'] - player['x'])
        dy = int((lpipe['y'] + upipe['y'])/2.0 - player['y'])
        if (dx, dy) not in self.qtable:
            self.qtable[(dx, dy)] = [random.random(), random.random()]
        action = self.policy.takeAction(self.qtable[(dx, dy)])
        self.prevAction = action
        self.prevState = (dx, dy)
        return action == JUMP

    # feeback gives feedback of previous action
    def feedback(self, player, upipe, lpipe, alive):
        if self.prevState is None:
            return
        dx = int(upipe['x'] - player['x'])
        dy = int((lpipe['y'] + upipe['y'])/2.0 - player['y'])
        if (dx, dy) not in self.qtable:
            self.qtable[(dx, dy)] = [random.random(), random.random()]
        optimalFuture = max(self.qtable[(dx, dy)])
        oldValue = self.qtable[self.prevState][self.prevAction]
        reward = self.award[alive]

        # update
        self.qtable[self.prevState][self.prevAction] = \
            (1.0-self.learnRate)*oldValue + \
            self.learnRate*(reward + self.discountFactor*optimalFuture)

