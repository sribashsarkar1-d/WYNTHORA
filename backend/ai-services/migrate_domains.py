import os
import shutil
import glob

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "app"))
algorithms_dir = os.path.join(base_dir, "algorithms")

# Mapping of old paths to new paths
# We will move directories completely to preserve relative imports inside them
mapping = {
    "system_dynamics": "domains/economy/system_dynamics",
    "gnn": "domains/politics/gnn",
    "abm": "domains/population/abm",
    "finance": "domains/economy/finance",
    "health": "domains/health/models",
    "rl": "domains/military/rl",
    "crypto": "infrastructure/crypto",
    "events": "simulation/events",
    "models": "ai/models",
    "nlp": "ai/nlp",
}

# 1. Move directories
for old_name, new_rel_path in mapping.items():
    old_path = os.path.join(algorithms_dir, old_name)
    new_path = os.path.join(base_dir, new_rel_path)
    
    if os.path.exists(old_path):
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        print(f"Moving {old_path} to {new_path}")
        try:
            shutil.move(old_path, new_path)
        except Exception as e:
            print(f"Failed to move {old_path}: {e}")
            
# 2. Also move master_simulation.py and data_loader.py
master_sim_old = os.path.join(algorithms_dir, "master_simulation.py")
if os.path.exists(master_sim_old):
    shutil.move(master_sim_old, os.path.join(base_dir, "simulation/engine/master_simulation.py"))

data_loader_old = os.path.join(algorithms_dir, "data_loader.py")
if os.path.exists(data_loader_old):
    shutil.move(data_loader_old, os.path.join(base_dir, "infrastructure/external_apis/data_loader.py"))

# 3. Search and replace import paths in all Python files
import_replacements = {
    "app.algorithms.system_dynamics": "app.domains.economy.system_dynamics",
    "app.algorithms.gnn": "app.domains.politics.gnn",
    "app.algorithms.abm": "app.domains.population.abm",
    "app.algorithms.finance": "app.domains.economy.finance",
    "app.algorithms.health": "app.domains.health.models",
    "app.algorithms.rl": "app.domains.military.rl",
    "app.algorithms.crypto": "app.infrastructure.crypto",
    "app.algorithms.events": "app.simulation.events",
    "app.algorithms.models": "app.ai.models",
    "app.algorithms.nlp": "app.ai.nlp",
    "app.algorithms.data_loader": "app.infrastructure.external_apis.data_loader",
}

py_files = glob.glob(os.path.join(base_dir, "**", "*.py"), recursive=True)

for file_path in py_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    original_content = content
    for old_import, new_import in import_replacements.items():
        content = content.replace(old_import, new_import)
        
    if content != original_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated imports in {file_path}")

print("Migration complete.")
