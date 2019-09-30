import random
import time

JUMP = 0
PAUSE = 1

ALIVE = 0
PASSPIPE = 1
DEAD = 2

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
        self.award = {ALIVE: 1, PASSPIPE: 100, DEAD: -1000}
        self.discountFactor = 0.5
        self.learnRate = 0.6
        self.policy = policy
        self.prevAction = PAUSE
        self.prevState = None
        self.prevTimestamp = 0

    # jump returns true if decide to jump this moment
    def jump(self, player, upipe, lpipe):
        #dx = int(upipe['x'] - player['x'])
        #dy = int((lpipe['y'] + upipe['y'])/2.0 - player['y'])
        state = self.getState(player, lpipe)
        action = self.policy.takeAction(self.qtable[state])
 #       print(player, lpipe, upipe, dx, dy)
        #print(state)
        #time.sleep(0.3)
        self.prevAction = action
        self.prevState = state
        return action == JUMP

    # feeback gives feedback of previous action
    def feedback(self, player, upipe, lpipe, result):
        if self.prevState is None:
            return

        state = self.getState(player, lpipe)
        optimalFuture = max(self.qtable[state])
        oldValue = self.qtable[self.prevState][self.prevAction]
        reward = self.award[result]

        # update
        self.qtable[self.prevState][self.prevAction] = \
            (1.0-self.learnRate)*oldValue + \
            self.learnRate*(reward + self.discountFactor*optimalFuture)

        if time.time() - self.prevTimestamp > 3:
            print("table size: ", len(self.qtable))
            self.prevTimestamp = time.time()

    def getState(self, player, lpipe):
        dx = int((lpipe['x'] - player['x'])/8)
        dy = int((lpipe['y'] - player['y'])/8)
        playerY = int(player['y']/8)
        state = (dx, dy, playerY)
        if state not in self.qtable:
            self.qtable[state] = [random.random(), random.random()+0.9]
        return state

