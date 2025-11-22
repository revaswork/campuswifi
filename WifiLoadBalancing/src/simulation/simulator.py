import random
import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parents[2] / "data"

class WifiSimulator:
    def __init__(self):
        # load initial aps + users from data/
        with open(DATA_DIR / "aps.json") as f:
            self.aps = json.load(f)

        with open(DATA_DIR / "users.json") as f:
            self.clients = json.load(f)

    def step(self):
        """Update AP loads + move users randomly."""

        # update AP loads
        for ap in self.aps:
            ap["load"] = max(0, min(100, ap["load"] + random.randint(-5, 5)))

        # move users randomly
        for user in self.clients:
            user["x"] = (user["x"] + random.randint(-3, 3)) % 200
            user["y"] = (user["y"] + random.randint(-3, 3)) % 200

    def get_state(self):
        """Return the state object expected by main.py"""
        return {
            "aps": self.aps,
            "clients": self.clients
        }








# import json
# import math
# import random
# from pathlib import Path

# DATA_DIR = Path(__file__).resolve().parents[2] / "data"


# class WifiSimulator:

#     # ===========================================================
#     # INITIALIZATION
#     # ===========================================================
#     def __init__(self):
#         # Load AP + User data
#         with open(DATA_DIR / "aps.json") as f:
#             self.aps = json.load(f)

#         with open(DATA_DIR / "users.json") as f:
#             self.clients = json.load(f)

#         # Algorithm assignment placeholder (Reva will fill)
#         self.assignments = {}  # { user_id: ap_id }

#         # Initialize AP load values
#         for ap in self.aps:
#             if "load" not in ap:
#                 ap["load"] = random.randint(20, 70)

#     # ===========================================================
#     # USER MOVEMENT (Niyati)
#     # ===========================================================
#     def move_users(self):
#         """Simple random movement inside the campus map."""
#         for user in self.clients:
#             user["x"] = (user["x"] + random.randint(-3, 3)) % 200
#             user["y"] = (user["y"] + random.randint(-3, 3)) % 200

#     # ===========================================================
#     # RSSI UPDATE (Niyati)
#     # ===========================================================
#     def calc_rssi(self, distance):
#         """Log-distance path-loss model."""
#         if distance <= 0:
#             return -30
#         rssi = -30 - 20 * math.log10(distance)
#         return max(-95, min(-40, rssi))

#     def update_rssi(self):
#         """Recalculate RSSI for each user based on nearest AP."""
#         for user in self.clients:
#             best_rssi = -95
#             best_ap = None

#             for ap in self.aps:
#                 dist = math.dist((user["x"], user["y"]), (ap["x"], ap["y"]))
#                 if dist <= ap["coverage_radius"]:
#                     rssi = self.calc_rssi(dist)
#                     if rssi > best_rssi:
#                         best_rssi = rssi
#                         best_ap = ap["id"]

#             user["RSSI"] = best_rssi
#             user["nearest_ap"] = best_ap  # useful for greedy algorithm

#     # ===========================================================
#     # AP LOAD UPDATE (Niyati)
#     # ===========================================================
#     def update_ap_load(self):
#         """Very basic load model for now."""
#         # Reset load
#         for ap in self.aps:
#             ap["load"] = 0

#         # Count users inside each AP's range
#         for user in self.clients:
#             if user["nearest_ap"] is None:
#                 continue

#             for ap in self.aps:
#                 if ap["id"] == user["nearest_ap"]:
#                     ap["load"] += user.get("airtime_usage", 1)

#     # ===========================================================
#     # MCMF (Reva will implement)
#     # ===========================================================
#     def apply_mcmf(self):
#         """
#         Run Minimum Cost Max Flow and update self.assignments
#         (Reva will fill this in)
#         """
#         pass

#     # ===========================================================
#     # GREEDY REDISTRIBUTION (Meet will implement)
#     # ===========================================================
#     def apply_greedy(self):
#         """
#         Detect overloaded APs and shift users using PQ
#         (Meet will fill this in)
#         """
#         pass

#     # ===========================================================
#     # MAIN STEP LOOP (Called by main.py)
#     # ===========================================================
#     def step(self):
#         """Run one simulation tick."""

#         # 1. Move users (Niyati)
#         self.move_users()

#         # 2. Update RSSI based on new positions (Niyati)
#         self.update_rssi()

#         # 3. Recalculate AP load (Niyati)
#         self.update_ap_load()

#         # 4. Run global optimization every few seconds (Reva)
#         # if self.tick % 5 == 0:
#         #     self.apply_mcmf()

#         # 5. Run local greedy balancing (Meet)
#         # self.apply_greedy()

#         # 6. Tick counter
#         # self.tick += 1

#     # ===========================================================
#     # RETURN STATE TO FRONTEND
#     # ===========================================================
#     def get_state(self):
#         """Return full state to WebSocket clients."""
#         return {
#             "aps": self.aps,
#             "clients": self.clients,
#             "assignments": self.assignments  # algorithm results
#         }
