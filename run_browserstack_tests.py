# run_browserstack_tests.py
import json
import subprocess
import os

# Load configurations
with open('browserstack_configs.json', 'r') as f:
    config = json.load(f)

# Run tests on each configuration
for env in config['environments']:
    print(f"Running tests on {env['name']}...")
    
    cmd = ["pytest", "tests/ui_tests/", "-v", "--use_browserstack"]
    
    # Add environment parameters
    for key, value in env.items():
        if key != 'name':
            if isinstance(value, bool):
                if value:
                    cmd.append(f"--{key}")
            else:
                cmd.append(f"--{key}")
                cmd.append(str(value))
    
    # Run the tests
    subprocess.run(cmd)