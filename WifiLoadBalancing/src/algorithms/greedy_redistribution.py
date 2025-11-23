import math
from algorithms.priority_queue import UserPriorityQueue


class GreedyRedistributor:

    def __init__(self, aps, clients):
        self.aps = aps
        self.clients = clients

        # fairness memory: avoid moving same user repeatedly
        self.move_history = {}  # user_id -> last_move_iteration
        self.cooldown_steps = 3  # prevents oscillation

        self.iteration = 0

    # --------------------------------------------------------
    # Step 1: Detect overloaded APs
    # --------------------------------------------------------
    def get_overloaded_aps(self):
        return [
            ap for ap in self.aps
            if ap["load"] > ap["airtime_capacity"]
        ]

    # --------------------------------------------------------
    # Step 2: Build Priority Queue using SMARTER criteria
    # --------------------------------------------------------
    def build_priority_queue(self, ap):
        pq = UserPriorityQueue()
        ap_id = ap["id"]

        for user in self.clients:

            if user.get("nearest_ap") != ap_id:
                continue

            # ------------- Smarter priority formula -------------
            # High priority = remove this user first
            # Priority factors:
            # - weaker RSSI (absolute)
            # - higher airtime usage
            # - has not been moved recently (fairness)
            # ----------------------------------------------------

            rssi_factor = abs(user.get("RSSI", -50))
            airtime = user.get("airtime_usage", 1)

            last_moved = self.move_history.get(user["id"], -100)
            cooldown_penalty = max(0, self.cooldown_steps - (self.iteration - last_moved))

            priority = (
                rssi_factor      * 0.6 +
                airtime          * 0.3 +
                cooldown_penalty * 3.0   # big penalty so we don't keep moving same user
            )

            pq.push(user, priority)

        return pq

    # --------------------------------------------------------
    # Step 3: Multi-factor alternative AP selection
    # --------------------------------------------------------
    def find_alternative_ap(self, user):
        best_ap = None
        best_score = float("inf")

        ux, uy = user["x"], user["y"]
        user_airtime = user.get("airtime_usage", 1)

        for ap in self.aps:

            if ap["id"] == user.get("nearest_ap"):
                continue

            # Must have AVAILABLE capacity
            if ap["load"] + user_airtime > ap["airtime_capacity"]:
                continue

            # Compute distance
            dist = math.dist((ux, uy), (ap["x"], ap["y"]))

            # Signal penalty (worse RSSI → worse score)
            # Estimate RSSI via inverse distance (simple model)
            signal_penalty = dist * 0.8

            # AP load penalty (prefer APs with more free space)
            load_penalty = (ap["load"] / ap["airtime_capacity"]) * 2.0

            # Stability factor (prefer stable APs)
            stability = ap.get("stability", 1.0)  # if not present, assume stable

            # Final score (lower = better)
            score = (
                dist             * 0.5 +
                signal_penalty   * 0.4 +
                load_penalty     * 1.2 -
                stability        * 0.3
            )

            if score < best_score:
                best_score = score
                best_ap = ap

        return best_ap

    # --------------------------------------------------------
    # Step 4: Apply Smarter Greedy Redistribution
    # --------------------------------------------------------
    def redistribute(self):
        self.iteration += 1

        overloaded_aps = self.get_overloaded_aps()

        for ap in overloaded_aps:

            pq = self.build_priority_queue(ap)

            # Loop: remove users until AP is not overloaded
            while len(pq) > 0 and ap["load"] > ap["airtime_capacity"]:

                user = pq.pop()
                if not user:
                    break

                # Fairness: avoid moving same user too often
                last_moved = self.move_history.get(user["id"], -100)
                if self.iteration - last_moved < self.cooldown_steps:
                    continue

                new_ap = self.find_alternative_ap(user)

                if new_ap:
                    # Perform the move
                    user_air = user.get("airtime_usage", 1)

                    ap["load"]      -= user_air
                    new_ap["load"]  += user_air

                    user["nearest_ap"] = new_ap["id"]
                    self.move_history[user["id"]] = self.iteration

                else:
                    # No AP available → break redistribution
                    break
