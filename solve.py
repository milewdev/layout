from __future__ import print_function
import sys


def debug(*objs):
  print(*objs, file=sys.stderr)
  
  
num_nodes = 4
max_domain = 6
scale = 20
all_solutions = []
solution = []


#
# This is an immutable class, hence the overridden __setattr__() and
# __delattr__(), and the odd call to object.__setattr__() in __init__().
#
# See: http://www.craigmbooth.com/python-fragments-1-a-class-with-immutable-attributes/
#
class Coordinate:
  
  def __init__(self, x, y):
    object.__setattr__(self, "x", x)
    object.__setattr__(self, "y", y)
    
  def __setattr__(self, *args):
    raise AttributeError("Coordinate is immutable")
    
  def __delattr__(self, *args):
    raise AttributeError("Coordinate is immutable")
  
  
class CoordinateIterator:
  
  def __init__(self, x_start, x_end, y_start, y_end):
    self.x_start = x_start
    self.x_end = x_end
    self.y_start = y_start
    self.y_end = y_end
    self.reset()

  def reset(self):
    self.x = self.x_start - 1 
    self.y = self.y_start
    
  def next(self):   # => True if it advances, False if not
    if self.x < self.x_end:
      self.x += 1
      return True
    elif self.y < self.y_end:
      self.x = self.x_start
      self.y += 1
      return True
    else:
      return False
      
  def __str__(self):
    return "(x: %d, y: %d)" % (self.x, self.y)
      
      
class Node:
  
  def __init__(self, coord_index):
    self.coord_index = coord_index
    
  def coord(self):
    coordinate = solution[self.coord_index]
    return Coordinate( coordinate.x, coordinate.y )
    
  def __str__(self):
    return "Node(coord_index: %d)" % (self.coord_index)
  
  
class Connection:
  
  def __init__(self, node1, node2):
    self.node1 = node1
    self.node2 = node2
    
  def length_squared(self):
    x_squared = (self.node2.coord().x - self.node1.coord().x) ** 2
    y_squared = (self.node2.coord().y - self.node1.coord().y) ** 2
    return x_squared + y_squared
    
  def __str__(self):
    return "Test(node1: %s, node2: %s)" % (self.node1, self.node2)
    
    
class Occupied:
  
  def __init__(self, x_min, x_max, y_min, y_max):
    self.x_min = x_min
    self.y_min = y_min
    width = x_max - x_min + 1
    height = y_max - y_min + 1
    self.grid = [[0 for x in xrange(width)] for y in xrange(height)] 

  def occupy(self, coordinate):
    self.grid[coordinate.x - self.x_min][coordinate.y - self.y_min] += 1
    
  def vacate(self, coordinate):
    self.grid[coordinate.x - self.x_min][coordinate.y - self.y_min] -= 1
    
  def is_vacant(self, coordinate):
    return self.grid[coordinate.x - self.x_min][coordinate.y - self.y_min] == 0


# node coordinates
node_coordinates = [ CoordinateIterator(1,5,1,5) for i in xrange(num_nodes-1) ]
node_coordinates.insert(0, CoordinateIterator(1,1,3,3))   # first node locked at coordinate (1,3)
  
  
# occupations
occupied = Occupied(0,6,0,6)


# nodes
nodes = [ Node(i) for i in xrange(num_nodes) ]


# connections
connections = [
  Connection(nodes[0], nodes[1]),
  Connection(nodes[1], nodes[2]),
  Connection(nodes[2], nodes[3]),
  Connection(nodes[0], nodes[2]),
]


def find_all_solutions(i):
  if i == len(node_coordinates):
    all_solutions.append(extract_solution(node_coordinates))
  else:
    while node_coordinates[i].next():     # TODO: eliminate train wreck?
      if occupied.is_vacant(node_coordinates[i]):
        occupied.occupy(node_coordinates[i])
        find_all_solutions(i + 1)
        occupied.vacate(node_coordinates[i])
    node_coordinates[i].reset()           # TODO: eliminate train wreck?
      
      
def extract_solution(node_coordinates):
  solution = []
  for coord in node_coordinates:
    clone = Coordinate( coord.x, coord.y )
    solution.append(clone)                # TODO: use coord.clone() instead?
  return solution

      
def save_candidate_solution(candidate_solution):
  all_solutions.append(list(candidate_solution))
  
  
def nice_closest_to_x_axis():
  nice = 0
  for point in solution:
    nice += abs(point.y - 3)
  return nice


def nice_closest_together():
  nice = 0
  for connection in connections:
    nice += connection.length_squared()
  return nice
  

def nice_number_of_nodes_on_x_axis():
  nice = 0
  for point in solution:
    if point.y == 3: nice += 1
  return (-1 * nice)    # make negative so that smaller values are better


def find_nice_solutions(solutions, nice_function):
  global solution
  best = float("inf")
  nice_solutions = []
  for solution in solutions:
    nice = nice_function()
    if nice < best:
      nice_solutions = [solution]
      best = nice
    elif nice == best:
      nice_solutions.append(solution)
  return nice_solutions
  
  
def print_solutions(solutions):
  global solution
  output_start()
  for solution in solutions:
    output()
  output_end()


def output_start():
  print( """\
      <!DOCTYPE html>
      <html>
        <body>
    """ )
  

def output_end():
  print( """\
    </body>
  </html>
  """ )
  
  
def output():
  
  # start svg tag
  print( "<svg width='%d' height='%d' viewBox='-1,-1,%d,%d' style='margin:1em;'>"
    % ((max_domain + 1) * scale, (max_domain + 1) * scale, (max_domain + 1) * scale, (max_domain + 1) * scale) )
    
  # horizontal grid lines
  for y in xrange(0, max_domain + 1):
    print( "<line x1='0' y1='%d' x2='%d' y2='%d' stroke='#eee' stroke-width='1' shape-rendering='crispEdges' />"
      % (y * scale, max_domain * scale, y * scale) )
      
  # vertical grid lines
  for x in xrange(0, max_domain + 1):
    print( "<line x1='%d' y1='0' x2='%d' y2='%d' stroke='#eee' stroke-width='1' shape-rendering='crispEdges' />"
      % (x * scale, x * scale, max_domain * scale) )
  
  # connections
  for connection in connections:
    x1, y1 = connection.node1.coord().x * scale, connection.node1.coord().y * scale
    x2, y2 = connection.node2.coord().x * scale, connection.node2.coord().y * scale
    print( "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='black' stroke-width='1' shape-rendering='crispEdges' />" % (x1, y1, x2, y2) )
  
  # nodes
  for node in nodes:
    x, y = node.coord().x * scale, node.coord().y * scale
    print( "<rect x='%d' y='%d' width='15' height='15' stroke='black' stroke-width='1' shape-rendering='crispEdges' fill='yellow' />" % (x-8, y-8) )
    print( "<text x='%d' y='%d' font-family=Monospace style='text-anchor: middle;'>%s</text>" % (x, y+3, node.coord_index) )
    
  # end svg tag
  print( "</svg>" )


find_all_solutions(0)
solutions = all_solutions
solutions = find_nice_solutions(solutions, nice_closest_to_x_axis)
solutions = find_nice_solutions(solutions, nice_closest_together)
# solutions = find_nice_solutions(solutions, nice_number_of_nodes_on_x_axis)
print_solutions(solutions)
