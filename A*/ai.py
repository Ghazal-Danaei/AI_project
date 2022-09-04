import random
from collections import deque
import json

import numpy as np

from modeled_env import ModeledEnv, set_constants
from time import time
from queue import PriorityQueue

class Agent:
    def __init__(self, perceive_func=None, agent_id=None, optimized=False, mode='a_star'):
        self.perceive_func = perceive_func
        self.my_id = agent_id

        self.predicted_actions = []
        self.actions_list = ['up', 'right', 'down', 'left']

        self.optimized = optimized
        self.alg = eval('self.'+mode)
        print('running '+mode)

    def act(self):
        sensor_data = self.perceive_func(self)
        if self.optimized:
            set_constants(json.loads(sensor_data['Current_Env'])['state'])
            sensor_data['Current_Env'] = ModeledEnv()
        else:
            from env import Env
            sensor_data['Current_Env'] = Env([1], [1]).from_json(**json.loads(sensor_data['Current_Env'])['state'])

        if self.predicted_actions == []:
            t0=time()
            self.predicted_actions = self.alg(sensor_data['Current_Env'])
            print(time()-t0)

        action = self.predicted_actions.pop()

        return action

    def bfs(self, root_game):
        q = []
        q.append([root_game, []])

        while q:
            # pop first element from queue
            node = q.pop(0)

            if random.random()<0.2: random.shuffle(self.actions_list)
            for action in self.actions_list:
                # add children to queue
                child_game = node[0].create_copy()
                if 'd' not in child_game.take_action(action, self.my_id):
                    q.append([child_game, [action] + node[1]])
                # goal test
                if child_game.goal_test(): return [action] + node[1]



    def heuristic(self, state):
        score = state.agent_list[self.my_id].foodScore
        return np.sqrt(40 - score)

    def a_star(self, root_game):
        y = 10
        q = PriorityQueue()
        q.put((0, 0, [root_game, []]))


        while q:
            # pop first element from queue
            node = q.get()[2][1]
            if random.random() < 0.2: random.shuffle(self.actions_list)
            for action in self.actions_list:
                # add children to queue
                child_game = node[0].create_copy()
                if 'd' not in child_game.take_action(action, self.my_id):
                    agent = child_game.state.agent_list[self.my_id]
                    x = agent.realCost
                    q.put((self.heuristic(child_game.state) + x,  x*y*y,
                           [child_game, [action] + node[1]]))
                    y = y+5
                # goal test
                if child_game.goal_test(): return [action] + node[1]

