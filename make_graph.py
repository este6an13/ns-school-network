import igraph as ig

# mapping classrooms from french system to our system
classrooms_map = {  'cpa': '1stA', 'cpb': '1stB', 'ce1a':'2ndA', 'ce1b':'2ndB', 
                    'ce2a':'3rdA', 'ce2b':'3rdB', 'cm1a':'4thA', 'cm1b':'4thB',
                    'cm2a':'5thA', 'cm2b':'5thB', 'teachers':'teachers' }
# mapping classrooms to grade and age (1st6 means 1st grade, age 6)
grades_map =    {   'cpa': '1st6', 'cpb': '1st6', 'ce1a':'2nd7', 'ce1b':'2nd7', 
                    'ce2a':'3rd8', 'ce2b':'3rd8', 'cm1a':'4th9', 'cm1b':'4th9',
                    'cm2a':'5th10', 'cm2b':'5th10', 'teachers':'teachers'   }
# https://www.frenchtoday.com/blog/french-culture/the-french-school-system-explained/

# key: node_id, values: classroom, contacts, duration
classrooms = {}
contacts = {}
duration = {}

# populating classroom dict with txt data
with open('data/DatasetS3.txt') as f:
    lines = f.readlines()
    for line in lines:
        id = int(line.split()[0])
        classroom = line.split()[1]
        # initialize dicts
        classrooms[id] = classroom
        contacts[id] = 0
        duration[id] = 0

# network of day 1
g = ig.Graph.Read_GML("data/DatasetS1.gml")

# populating contacts and duration dicts
for edge in g.es:
    source_node = int(edge.source_vertex['id'])
    target_node = int(edge.target_vertex['id'])
    # updating edge attributes (counts)
    contacts[source_node] += edge['count']
    duration[source_node] += edge['duration']
    contacts[target_node] += edge['count']  
    duration[target_node] += edge['duration']

# setting nodes attributes:
    # classroom and grade (with age) based on classrooms dict
    # contacts and duration based on contacts and duration dicts
for node in g.vs:
    node_id = int(node['id'])
    classroom = classrooms.get(node_id)
    # setting nodes attributes
    node['classroom'] = classrooms_map[classroom]
    node['grade'] = grades_map[classroom]
    node['contacts'] = contacts.get(node_id)
    node['duration'] = duration.get(node_id)

# network of day 2
g = ig.Graph.Read_GML("data/DatasetS2.gml")

# populating contacts and duration dicts
for edge in g.es:
    source_node = int(edge.source_vertex['id'])
    target_node = int(edge.target_vertex['id'])
    # updating edge attributes (counts)
    contacts[source_node] += edge['count']
    duration[source_node] += edge['duration']
    contacts[target_node] += edge['count']  
    duration[target_node] += edge['duration']

# setting nodes attributes:
    # classroom and grade (with age) based on classrooms dict
    # contacts and duration based on contacts and duration dicts
for node in g.vs:
    node_id = int(node['id'])
    classroom = classrooms.get(node_id)
    # setting and updating nodes attributes
    node['classroom'] = classrooms_map[classroom]
    node['grade'] = grades_map[classroom]
    node['contacts'] = contacts.get(node_id)
    node['duration'] = duration.get(node_id)

ig.write(g, "results/Graph.gml", format="gml")

# to eliminate edges of less than 2 min in duration
g = ig.Graph.Read_GML("results/Graph.gml")
g.delete_edges(g.es.select(duration_lt=120))
ig.write(g, "results/Subgraph.gml", format="gml")


