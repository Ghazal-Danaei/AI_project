import random
from copy import deepcopy
from env import Env
import json

class Agent:
    def __init__(self, perceive_func=None, agent_id=None):
        self.perceive_func = perceive_func
        self.my_id = agent_id

        ######### EDITABLE SECTION #########

        self.predicted_actions = []

        ######### END OF EDITABLE SECTION #########

    def act(self):
        sensor_data = self.perceive_func(self)
        sensor_data['Current_Env'] = Env([1], [1]).from_json(**json.loads(sensor_data['Current_Env'])['state'])

        ######### EDITABLE SECTION #########

        if self.predicted_actions==[]: self.predicted_actions=self.bfs(sensor_data['Current_Env'])
        action=self.predicted_actions.pop()

        ######### END OF EDITABLE SECTION #########

        return action

    ######### VV EDITABLE SECTION VV #########
    def bfs(self, game):
        q = []
        q.append([game, []])
        while q:


            node = q.pop(0)


            if node[0].goal_test():
                return node[1]


            actions_list = ["right", "left", "up", "down"]
            random.shuffle(actions_list)

            for action in actions_list:
                child_game = node[0].create_copy()
                if 'has died' not in child_game.take_action(action, self.my_id):
                    q.append([child_game, [action] + node[1]])