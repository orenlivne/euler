'''
Created on Aug 9, 2015

@author: oren
'''
import networkx as nx

def load_graph(file_name):
    adoption_ids_by_person = {}
    persons_by_adoption_id = {}
    f = open(file_name, 'rb')
    f.next() # Ignore header line
    data = [x.strip().split() for x in f]
    for person, adoption_id in data:
        adoption_ids_by_person.setdefault(person, set()).add(adoption_id)
        persons_by_adoption_id.setdefault(adoption_id, set()).add(person)
   
    g = nx.Graph()
    g.add_nodes_from(adoption_ids_by_person.iterkeys())
    edge_list = {}
    for adoption_id, clique in persons_by_adoption_id.iteritems():
        for person1, person2 in ((person1, person2) for person1 in clique for person2 in clique if person2 != person1): 
            key = (person1, person2) if person1 < person2 else (person2, person1)
            value = edge_list.setdefault(key, 0)   
            edge_list[key] = value + 1
    g.add_weighted_edges_from((person1, person2, weight) for ((person1, person2), weight) in edge_list.iteritems())
    return g

if __name__ == '__main__':
    g = load_graph('c:/users/oren/downloads/in.txt')
    print 'nodes', g.number_of_nodes(), 'edges', g.number_of_edges()
    