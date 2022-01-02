import sys
import os

folder = sys.argv[1] if len(sys.argv) > 1 else ""

if not folder:
    print("Directory is not specified")
else:
    for root, folders, files in os.walk(folder):
        for file in files:
            print(os.path.join(root, file))
