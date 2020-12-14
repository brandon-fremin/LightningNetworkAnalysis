class Node_Distance:
    def __init__(self, name, dist):
        self.name = name
        self.dist = dist


class Graph:

    def __init__(self, node_count):
        self.adjlist = {}
        self.node_count = node_count

    def Add_Into_Adjlist(self, src, node_dist):
        if src not in self.adjlist:
            self.adjlist[src] = []
        self.adjlist[src].append(node_dist)

    def Dijkstras_Shortest_Path(self, source, display=True):

        # Initialize the distance of all the nodes from source to infinity
        maxx = float("inf")
        distance = {}
        for key in self.adjlist.keys():
            distance[key] = maxx

        # Distance of source node to itself is 0
        distance[source] = 0

        # Create a dictionary of { node, distance_from_source }
        dict_node_length = {source: 0}
        dict_node_prev = {source: "_sentinel"}

        while dict_node_length:

            # Get the key for the smallest value in the dictionary
            # i.e Get the node with the shortest distance from the source
            source_node = min(dict_node_length, key=lambda k: dict_node_length[k])
            del dict_node_length[source_node]

            for node_dist in self.adjlist[source_node]:
                adjnode = node_dist.name
                length_to_adjnode = node_dist.dist

                # Edge relaxation
                if distance[adjnode] > distance[source_node] + length_to_adjnode:
                    distance[adjnode] = distance[source_node] + length_to_adjnode
                    dict_node_length[adjnode] = distance[adjnode]
                    dict_node_prev[adjnode] = str(source_node)

        for key in self.adjlist.keys():
            if display:
                print(f"Source Node ({source[-16:]})  -> Destination Node({key[-16:]})  :  {distance[key]}")
            dict_node_length[key] = distance[key] if distance[key] != maxx else maxx
            if distance[key] == maxx:
                dict_node_prev[key] = None

        return dict_node_length, dict_node_prev
