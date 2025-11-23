import heapq

class UserPriorityQueue:
    def __init__(self):
        self.heap = []
        self.counter = 0  # tie-breaker to avoid comparing dicts

    def push(self, user, priority):
        # lower priority number = higher removal priority
        entry = (priority, self.counter, user)
        heapq.heappush(self.heap, entry)
        self.counter += 1

    def pop(self):
        if self.heap:
            return heapq.heappop(self.heap)[2]
        return None

    def __len__(self):
        return len(self.heap)

    def clear(self):
        self.heap = []
        self.counter = 0
