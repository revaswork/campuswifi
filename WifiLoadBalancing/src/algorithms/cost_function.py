import math

# -----------------------------
# Tunable weight parameters
# -----------------------------
WEIGHTS = {
    "distance": 1.0,
    "signal_penalty": 1.5,
    "airtime_usage": 2.0,
    "sticky_penalty": 5.0,
    "interference": 3.0,
    "switching_cost": 1.0
}

# RSSI threshold to detect sticky clients
RSSI_THRESHOLD = -75  # if RSSI < -75, client is sticky


# -----------------------------
# Helper functions
# -----------------------------
def euclidean_distance(user, ap):
    return math.dist((user["x"], user["y"]), (ap["x"], ap["y"]))


def signal_penalty(RSSI):
    """Convert RSSI into a positive penalty (worse signal = larger penalty)."""
    # Normal RSSI range: -40 (best) to -90 (worst)
    # Convert to positive cost
    return max(0, (-RSSI - 40) / 10)


def sticky_client_penalty(RSSI):
    """Penalty for sticky clients (low RSSI)."""
    if RSSI < RSSI_THRESHOLD:
        return 1  # will be multiplied by sticky weight
    return 0


def interference_penalty(ap):
    """AP interference score 0–1."""
    return ap.get("interference_score", 0.0)


# -----------------------------
# MAIN COST COMPUTATION
# -----------------------------
def compute_cost(user, ap):
    """
    Compute total cost for assigning a user to a specific AP.
    Lower cost = more likely MCMF will pick that AP.
    """

    # 1. Distance component
    dist = euclidean_distance(user, ap)

    # 2. Signal strength penalty
    sig_pen = signal_penalty(user["RSSI"])

    # 3. Airtime consumption cost
    air_pen = user["airtime_usage"]

    # 4. Sticky client penalty
    sticky_pen = sticky_client_penalty(user["RSSI"])

    # 5. Interference penalty (AP-level)
    inter_pen = interference_penalty(ap)

    # 6. Optional switching cost (for dynamic phase)
    switching_cost = 0  # can be updated later during greedy rebalancing

    # -----------------------------
    # Weighted Sum of Costs
    # -----------------------------
    total_cost = (
        WEIGHTS["distance"] * dist +
        WEIGHTS["signal_penalty"] * sig_pen +
        WEIGHTS["airtime_usage"] * air_pen +
        WEIGHTS["sticky_penalty"] * sticky_pen +
        WEIGHTS["interference"] * inter_pen +
        WEIGHTS["switching_cost"] * switching_cost
    )

    return round(total_cost, 3)


# -----------------------------
# Debugging test
# -----------------------------
if __name__ == "__main__":
    # Fake sample data
    user = {"x": 10, "y": 10, "RSSI": -78, "airtime_usage": 3}
    ap = {"x": 15, "y": 15, "interference_score": 0.4}

    print("Cost:", compute_cost(user, ap))
