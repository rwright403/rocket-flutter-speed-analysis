import subprocess
import os

def debug_dir(path):
    print(f"\n🔍 Listing contents of: {path}")
    if os.path.exists(path):
        for item in os.listdir(path):
            print("  -", item)
    else:
        print("  ❌ Path does not exist!")

def run_machline(input_file_path):

    result = subprocess.run(
        ["./ext/MachLine/machline.exe", input_file_path], # This is the command to execute machline from the project directory
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

#TODO: COMMENT OUT AFTER DEBUGGING
    print("Successfully ran MachLine.")
        
    return result.stdout
