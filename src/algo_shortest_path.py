import time
from src.verifier import outsider_verify
from src.path_finder import path_finder, failure_node


def shortest_path(source, target, amount, all_nodes, channel_balances, distance_function, route_evaluator):
    start_time = time.time()
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(f"Shortest Path Algorithm:\nSource: {source}\nTarget: {target}\nAmount: {amount}")

    blacklist = []

    def blacklist_verifier(node, channel, channel_balances, amount):
        if channel["short_channel_id"] in blacklist:
            return False
        else:
            return outsider_verify(node, channel, channel_balances, amount)

    num_tries = 1
    hops = 0
    optimal = None
    while num_tries <= 10:
        distances, prevs, optimal_route = path_finder(source, target, amount,
                                                      all_nodes, channel_balances,
                                                      blacklist_verifier,
                                                      distance_function,
                                                      alpha=1, show_plot=False, print_text=False)
        if not optimal_route:
            print("No Valid Path!")
            break

        f_node_id, f_channel_id = failure_node(optimal_route, all_nodes, channel_balances, amount)
        if f_node_id:
            blacklist.append(f_channel_id)
            num_tries = num_tries + 1
            hops = hops + optimal_route.index(f_node_id)
            if num_tries > 10:
                print("Depleted Attempts!")
        else:
            hops = hops + len(optimal_route) - 1
            optimal = optimal_route
            break

    if optimal:
        print(f"Optimal route required {num_tries} attempts, {hops} hops:")
        [print(o) for o in optimal]
    else:
        pass

    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    runtime = time.time() - start_time
    return {
        "source": source,
        "target": target,
        "num_tries": num_tries,
        "hops_taken": hops,
        "final_dist": route_evaluator(optimal),
        "runtime": runtime
    }