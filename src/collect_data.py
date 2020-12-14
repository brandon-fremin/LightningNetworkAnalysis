import multiprocessing as mp
from src.helper import load, save
from src.create_node import create_node


def processor(index, nodes_to_process):
    COUNTER_MAX = 10
    counter = 1
    nodes_map = load(f"nodes_map_processor_{index}.pkl")
    keys_to_process = set(nodes_to_process.keys())
    existing_keys = set(nodes_map.keys())
    keys_to_search = frozenset(keys_to_process - existing_keys)
    for key in keys_to_search:
        node = nodes_to_process[key]
        nodes_map[node["id"]] = create_node(node)
        if counter % COUNTER_MAX == 0:
            save(nodes_map, f"nodes_map_processor_{index}.pkl")
            print(f"Processor {index} Saved Current Map ({counter}/{len(keys_to_search)})...")
        counter = counter + 1
    save(nodes_map, f"nodes_map_processor_{index}.pkl")
    print(f"Processor {index} Finished!")


def collect_data():
    num_cpu = mp.cpu_count()
    print(num_cpu)
    pool = mp.Pool(num_cpu)

    active_nodes = load("nodes.pkl", 'https://explorer.acinq.co/nodes', True)
    active_keys = [node["id"] for node in active_nodes]
    node_map = {}
    for i in range(len(active_keys)):
        node_map[active_keys[i]] = active_nodes[i]

    num_keys = len(active_keys)
    for i in range(num_cpu):
        cpu_keys = active_keys[num_keys * i // num_cpu: num_keys * (i + 1) // num_cpu]
        cpu_nodes = {}
        for key in cpu_keys:
            cpu_nodes[key] = node_map[key]
        print(f"Processor {i} started with keys {num_keys * i // num_cpu} - {num_keys * (i + 1) // num_cpu - 1}")
        pool.apply_async(processor, args=(i, cpu_nodes))

    pool.close()
    pool.join()  # We don't pass this line until all pools are done


def meld_sets(found, listed, string="nodes"):
    found = set(found)
    listed = set(listed)
    if found.issubset(listed) and listed.issubset(found):
        print(f"All {string} listed were found!")
        return frozenset(found.intersection(listed))

    listed_found = list(listed - found)
    listed_found.sort()
    print(f"Couldn't locate the following {string} [{len(listed_found)}]:")
    print(listed_found)

    found_listed = list(found - listed)
    found_listed.sort()
    print(f"Found the following {string} but they weren't listed [{len(found_listed)}]:")
    print(found_listed)
    return frozenset(found.intersection(listed))


def merge_collected_data():
    num_cpu = mp.cpu_count()
    node_maps = {}
    for i in range(num_cpu):
        node_maps[i] = load(f"nodes_map_processor_{i}.pkl")

    all_nodes = {}
    all_keys = set([])
    for i in range(num_cpu):
        for key in node_maps[i].keys():
            assert key not in all_keys
            all_nodes[key] = node_maps[i][key]
            all_keys.add(key)

    active_nodes = load("nodes.pkl", 'https://explorer.acinq.co/nodes', False)
    active_node_keys = set([n["id"] for n in active_nodes])

    loaded_node_keys = meld_sets(all_keys, active_node_keys, "nodes")
    for key in (set(all_nodes.keys()) - loaded_node_keys):
        del all_nodes[key]

    active_channels = load("channels.pkl", 'https://explorer.acinq.co/channels', True)
    active_channel_ids = frozenset([c["id"] for c in active_channels])  # Get list of active lightning network channels

    all_channels = {}
    collision_map = {}  # We should have collisions because there is an edge in both directions
    for key, node in all_nodes.items():
        for edge in node["edges"]:
            channel_id = edge["short_channel_id"]

            # skip channel ids which aren't active
            if channel_id not in active_channel_ids:
                continue

            # increment collision map
            if channel_id in all_channels.keys():
                try:
                    collision_map[channel_id] = collision_map[channel_id] + 1
                except:
                    collision_map[channel_id] = 1

            # store edge as valid channel
            all_channels[channel_id] = edge

    # There should be exactly two entries for each edge (forward, backward) so there is one collision
    for key, value in collision_map.items():
        assert value == 1

    # If the edge had no collision, then it's invalid because it's a one-way channel
    valid_active_channel_ids = meld_sets(collision_map.keys(), active_channel_ids, "channels")
    for key in (set(all_channels.keys()) - valid_active_channel_ids):
        del all_channels[key]

    return all_nodes, all_channels
