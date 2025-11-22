import networkx as nx
import math
import json
from .cost_function import compute_cost


class GraphModel:

    def __init__(self, users, aps):
        self.users = users
        self.aps = aps
        self.graph = nx.DiGraph()

    def build_flow_network(self):
        """Build the bipartite flow network: S -> Users -> APs -> T"""

        G = self.graph

        # Add special nodes
        G.add_node("S")  # Source
        G.add_node("T")  # Sink

        # -------------------------
        # Add User nodes and edges
        # -------------------------
        for user in self.users:
            uid = user["id"]

            # Edge: S -> User
            G.add_edge("S", uid, capacity=1, weight=0)

            # Connect user to all APs
            for ap in self.aps:
                aid = ap["id"]

                # Compute cost using cost function
                cost = compute_cost(user, ap)

                # Add edge User -> AP
                G.add_edge(uid, aid, capacity=1, weight=cost)

        # -------------------------
        # Add AP nodes and edges
        # -------------------------
        for ap in self.aps:
            aid = ap["id"]

            # AP → T edge based on airtime or client capacity
            G.add_edge(aid, "T", capacity=ap["airtime_capacity"], weight=0)

        return G


def load_json(filename):
    with open(filename, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    # Test the graph model
    users = load_json("WifiLoadBalancing/data/users.json")
    aps = load_json("WifiLoadBalancing/data/aps.json")

    gm = GraphModel(users, aps)
    G = gm.build_flow_network()

    print("Graph created with:")
    print("Nodes:", len(G.nodes))
    print("Edges:", len(G.edges))
