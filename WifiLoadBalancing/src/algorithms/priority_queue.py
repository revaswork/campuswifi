import heapq

class UserPriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, user, priority):
        """
        user: dict with user info
        priority: lower number => higher priority
        """
        heapq.heappush(self.heap, (priority, user))

    def pop(self):
        """Return the highest priority user"""
        if self.heap:
            return heapq.heappop(self.heap)[1]
        return None

    def __len__(self):
        return len(self.heap)

    def clear(self):
        self.heap = []
