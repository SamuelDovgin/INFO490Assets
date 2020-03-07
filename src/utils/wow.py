import Tools
print(dir(Tools))
# https://www.dataquest.io/blog/advanced-jupyter-notebooks-tutorial/
## https://towardsdatascience.com/google-drive-google-colab-github-dont-just-read-do-it-5554d5824228
# https://colab.research.google.com/github/fbkarsdorp/python-course/blob/master/answerbook/Chapter%2010%20-%20Learning%20without%20Supervision.ipynb#scrollTo=GVu_RoIarsWI
import urllib
import importlib
id='1tkNkvGsZARYKFNLk6BIA_GLS7Z6JMXEb'
id='1JaBOzRUM3pgbYVFpU640SjxCjH7SH98N' # Tools.py
def install_module(doc_id, filename, force=False):

  import os
  if not force and os.path.exists(filename):
    return True

  baseurl = "https://drive.google.com/uc"
  params = {"export" : "download",
            "id"     : doc_id}

  url = baseurl + "?" + urllib.parse.urlencode(params)
  r = urllib.request.urlopen(url)
  text = str(r.read().decode('UTF-8'))
  with open(filename, 'w') as fd:
    fd.write(text)
  return text

  # with open('__init__.py', 'w') as fd:
  #   fd.write('')

import os
#os.remove('__init__.py')
#os.remove('Tool2.py')
import sys
#sys.path.append('..')
#from content import Tool2 as test
#print(os.getcwd())
install_module(id, 'Tool3.py')
# mymod = importlib.import_module('Tools')
# print(dir(mymod))
import Tool3 as test
#print(dir(test))
test.hello_world()
notebook_id = '1UiDdydJD4omb-aAqMq1q5bQqggMHv0UH'
import ipywidgets as widgets
from IPython.display import display

def button_test(fn, notebook_id):

  # make sure notebook is readable
  txt = install_module(notebook_id, 'file.json', force=True)
  print(txt)
  if not txt.find('{"nbformat') == 0:
    print("Make notebook viewable")
    return False

  # id of Python helper
  id='1JaBOzRUM3pgbYVFpU640SjxCjH7SH98N' # Tools.py
  install_module(id, 'Tools.py', True)
  import Tools

  cells = Tools.parse(txt)
  print(cells)

  name = fn.__name__
  button = widgets.Button(description="Test " + name)
  output = widgets.Output()

  def on_button_clicked(b):
    # Display the message within the output widget.
    with output:
       print("Button clicked.", name)

  button.on_click(on_button_clicked)
  display(button, output)


def hello_world(a,b):
  return a + b

button_test(hello_world, notebook_id)
from IPython.core.display import HTML
import requests
def css_styling():
    styles = requests.get('https://raw.githubusercontent.com/fbkarsdorp/python-course/master/styles/custom.css')
    txt = styles.text
    idx = txt.find('<style>')
    return txt[idx:]
HTML(css_styling() + '<div class="warning">TEST</div>')
apple_a = {"bad", "red", "firm", "sweet"}
apple_b = {"bad", "yellow", "firm", "sour"}
len(apple_a.difference(apple_b))
apples = [(0, {"bad", "red", "firm", "sweet"}),
          (1, {"bad", "red", "firm", "sour"}),
          (2, {"bad", "yellow", "firm", "sour"}),
          (3, {"good", "red", "soft", "sour"}),
          (4, {"good", "yellow", "soft", "sweet"}),
          (5, {"bad", "yellow", "firm", "sour"})]

n = len(apples)
distances = [[0 for i in range(n)] for _ in range(n)]
for i in range(n):
    for j in range(i):
        distance = len(apples[i][1].difference(apples[j][1]))
        distances[i][j] = distance
        distances[j][i] = distances[i][j]
distances
apples[2] = (6, (apples[2], apples[5]))
del apples[5]
apples
apples[0] = (7, (apples[0], apples[1]))
del apples[1]
apples
apples[0] = (8, (apples[0], apples[1]))
del apples[1]
apples
apples[1] = (9, (apples[1], apples[2]))
del apples[2]
apples
apples[0] = (10, (apples[0], apples[1]))
del apples[1]
apples
def jaccard_distance(a, b):
    # insert your code here
    union_len = len(a.union(b))
    return (union_len - len(a.intersection(b))) / union_len

# these tests should return True if your code is correct
print(jaccard_distance({'a', 'b', 'c'}, {'b', 'c', 'a'}) == 0.0)
print(round(jaccard_distance({'a', 'b', 'c'}, {'b', 'c'}), 2) == 0.33)
def pairwise_distances(X, distance_fn=jaccard_distance):
    # insert your code here
    n = len(X)
    distances = [[0 for i in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i):
            distances[i][j] = distance = distance_fn(X[i], X[j])
            distances[j][i] = distance
    return distances

# these tests should return True if your code is correct
X = [{'a', 'f', 'c'}, {'b', 'd', 'a'}, {'a', 'b', 'c'}, {'f', 'b', 'c'}]
print(pairwise_distances(X) == [[0,   0.8, 0.5, 0.5],
                               [0.8, 0,   0.5, 0.8],
                               [0.5, 0.5, 0,   0.5],
                               [0.5, 0.8, 0.5, 0  ]])
from itertools import combinations

def smallest_distance(dm):
    # insert your code here
    return min(combinations(range(len(dm)), 2), key=lambda i: dm[i[0]][i[1]])

# these tests should return True if your code is correct
distances = [[0, 1, 2, 3, 3, 2],
             [1, 0, 1, 2, 4, 1],
             [2, 1, 0, 3, 3, 0],
             [3, 2, 3, 0, 2, 3],
             [3, 4, 3, 2, 0, 3],
             [2, 1, 0, 3, 3, 0]]
print(smallest_distance(distances) == (2, 5))
class Cluster(list):
    """Represents a Cluster node in a Dendrogram. A Cluster can be
    initialized using

    >>> c = Cluster(1)

    to create a cluster leaf node with id=1. You can also initialize
    a non-terminal `Cluster` node using

    >>> c = Cluster(3, Cluster(1), Cluster(2))

    where Cluster(1) and Cluster(2) are the children of Cluster(3)."""

    def __init__(self, id, *children):
        self.id = id
        super(Cluster, self).__init__(children)

    def __repr__(self):
        childstr = ", ".join(str(c) for c in self)
        if self:
            return '%s(%s, [%s])' % (type(self).__name__, self.id, childstr)
        return '%s(%s)' % (type(self).__name__, self.id)

    def __str__(self):
        return self.pprint()

    def pprint(self, indent=0):
        s = '%s(%s' % (type(self).__name__, self.id)
        for child in self:
            if child:
                s += '\n' + ' ' * (indent + 2) + child.pprint(indent=indent+2)
            else:
                s += '\n' + ' ' * (indent + 2) + '%r' % child
        return s + ')'
c1 = Cluster(1)
c2 = Cluster(2)
print(Cluster(3, c1, c2))
class ClusterTree:
    """A ClusterTree, or Dendrogram consists of one or more
    `Cluster` objects. Initialize a `ClusterTree` using

    >>> tree = ClusterTree(n=10)

    where n is the number of original data points to be clustered."""

    def __init__(self, n, labels=None):
        self._n = n
        if labels is None:
            labels = range(n)
        self._clusters = [Cluster(i) for i in labels]

    def merge(self, i, j):
        # insert your code here
        self._clusters[i] = Cluster(self._n, self._clusters[i], self._clusters.pop(j))
        self._n += 1

    def __str__(self):
        return '%s' % self._clusters[0]

# these tests should return True if your code is correct
tree = ClusterTree(5)
tree.merge(1, 2)
print(len(tree._clusters[1]) == 2)
print(tree._clusters[1].id == 5)
def single_linkage(dm, i, j):
    # insert your code here
    for k in range(len(dm)):
        if k != i and k != j:
            dm[i][k] = distance = min(dm[i][k], dm[j][k])
            dm[k][i] = distance
    dm = [[val for c, val in enumerate(row) if c != j]
               for r, row in enumerate(dm) if r != j]
    return dm

# these tests should return True if your code is correct

distances = [[0, 1, 2, 3, 3, 1],
             [1, 0, 1, 2, 4, 1],
             [2, 1, 0, 3, 3, 0],
             [3, 2, 3, 0, 2, 3],
             [3, 4, 3, 2, 0, 3],
             [1, 1, 0, 3, 3, 0]]

print(single_linkage(distances, 2, 5) == [[0, 1, 1, 3, 3],
                                          [1, 0, 1, 2, 4],
                                          [1, 1, 0, 3, 3],
                                          [3, 2, 3, 0, 2],
                                          [3, 4, 3, 2, 0]])
def cluster(data_points, labels=None, linkage=single_linkage, distance_fn=jaccard_distance):
    # initialize a `ClusterTree` with n=len(data_points)
    tree = ClusterTree(len(data_points), labels=labels)
    # compute the pairwise distances between all data points
    # using the provided distance function
    dm = pairwise_distances(data_points, distance_fn=distance_fn) # insert your code here
    while len(dm) > 1:
        # extract the indices of the clusters corresponding to the
        # two closest clusters in the distance matrix
        i, j = smallest_distance(dm) # insert your code here
        # update the distance matrix using the provided linkage function
        dm = linkage(dm, i, j) # insert your code here
        # merge the two clusters in the ClusterTree:
        tree.merge(i, j) # insert your code here
    return tree

# these tests should return True if your code is correct
apples = [{"bad", "red", "firm", "sweet"}, {"bad", "red", "firm", "sour"},
          {"bad", "yellow", "firm", "sour"}, {"good", "red", "soft", "sour"},
          {"good", "yellow", "soft", "sweet"}, {"bad", "yellow", "firm", "sour"}]
tree = cluster(apples)
print(tree._clusters[0].id == 10)
def general_linkage(dm, i, j, distance_fn):
    for k in range(len(dm)):
        if k != i and k != j:
            dm[i][k] = distance = distance_fn(dm[i][k], dm[j][k])
            dm[k][i] = distance
    dm = [[val for c, val in enumerate(row) if c != j]
               for r, row in enumerate(dm) if r != j]
    return dm
def single_linkage(dm, i, j):
    return general_linkage(dm, i, j, min)
def complete_linkage(dm, i, j):
    # insert your code here
    return general_linkage(dm, i, j, max)

# these tests should return True if your code is correct

distances = [[0, 1, 2, 3, 3, 1],
             [1, 0, 1, 2, 4, 1],
             [2, 1, 0, 3, 3, 0],
             [3, 2, 3, 0, 2, 3],
             [3, 4, 3, 2, 0, 3],
             [1, 1, 0, 3, 3, 0]]

complete_linkage(distances, 2, 5) == [[0, 1, 2, 3, 3],
                                      [1, 0, 1, 2, 4],
                                      [2, 1, 0, 3, 3],
                                      [3, 2, 3, 0, 2],
                                      [3, 4, 3, 2, 0]]
numerals = [
   ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"],
   ["een", "twee", "drie", "vier", "vijf", "zes", "zeven", "acht", "negen", "tien"],
   ["ien", "twa", "trije", "fjouwer", "fiif", "seis", "san", "acht", "njoggen", "tsien"],
   ["eins", "zwei", "drei", "vier", "funf", "sechs", "sieben", "acht", "neun", "zehn"],
   ["en", "to", "tre", "fire", "fem", "seks", "sju", "atte", "ni", "ti"],
   ["én", "to", "tre", "fire", "fem", "seks", "syv", "otte", "ni", "ti"],
   ["en", "tva", "tre", "fyra", "fem", "sex", "sju", "atta", "nio", "tio"],
   ["uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez"],
   ["un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix"],
   ["uno", "due", "tre", "quattro", "cinque", "sei", "sette", "otto", "nove", "dieci"]]

languages = ['English', 'Dutch', 'Frisian', 'German', 'Norwegian',
             'Danish', 'Swedish', 'Spanish', 'French', 'Italian']
dutch_one = set(list("een"))
english_one = set(list("one"))
jaccard_distance(dutch_one, english_one)
def summed_jaccard_distance(A, B):
    # insert your code here
    return sum(jaccard_distance(set(list(a)), set(list(b))) for a, b in zip(A, B))

# these tests should return True if your code is correct
print(round(summed_jaccard_distance(numerals[0], numerals[4]), 2) == 5.57)
print(round(summed_jaccard_distance(numerals[5], numerals[6]), 2) == 4.8)
solution = cluster(numerals, labels=languages,
                   distance_fn=summed_jaccard_distance) # insert your code here
print(solution)
from IPython.core.display import HTML
def css_styling():
    styles = open("styles/custom.css", "r").read()
    return HTML(styles)
css_styling()