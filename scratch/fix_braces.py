import os

file_path = "/Users/andreasmuller/experiments/cernsim/CERN_Visualisierung/scripts/create_notebook.py"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.read().split("\n")

# Find the specific block to replace
start_idx = -1
for idx, line in enumerate(lines):
    if "trSteps.forEach(s=>s.classList.remove(\"cur\",\"cur-i\",\"done\"));" in line:
        start_idx = idx
        break

if start_idx != -1:
    print(f"Found line at index: {start_idx}")
    # Let's check lines[start_idx+1] and lines[start_idx+2]
    print(f"Line + 1: '{lines[start_idx+1]}'")
    print(f"Line + 2: '{lines[start_idx+2]}'")
    
    # We want to replace lines[start_idx+1] and lines[start_idx+2] with a single "}"
    if lines[start_idx+1].strip() == "}" and lines[start_idx+2].strip() == "}":
        print("Confirmed duplicate closing braces!")
        # Replace the next two lines with a single closing brace
        lines[start_idx+1] = "}"
        # Delete lines[start_idx+2]
        lines.pop(start_idx+2)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print("Successfully removed the extra closing brace and saved the file!")
    else:
        print("Spacing or structure did not match duplicate braces!")
else:
    print("Could not find the target code line!")
