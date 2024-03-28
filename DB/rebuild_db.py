import subprocess
import os

# Get the current working directory
current_directory = os.getcwd()

# Define the relative path to your script
relative_path = 'DB/drop_db.py'
# Construct the full path
full_path = os.path.join(current_directory, relative_path)

# Run the script using subprocess
subprocess.run(['python3', full_path])

relative_path = 'DB/create_db.py'
full_path = os.path.join(current_directory, relative_path)
subprocess.run(['python3', full_path])

relative_path = 'DB/migrations.py'
full_path = os.path.join(current_directory, relative_path)
subprocess.run(['python3', full_path])

relative_path = 'DB/seed_db.py'
full_path = os.path.join(current_directory, relative_path)
subprocess.run(['python3', full_path])