import json
def loadk():
    with open("training.json", "r") as readfile:
        global lis
        lis = json.load(readfile)
        age = lis['age']
        name = lis['name']
    print(age, name)

def white():
    with open("training.json", "w") as whritefile:
        lis["place"] = "Grodno"
        json.dump(lis, whritefile)
loadk()
white()