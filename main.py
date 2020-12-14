from src.helper import load, save, print_json
from src.path_finder import path_cost, get_disconnected_keys
from src.algo_shortest_path import shortest_path
from src.algo_extra_loops import extra_loops
from src.algo_random_routing import random_routing
from src.distance import dist_d, cost_d
from src.collect_data import collect_data, merge_collected_data
from src.channel_balances import define_channel_balances
from src.plotter import box_plot


def reload_live_data():
    print("Collecting data will take a few hours...")
    collect_data()
    all_nodes, all_channels = merge_collected_data()
    save(all_nodes, "all_nodes.pkl")
    save(all_channels, "all_channels.pkl")
    return all_nodes, all_channels


def randomize_channel_balances(all_nodes, all_channels):
    channel_balances = define_channel_balances(all_nodes, all_channels)
    disconnected_keys = get_disconnected_keys(all_nodes, channel_balances)
    save(channel_balances, "channel_balances.pkl")
    save(disconnected_keys, "disconnected_keys.pkl")
    return channel_balances, disconnected_keys


def collect_data_to_compare_algorithms(all_nodes, channel_balances, disconnected_keys):
    answers_short = []
    answers_loop = []
    answers_rand = []

    valid_ids = tuple(set(all_nodes.keys()) - disconnected_keys)
    amount = 0

    def dist_eval(optimal):
        return len(optimal) - 1 if optimal else float("inf")

    large_number = 123456789
    factor = 1234

    valid_ids = list(valid_ids)

    user_input = input("How many trials would you like to run? ")
    try:
        num_trials = int(user_input)
    except:
        num_trials = 10

    user_input = input("How many satoshi would you like to route? ")
    try:
        amount = int(user_input)
    except:
        amount = 10

    user_input = input("Enter a filename to store the resulting pickled file: ")
    if user_input:
        filename = str(user_input) + ".pkl"
    else:
        filename = "1.pkl"

    for i in range(num_trials):
        source = valid_ids[large_number % len(valid_ids)]
        large_number = (large_number % len(valid_ids)) * factor
        target = valid_ids[large_number % len(valid_ids)]
        large_number = (large_number % len(valid_ids)) * factor
        answers_short.append(shortest_path(source, target, amount, all_nodes, channel_balances, dist_d, dist_eval))
        if answers_short[-1]["final_dist"] == float("inf"):
            empty_answer = {
                "source": source,
                "target": target,
                "num_tries": 0,
                "hops_taken": 0,
                "final_dist": float("inf"),
                "runtime": 0
            }
            answers_loop.append(empty_answer)
            answers_rand.append(empty_answer)
            continue
        answers_loop.append(extra_loops(source, target, amount, all_nodes, channel_balances, dist_d, dist_eval))
        answers_rand.append(
            random_routing(source, target, amount, all_nodes, channel_balances, valid_ids, dist_d, dist_eval))

    results = {
        "answers_short": answers_short,
        "answers_loop": answers_loop,
        "answers_rand": answers_rand
    }

    save(results, filename)

    print(f"Results have been saved in {filename}")


def plot_existing_data():
    filename = input("Select filename [include as written in pickles folder]: ")
    box_plot(filename)
    

def route_transaction(all_nodes, channel_balances, disconnected_keys):
    valid_ids = tuple(set(all_nodes.keys()) - disconnected_keys)
    amount = 0

    def dist_eval(optimal):
        return len(optimal) - 1 if optimal else float("inf")

    def cost_eval(optimal):
        if not optimal:
            return float("inf")
        else:
            return path_cost(optimal, all_nodes, amount)

    user_input = input("Enter a source public key: ")
    while user_input not in all_nodes.keys():
        if user_input == "q":
            return
        user_input = input("Coudln't locate that pubkey :(\nPlease enter another pubkey: ")
    source = user_input
    if user_input == "q":
        return

    user_input = input("Enter a target public key: ")
    while user_input not in all_nodes.keys():
        if user_input == "q":
            return
        user_input = input("Coudln't locate that pubkey :(\nPlease enter another pubkey: ")
    target = user_input
    if user_input == "q":
        return

    user_input = input("Enter and amount to send, in satoshi: ")
    try:
        if user_input == "q":
            return
        amount = int(user_input)
    except:
        amount = -1
    while amount < 0:
        user_input = input("Invalid amount :(\nPlease enter another amount: ")
        try:
            if user_input == "q":
                return
            amount = int(user_input)
        except:
            amount = -1
    if user_input == "q":
        return

    valid_options = ["0", "1", "q"]
    user_input = input(
        "Select a scoring metric: \n[0] Hop Distance\n[1] Cost\nChoice: ")
    while user_input not in valid_options:
        user_input = input("Invalid selection :(\nSelect a scoring metric: \n[0] Hop Distance\n[1] Cost\nChoice: ")

    if user_input == "0":
        distance_function = dist_d
        evaluation_function = dist_eval
    elif user_input == "1":
        distance_function = cost_d
        evaluation_function = cost_eval
    else:
        return

    valid_options = ["0", "1", "2", "q"]
    user_input = input("Select a routing algorithm: \n[0] Shortest Path\n[1] Extra Loops\n[2] Random Routing\nChoice: ")
    while user_input not in valid_options:
        user_input = input(
            "Invalid selection :(\nSelect a routing algorithm: \n[0] Shortest Path\n[1] Extra Loops\n[2] Random Routing\nChoice: ")

    if user_input == "0":
        shortest_path(source, target, amount, all_nodes, channel_balances, distance_function, evaluation_function)
    elif user_input == "1":
        extra_loops(source, target, amount, all_nodes, channel_balances, distance_function, evaluation_function)
    elif user_input == "2":
        random_routing(source, target, amount, all_nodes, channel_balances, valid_ids, distance_function,
                       evaluation_function)
    else:
        return


def main():
    user_input = ""
    all_nodes = load("all_nodes.pkl")
    all_channels = load("all_channels.pkl")
    channel_balances = load("channel_balances.pkl")
    disconnected_keys = load("disconnected_keys.pkl")

    options = ["0", "1", "2", "3", "4"]
    while user_input != "q":
        print("Options... [enter q to quit]")
        print("[0] Reload live data (this will take a while)")
        print("[1] Randomize channel balances")
        print("[2] Collect data to compare algorithms")
        print("[3] Plot existing data")
        print("[4] Route a transaction")
        user_input = input("Please select an option: ")
        if user_input in options:
            if user_input == "0":
                all_nodes, all_channels = reload_live_data()
            elif user_input == "1":
                channel_balances, disconnected_keys = randomize_channel_balances(all_nodes, all_channels)
            elif user_input == "2":
                collect_data_to_compare_algorithms(all_nodes, channel_balances, disconnected_keys)
            elif user_input == "3":
                plot_existing_data()
            elif user_input == "4":
                route_transaction(all_nodes, channel_balances, disconnected_keys)


if __name__ == "__main__":
    main()

