from model.model import Model

myModel = Model()
myModel.getAllTeams("2015")
myModel._creaGrafo("2015")
print(myModel.getGraphDetails())

path, sol = myModel.percorso(2777)
print("Peso ", sol)
for p in path:
    print(p)

