from os import listdir
from os.path import isfile, join

directory = "tests/cnf_problems"
onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
print(onlyfiles)