import subprocess
import sys
import os

# Replace 'target_script.py' with the name of the Python script you want to open
script_to_open = "main.py"

try:
    # Get the path to the Python interpreter
    python_interpreter = sys.executable
    
    # Check if the script exists
    if not os.path.exists(script_to_open):
        raise FileNotFoundError(f"The '{script_to_open}' file was not found.")
    
    # Run the target script in the background without showing the command prompt
    subprocess.Popen(
        [python_interpreter, script_to_open],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
except FileNotFoundError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"An error occurred: {str(e)}")

