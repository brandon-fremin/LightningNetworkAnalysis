import time
from src.verifier import outsider_verify
from src.path_finder import path_finder, failure_node


def random_routing(source, target, amount, all_nodes, channel_balances, valid_ids, distance_function, route_evaluator):
    start_time = time.time()
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(f"Random Routing Algorithm:\nSource: {source}\nTarget: {target}\nAmount: {amount}")

    blacklist = []

    def blacklist_verifier(node, channel, channel_balances, amount):
        if channel["short_channel_id"] in blacklist:
            return False
        else:
            return outsider_verify(node, channel, channel_balances, amount)

    num_tries = 1
    hops = 0
    optimal = []
    choosable_ids = (set(valid_ids) - {source}) - {target}
    large_number = 123456789
    while num_tries <= 20:
        middle_man_1 = list(choosable_ids)[large_number % len(choosable_ids)]
        choosable_ids = choosable_ids - {middle_man_1}
        middle_man_2 = list(choosable_ids)[large_number % len(choosable_ids)]

        distances, prevs, path_1 = path_finder(source, middle_man_1, amount,
                                                      all_nodes, channel_balances,
                                                      blacklist_verifier,
                                                      distance_function,
                                                      alpha=1, show_plot=False, print_text=False)

        distances, prevs, path_2 = path_finder(middle_man_1, middle_man_2, amount,
                                               all_nodes, channel_balances,
                                               blacklist_verifier,
                                               distance_function,
                                               alpha=1, show_plot=False, print_text=False)

        distances, prevs, path_3 = path_finder(middle_man_2, target, amount,
                                               all_nodes, channel_balances,
                                               blacklist_verifier,
                                               distance_function,
                                               alpha=1, show_plot=False, print_text=False)

        if (not path_1) or (not path_2) or (not path_3):
            num_tries = num_tries + 1
            if num_tries > 20:
                print("Depleted Attempts!")
            continue

        optimal_route = []
        optimal_route.extend(path_1)
        optimal_route.extend(path_2[1: -1])
        optimal_route.extend(path_3)

        f_node_id, f_channel_id = failure_node(optimal_route, all_nodes, channel_balances, amount)
        if f_node_id:
            blacklist.append(f_channel_id)
            num_tries = num_tries + 1
            hops = hops + optimal_route.index(f_node_id)
            if num_tries > 20:
                print("Depleted Attempts!")
        else:
            hops = hops + len(optimal_route) - 1
            optimal = optimal_route
            break

    if len(optimal) > 0:
        print(f"Route required {num_tries} attempts, {hops} total hops:")
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
