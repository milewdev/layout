from constraint import *
problem = Problem()
problem.addVariables(["a", "b"], [1, 2])
def func(a, b):
  return b > a
problem.addConstraint(func, ["a", "b"])
print(problem.getSolution())
