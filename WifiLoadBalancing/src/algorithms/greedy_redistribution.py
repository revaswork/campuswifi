import math
from algorithms.priority_queue import UserPriorityQueue


class GreedyRedistributor:

    def __init__(self, aps, clients):
        self.aps = aps
        self.clients = clients

    # --------------------------------------------------------
    # Step 1: Detect overloaded APs
    # --------------------------------------------------------
    def get_overloaded_aps(self):
        overloaded = []
        for ap in self.aps:
            if ap["load"] > ap["airtime_capacity"]:
                overloaded.append(ap)
        return overloaded

    # --------------------------------------------------------
    # Step 2: Build Priority Queue of users to remove
    # --------------------------------------------------------
    def build_priority_queue(self, ap):
        pq = UserPriorityQueue()

        for user in self.clients:
            if user.get("nearest_ap") == ap["id"]:
                # Priority: weakest RSSI gets removed first
                priority = abs(user["RSSI"])  # weaker = higher priority
                pq.push(user, priority)

        return pq

    # --------------------------------------------------------
    # Step 3: Find alternative AP for a single user
    # --------------------------------------------------------
    def find_alternative_ap(self, user):
        best_ap = None
        best_cost = float("inf")

        for ap in self.aps:
            if ap["id"] == user.get("nearest_ap"):
                continue  # skip current AP

            # AP must have capacity
            if ap["load"] >= ap["airtime_capacity"]:
                continue

            # compute distance
            dist = math.dist((user["x"], user["y"]), (ap["x"], ap["y"]))

            if dist < best_cost:
                best_cost = dist
                best_ap = ap

        return best_ap

    # --------------------------------------------------------
    # Step 4: Apply Greedy Redistribution
    # --------------------------------------------------------
    def redistribute(self):
        overloaded_aps = self.get_overloaded_aps()

        for ap in overloaded_aps:
            pq = self.build_priority_queue(ap)

            while len(pq) > 0 and ap["load"] > ap["airtime_capacity"]:
                user = pq.pop()
                new_ap = self.find_alternative_ap(user)

                if new_ap:
                    # Move user
                    user["nearest_ap"] = new_ap["id"]
                    ap["load"] -= user.get("airtime_usage", 1)
                    new_ap["load"] += user.get("airtime_usage", 1)
                else:
                    # No AP available
                    break
