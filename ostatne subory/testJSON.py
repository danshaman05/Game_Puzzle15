#test JSON:

import json

pole = [[[0, 2], [2, 3]], [0, 0], [2, 2]]

def save():
    with open('rozohrata.txt', 'w') as f:
        json.dump(pole, f)

save()

##j = []

def load():
    j = json.load(open('rozohrata.txt'))
    print(pole==j)

load()
##print(j)

#VYSLEDKO TESTU:
##JSON  vie robit aj s 3-dim poliami
