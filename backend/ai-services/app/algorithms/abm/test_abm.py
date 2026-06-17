from world import WorldEnvironment
from agent import VirtualCitizen

def run_test():
    print("Initializing ABM Simulation World (10x10)...")
    world = WorldEnvironment(10, 10)
    
    print("Spawning 3 Virtual Citizens...")
    for i in range(3):
        agent = VirtualCitizen(agent_id=i, x=5, y=5, world=world)
        world.add_agent(agent)
        
    print("\n--- Running 5 Simulation Ticks ---\n")
    for tick in range(1, 6):
        print(f"[Tick {tick}]")
        world.tick()
        print("-" * 30)
        
if __name__ == "__main__":
    run_test()
