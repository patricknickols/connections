from connections.calculi.classical import ConnectionEnv
from os import listdir
from os.path import isfile, join
import time

def run_file(file, timeout):
    output = ""
    env = ConnectionEnv(file)
    observation = env.reset()
    timeout = time.time() + timeout  # timeout is in seconds
    while True:
        action = env.action_space[0]
        observation, reward, done, info = env.step(action)
        if time.time() > timeout:
            return "Timed out"
        if done:
            output += str(env.state.proof_sequence)
            output += "\n"
            output += str(env.state.tableau)
            output += "\n"
            output += str(info)
            return output


def make_benchmark(timeout):
    filename = f"Baseline_results_{timeout}s.txt"
    with open(filename, "w") as f:
        directory = "tests/cnf_problems"
        onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
        for file in onlyfiles:
            f.write(f"Filename: {file} \n")
            f.write(run_file(f"{directory}/{file}", timeout))
            f.write("\n")

def analyse_benchmark(file):
    timeout_count = 0
    solved_count = 0
    with open(file, "r") as f:
        for line in f:
            if line == "Timed out\n":
                timeout_count += 1
            if line == "{'status': 'Theorem'}\n":
                solved_count += 1
    print(f"Timeout count: {timeout_count}")
    print(f"Solved count: {solved_count}")

