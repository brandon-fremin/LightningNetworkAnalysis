import random
from src.dijkstras import Graph, Node_Distance
import matplotlib.pyplot as plt
from src.distance import dist_d, cost_d


def path_finder(source, target, amount, all_nodes, channel_balances, verify_function, distance_function, alpha=1.0, show_plot=False, print_text=True):
    graph = Graph(len(all_nodes))
    for key, node in all_nodes.items():
        self_id = node["id"]
        in_graph = False
        for key, channel in node["channels"].items():
            # Remove some edges for no reason
            if random.uniform(0, 1) > alpha:
                continue

            if verify_function(node, channel, channel_balances, amount):
                peer_id = channel["peer_id"]
                distance = distance_function(channel, amount)
                graph.Add_Into_Adjlist(self_id, Node_Distance(peer_id, distance))
                in_graph = True

        # Add a self edge if a node has no edges to carry amount through it
        if not in_graph:
            graph.Add_Into_Adjlist(self_id, Node_Distance(self_id, 1))

    distances, prevs = graph.Dijkstras_Shortest_Path(source, False)
    optimal_route = None
    if (print_text):
        print("*************************************************************")
        print(f"Optimal Path:\nSource: {source}\nTarget: {target}\nAmount: {amount}\nDist  : {distances[target]} units\n")
    if distances[target] != float("inf"):
        curr = target
        route = []
        while curr != "_sentinel":
            route.insert(0, curr)
            curr = prevs[curr]
        if print_text:
            print("Explicit Route: ")
            [print(f"{r}") for r in route]
        optimal_route = route

        if show_plot:
            x, y = [], []
            for r in route:
                if not all_nodes[r]["geo"]:
                    continue
                x.append(all_nodes[r]["geo"]["longitude"])
                y.append(all_nodes[r]["geo"]["latitude"])
            plt.plot(x, y)
            plt.scatter(x, y, c="red", s=50)
            plt.xlim([-180, 180])
            plt.ylim([-90, 90])
            plt.show()

    elif print_text:
        print("No explicit route :(")

    if print_text:
        print("*************************************************************")

    return distances, prevs, optimal_route


def get_disconnected_keys(all_nodes, channel_balances):
    # Two popular nodes that should be connected for forseable future
    source = '028a8e53d70bc0eb7b5660943582f10b7fd6c727a78ad819ba8d45d6a638432c49'
    target = '020ca546d600037181b7cbcd094818100d780d32fd9f210e14390e0d10b7ec71fb'
    amount = 0

    def trivial_verifier(node, channel, channel_balances, amount):
        return True

    distances, prevs, optimal_route = path_finder(source, target, amount,
                                                  all_nodes, channel_balances,
                                                  trivial_verifier,
                                                  dist_d,
                                                  alpha=1)
    print()

    counter = 0
    disconnected_keys = []
    for key in all_nodes.keys():
        if distances[key] == float('inf'):
            disconnected_keys.append(key)
            counter = counter + 1
    print(f"There are {counter} disconnected keys")
    return set(disconnected_keys)


def path_cost(optimal_route, all_nodes, amount):
    if len(optimal_route) == 0:
        return 0

    cost = 0
    for i in range(len(optimal_route) - 1):
        node_id = optimal_route[i]
        next_node_id = optimal_route[i + 1]
        for channel in all_nodes[node_id]["channels"].values():
            if channel["peer_id"] == next_node_id:
                cost = cost + cost_d(channel, amount)
                break

    return cost


def failure_node(optimal_route, all_nodes, channel_balances, amount):
    if not optimal_route or len(optimal_route) == 0:
        return None, None

    for i in range(len(optimal_route) - 1):
        node_id = optimal_route[i]
        next_node_id = optimal_route[i + 1]
        for channel in all_nodes[node_id]["channels"].values():
            if channel["peer_id"] == next_node_id:
                channel_id = channel["short_channel_id"]
                if channel_balances[channel_id][node_id] < amount:
                    # print_json(channel_balances[channel["short_channel_id"]])
                    return node_id, channel_id

    return None, None