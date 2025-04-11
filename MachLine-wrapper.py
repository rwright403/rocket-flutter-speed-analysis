###NOTE: CHATGPT CODE be careful


import subprocess

def run_machline(input_file_path):
    result = subprocess.run(
        ["./external/machline/build/machline.exe", input_file_path],
        cwd="external/machline/build",  # or wherever the .exe lives
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        print("MachLine failed:", result.stderr)
    else:
        print("MachLine finished successfully.")
    return result.stdout
