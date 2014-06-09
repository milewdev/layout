from constraint import *

num_nodes = 5
domain = [20,40,60,80,100]
problem = Problem()

# custom constraint functions
def right_or_below_constraint(x1, y1, x2, y2):
  return ((x2 == x1 + 20) and (y2 == y1)) or ((x2 == x1) and (y2 == y1 + 20))
  
def first_state_constraint(x, y):
  return x == 20 and y == 60

# define variables
for i in range(1, num_nodes + 1):
  problem.addVariables( [ "x%d" % i, "y%d" %i ], domain )

# specify constraints
problem.addConstraint( first_state_constraint, ["x1", "y1"] )
for i in range(1, num_nodes):
  problem.addConstraint( right_or_below_constraint, [ "x%d" % i, "y%d" % i, "x%d" % (i + 1), "y%d" % (i + 1) ] )

print( """\
    <!DOCTYPE html>
    <html>
      <body>
  """ )
for solution in problem.getSolutions():
    print( """\
      <svg width='120' height='120' viewBox='0,0,120,120'>
        <rect x='0' y='0' width='120' height='120' stroke='gray' stroke-width-'1' fill='white' />
      """ )
    xs, ys = solution["x1"], solution["y1"]
    for i in range(2, num_nodes + 1):
      xe, ye = solution["x%d" % i], solution["y%d" % i]
      print( "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='black' stroke-width='1px' />" % (xs, ys, xe, ye) )
      xs, ys = xe, ye
    for i in range(1, num_nodes + 1):
      x, y = solution["x%d" % i], solution["y%d" % i]
      print( "<circle cx='%d' cy='%d' r='5' stroke='black' stroke-width='1' fill='red' />" % (x, y) )
    print( """\
      </svg>
    """ )
print( """\
  </body>
</html>
""" )
