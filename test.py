import gymnasium as gym
from connections.calculi.classical import ConnectionEnv, ConnectionState, ConnectionAction
from connections.utils.cnf_parsing import file2cnf
from os import listdir
from os.path import isfile, join
import time


def map_actions(actions: list[ConnectionAction]):
    return gym.Discrete(len(actions))

def map_state(state : ConnectionState):
    multiplier = int(state.iterative_deepening)
    matrix = state.matrix
    tableau = state.tableau
    sigma = state.substitutions


class GymWrapper(gym.Env):
    def __init__(self, connection_env : ConnectionEnv):
        self.internal_env = connection_env
        self.action_space = gym.Discrete(len(self.internal_env.action_space))
        self.observation_space = gym.Box(self.internal_env.state)

    def reset(self):
        self.internal_env.reset()

    def step(self):
        action = self.env.action_space[0]
        return self.internal_env.step(action)

file = "tests/cnf_problems/SYN001+1.p"

def describe_features(observation : ConnectionState):
    print(f"Path: {observation.tableau}\n")
    if observation.goal is not None:
        print(f"Current goal: {observation.goal.path()}\n")
        print(f"Actions: {observation.goal.actions}\n")

def run_file(file):
    start_time = time.time()
    output = ""
    env = ConnectionEnv(file)
    print(env.matrix.clauses)
    observation = env.reset()
    while True:
        action = env.action_space[0]
        observation, reward, done, info = env.step(action)
        describe_features(observation)
        print("\n\n")
        if done:
            end_time = time.time()
            output += str(env.state.proof_sequence)
            output += "\n"
            output += str(env.state.tableau)
            output += "\n"
            output += str(info)
            print(f"Total time: {end_time - start_time}")
            return output


#run_file(file)
print(run_file("some_pets_are_cats.p"))      


#my_wrapper = GymWrapper(env)

#print(my_wrapper)





