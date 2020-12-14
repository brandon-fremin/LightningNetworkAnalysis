import requests


class Node:
    def __init__(self, ln_node):
        self.node = {
            "id": None,
            "alias": None,
            "ip": None,
            "geo": None,
            "edges": []
        }

        fields = ["id", "alias", "ip", "geo"]
        for field in fields:
            try:
                self.node[field] = ln_node[field]
            except:
                pass

    def get_edges(self):
        req = f'https://ln.bigsun.xyz/api/rpc/node_channels?nodepubkey={self.node["id"]}'
        edges = requests.get(req).json()
        for e in edges:
            try:
                float(e["inpol"]["base"])
                float(e["outpol"]["base"])
            except:
                continue
            self.node["edges"].append(create_edge(e))

    def json(self):
        return self.node


def create_edge(e):
    edge = {
        "short_channel_id": None,
        "peer_id": None,
        "satoshis": None,
        "inpol": None,
        "outpol": None
    }

    fields = ["short_channel_id", "satoshis", "inpol", "outpol"]
    for field in fields:
        try:
            edge[field] = e[field]
        except:
            pass

    try:
        edge["peer_id"] = e["peer"]["id"]
    except:
        pass

    return edge


def create_node(ln_node):
    node = Node(ln_node)
    node.get_edges()
    return node.json()
