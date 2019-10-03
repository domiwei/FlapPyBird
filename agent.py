import random
import time
import math
import json

JUMP = 0
PAUSE = 1

ALIVE = 0
PASSPIPE = 1
DEAD = 2

class EpsilonGreedy:
    def __init__(self):
        self.epsilon = 0.01

    def takeAction(self, actions):
        if random.random() > self.epsilon:
            return actions.index(max(actions))
        return random.randint(0, len(actions)-1)

class Agent:
    def __init__(self, policy, modelfile="", writemodel=True):
        # (dx, dy, ypos, yvel) -> [award of jump, award of do nothing]
        self.qtable = {}
        if modelfile != "":
            with open(modelfile, "r") as f:
                model = f.readline()
                print(model)
                self.qtable = eval(model)
        self.award = {ALIVE: 1, PASSPIPE: 1000, DEAD: -1000}
        self.discountFactor = 0.8
        self.learnRate = 0.5
        self.policy = policy
        self.prevAction = PAUSE
        self.prevState = None
        self.prevTimestamp = 0
        self.writemodel = writemodel

    # jump returns true if decide to jump this moment
    def jump(self, player, upipe, lpipe):
        #dx = int(upipe['x'] - player['x'])
        #dy = int((lpipe['y'] + upipe['y'])/2.0 - player['y'])
        state = self.getState(player, lpipe)
        if state == self.prevState: # do nothing
            return
        action = self.policy.takeAction(self.qtable[state])
 #       print(player, lpipe, upipe, dx, dy)
        #print(state, self.qtable[state])
        #time.sleep(0.3)
        self.prevAction = action
        self.prevState = state
        return action == JUMP

    # feeback gives feedback of previous action
    def feedback(self, player, upipe, lpipe, result):
        if self.prevState is None or self.prevState[0] == 0:
            return

        state = self.getState(player, lpipe)
        if state == self.prevState: # do nothing
            return
        optimalFuture = max(self.qtable[state])
        oldValue = self.qtable[self.prevState][self.prevAction]
        reward = self.award[result]
        #if result == ALIVE and state[1]>30: # try to discount
        #    reward = (-1.0*math.exp(abs(state[1]-30)/4))

        # update
        self.qtable[self.prevState][self.prevAction] = \
            (1.0-self.learnRate)*oldValue + \
            self.learnRate*(reward + self.discountFactor*optimalFuture)

        if time.time() - self.prevTimestamp > 5:
            print("table size: ", len(self.qtable))
            if self.writemodel:
                with open("qtable.model", "w") as f:
                    f.write(str(self.qtable))
            self.prevTimestamp = time.time()
#            print(self.prevState, state, oldValue, self.qtable[self.prevState][self.prevAction])

    #    print(self.prevState, state, oldValue, self.qtable[self.prevState])
    #    time.sleep(0.5)
        if result == DEAD:
            #print(self.prevState, state, oldValue, self.qtable[self.prevState])
            self.prevState = None

    def getState(self, player, lpipe):
        dx = int((lpipe['x'] - player['x'])/4)
        dy = int((lpipe['y'] - player['y'])/4)
        #playerY = int(player['y']/2)
        state = (dx, dy, int(player['v']/2))
        if state not in self.qtable:
            self.qtable[state] = [0.0, 0.01]
        return state

