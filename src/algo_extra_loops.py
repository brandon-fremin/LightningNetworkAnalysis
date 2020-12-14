import time
from src.verifier import outsider_verify
from src.path_finder import path_finder, failure_node


def exclusive_path(source, target, optimal_route, all_nodes, channel_balances, amount, distance_function):
    if not optimal_route or len(optimal_route) < 2:
        return optimal_route

    exclusion_list = optimal_route
    def exclusive_verify(node, channel, channel_balances, amount):
        source_id = node["id"]
        target_id = channel["peer_id"]
        if (source_id in exclusion_list) and (target_id in exclusion_list):
            return False
        else:
            return outsider_verify(node, channel, channel_balances, amount)

    distances, prevs, opt = path_finder(source, target, amount,
                                                  all_nodes, channel_balances,
                                                  exclusive_verify,
                                                  distance_function,
                                                  alpha=1, show_plot=False, print_text=False)

    if not opt:
        return [source, target]
    else:
        assert len(optimal_route) >= 3
        return opt


def extra_loops(source, target, amount, all_nodes, channel_balances, distance_function, route_evaluator):
    start_time = time.time()
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(f"Extra Loops Algorithm:\nSource: {source}\nTarget: {target}\nAmount: {amount}")

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

        list_ptr = 0
        while list_ptr < len(optimal_route) - 1:
            curr = optimal_route[list_ptr]
            next = optimal_route[list_ptr + 1]
            slice = exclusive_path(curr, next, optimal_route, all_nodes, channel_balances, amount, distance_function)
            slice = slice[1: -1]
            length = len(slice)
            optimal_route[list_ptr + 1: list_ptr + 1] = slice
            list_ptr = list_ptr + length + 1

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

