"""
Template for implementing QLearner  (c) 2015 Tucker Balch
"""

import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.s = 0
        self.a = 0

        self.num_states = num_states
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna

        #Initialize the Q table
        self.Q = np.zeros((num_states, num_actions))

    def author(self):
        return 'pbhatta3'  # Change this to your user ID


    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        random_choice = np.random.random()
        # print("Query Set State Random Choice == ", random_choice)
        # print("Query Set State self.rar == ", self.rar)
        if random_choice <= self.rar:
            action = rand.randint(0, self.num_actions - 1)
            # print("Query Set State srandom_choice <=(LesserEqual) self.rar")
            # print("Query Set State action == ", action)
            # print("Query Array == ", self.Q)
            # print("Query Set State for state s == ", s, " Q[s,:] == ", self.Q[s, :])
        elif random_choice > self.rar:
            action = self.Q[s,:].argmax()
            # print("Query Set State srandom_choice >(Greater) self.rar")
            # print("Query Set State action == ", action)
            # print("Query Array == ", self.Q)
            # print("Query Set State for state s == ", s, " Q[s,:] == ", self.Q[s, :])

        #apply decay rate
        self.rar = self.rar * self.radr

        if self.verbose: print ("s =", s,"a =",action)
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """
        #action = rand.randint(0, self.num_actions-1)
        # print("Before :: Query Function " , "self.s == ", self.s, " self.a == ", self.a, " self.Q[self.s, self.a] == ",  self.Q[self.s, self.a])
        self.Q[self.s, self.a] = (1 - self.alpha) * self.Q[self.s, self.a] + self.alpha *(r + (self.gamma * self.Q[s_prime,:].max()))
        # print("After :: Query Function ", "self.s == ", self.s, " self.a == ", self.a, " self.Q[self.s, self.a] == ",
        #       self.Q[self.s, self.a])
        #print("Query Function  self.Q[self.s, self.a] == ", action)
        random_choice = rand.random()
        if random_choice <= self.rar:
            action = rand.randint(0, self.num_actions - 1)
        elif random_choice > self.rar:
            action = self.Q[s_prime,:].argmax()

        self.rar = self.rar * self.radr
        self.s = s_prime
        self.a = action


        if self.verbose: print ("s =", s_prime,"a =",action,"r =",r)
        return action

if __name__=="__main__":
    print ("Remember Q from Star Trek? Well, this isn't him")

