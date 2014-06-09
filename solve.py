from __future__ import print_function
import sys


def debug(*objs):
  print(*objs, file=sys.stderr)
  
  
class Coordinate:
  
  def __init__(self, x_start, x_end, y_start, y_end):
    self.x_start, self.x_end = x_start, x_end
    self.y_start, self.y_end = y_start, y_end
    self.x, self.y = self.x_start, self.y_start

  def next():   # => True if it advances, False if not
    if self.x < self.x_end:
      self.x += 1
      return True
    elif self.y < self.y_end:
      self.x = self.x_start
      self.y += 1
      return True
    else:
      return False
      
      
class Node:
  
  def __init__(self, coordinate):
    self.coordinate = coordinate
  
  
class Connection:
  
  def __init__(self, node1, node2):
    self.node1 = node1 * 2
    self.node2 = node2 * 2
    
  def length_squared(self, solution):
    x_squared = (solution[self.node2] - solution[self.node1]) ** 2
    y_squared = (solution[self.node2+1] - solution[self.node1+1]) ** 2
    return x_squared + y_squared
    
  def __str__(self):
    return "Test(node1:%d, node2:%d)" % (self.node1, self.node2)


num_nodes = 4
num_variables = num_nodes * 2
max_domain = 6
domain = [1,2,3,4,5]
universe = [domain] * num_variables
universe[0] = [1]   # first node must be at (x,y) = (left, middle)
universe[1] = [3]
candidate_solution = [None] * num_variables
all_solutions = []
occupied = [[0 for x in xrange(max_domain+1)] for y in xrange(max_domain+1)] 
scale = 20


# build connections
connections = [
  Connection(0, 1),
  Connection(1, 2),
  Connection(2, 3),
  Connection(0, 2),
]


def find_all_solutions(i):
  if i == num_variables:
    save_candidate_solution(candidate_solution)
  else:
    for value in universe[i]:
      candidate_solution[i] = value
      result = True
      if (i % 2) == 1:
        occupied[ candidate_solution[i-1] ][ candidate_solution[i] ] += 1
        if occupied[ candidate_solution[i-1] ][ candidate_solution[i] ] > 1:
          result = False
      if result:
        find_all_solutions(i+1)
      if (i % 2) == 1:
        occupied[ candidate_solution[i-1] ][ candidate_solution[i] ] -= 1
      candidate_solution[i] = None

      
def save_candidate_solution(candidate_solution):
    all_solutions.append(list(candidate_solution))
  
  
def nice_closest_to_x_axis(solution):
  nice = 0
  for y in range(1, num_variables, 2):
    nice += abs(solution[y] - 5)
  return nice


def nice_closest_together(solution):
  nice = 0
  for connection in connections:
    nice += connection.length_squared(solution)
  return nice
  

def nice_number_of_nodes_on_x_axis(solution):
  nice = 0
  for y in range(1, num_variables, 2):
    if solution[y] == 5: nice += 1
  return (-1 * nice)    # make negative so that smaller values are better


def find_nice_solutions(all_solutions, nice_function):
  best = float("inf")
  nice_solutions = []
  for solution in all_solutions:
    nice = nice_function(solution)
    if nice < best:
      nice_solutions = [solution]
      best = nice
    elif nice == best:
      nice_solutions.append(solution)
  return nice_solutions


def print_solutions(solutions):
  output_start()
  for solution in solutions: 
    output(solution)
  output_end()


def output_start():
  print( """\
      <!DOCTYPE html>
      <html>
        <body>
    """ )
  

def output(solution):
  
  # start svg tag
  print( """\
    <svg width='%d' height='%d' viewBox='-1,-1,%d,%d' style='margin:1em;'>
    """ % ((max_domain + 1) * scale, (max_domain + 1) * scale, (max_domain + 1) * scale, (max_domain + 1) * scale) )
    
  # horizontal grid lines
  for y in xrange(0, max_domain + 1):
    print( """
      <line x1='0' y1='%d' x2='%d' y2='%d' stroke='#eee' stroke-width='1' shape-rendering='crispEdges' />
      """ % (y * scale, max_domain * scale, y * scale) )
      
  # vertical grid lines
  for x in xrange(0, max_domain + 1):
    print( """
      <line x1='%d' y1='0' x2='%d' y2='%d' stroke='#eee' stroke-width='1' shape-rendering='crispEdges' />
      """ % (x * scale, x * scale, max_domain * scale) )
  
  # connections
  for connection in connections:
    x1, y1 = solution[connection.node1] * scale, solution[connection.node1 + 1] * scale
    x2, y2 = solution[connection.node2] * scale, solution[connection.node2 + 1] * scale
    print( "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='black' stroke-width='1' shape-rendering='crispEdges' />" % (x1, y1, x2, y2) )
    
  # nodes
  for i in range(0, num_variables, 2):
    x, y = solution[i] * scale, solution[i+1] * scale
    print( "<rect x='%d' y='%d' width='15' height='15' stroke='black' stroke-width='1' shape-rendering='crispEdges' fill='yellow' />" % (x-8, y-8) )
    print( "<text x='%d' y='%d' font-family=Monospace style='text-anchor: middle;'>%d</text>" % (x, y+3, (i / 2)) )
    
  # end svg tag
  print( """\
    </svg>
    """ )
  

def output_end():
  print( """\
    </body>
  </html>
  """ )


find_all_solutions(0)
solutions = all_solutions
#solutions = find_nice_solutions(solutions, nice_closest_to_x_axis)
solutions = find_nice_solutions(solutions, nice_closest_together)
#solutions = find_nice_solutions(solutions, nice_number_of_nodes_on_x_axis)
print_solutions(solutions)
