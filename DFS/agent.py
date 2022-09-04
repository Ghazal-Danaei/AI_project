import random
from copy import deepcopy
from env import Env
import json
import sys
sys.setrecursionlimit(10**6)

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

        if self.predicted_actions==[]: self.predicted_actions=self.dfs(sensor_data['Current_Env'])
        action=self.predicted_actions.pop()

        ######### END OF EDITABLE SECTION #########

        return action

    ######### VV EDITABLE SECTION VV #########
    def dfs(self,  root_env):
        s = t = 0


        if root_env.goal_test():
            return [True, "found the goal"]
        else:
            while True:
                actions_list = ["right", "left", "up", "down"]
                random.shuffle(actions_list)
                for action in actions_list:
                    child_game = deepcopy(root_env)
                    game_result = child_game.take_action(action, self.my_id)
                    snake1 = child_game.state.agent_list[self.my_id]
                    if ('has died' not in game_result) :
                        dfs_result = self.dfs(child_game)
                        actions_taken = deepcopy(dfs_result[1]) if type(dfs_result[1]) is list else []
                        actions_taken.append(action)
                        if dfs_result[0]:
                                return [True, actions_taken]


        return [False, "no good action found"]
