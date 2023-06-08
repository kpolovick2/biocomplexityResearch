import ILP_linear as ilp

D_wine = ilp.ILP_linear("../UCI datasets/wine/wine_data.txt")
D_iris = ilp.ILP_linear("../UCI datasets/iris/iris_data.txt")
D_shroom = ilp.ILP_linear("../UCI datasets/mushroom/mushroom_data.txt")
print(D_shroom)