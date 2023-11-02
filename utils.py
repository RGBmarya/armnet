from collections import deque
import heapq

# replace with heap implementationa

class Module():
    id = 1
    def __init__(self, color, active=True) -> None:
        self.id = Module.id
        self.active = active
        self.queue = [] # [step, color]
        
        heapq.heapify(self.queue)
        Module.id += 1
    
    def get_id(self):
        return self.id
    
    def is_active(self) -> bool:
        return self.active

    def set_active(self, is_active) -> None:
        self.active = is_active

    def add_task(self, task: list) -> None:
        heapq.heappush(self.queue, task)

    # Decrement all actions in queue
    def step(self) -> None:
        for task in self.queue:
            task[0] -= 1

    # Execute action for all tasks with step 0
    def execute_all(self) -> None:
        while self.queue and self.queue[0][0] == 0:
            self.execute(self.queue[0])
            heapq.heappop(self.queue)
        
    # Execute single task
    def execute(self, task: list) -> None:
        step, color = task
        print(f"Module {self.id} pushed {color} block into bin") # Replace with actual servo action

if __name__ == "__main__":
    m = Module("red")

    m.add_task([1, "Red"])
    m.add_task([2, "Blue"])
    m.add_task([1, "Yellow"])
    m.add_task([3, "Green"])
    
    while (m.queue):
        print(m.queue)
        m.execute_all()
        m.step()