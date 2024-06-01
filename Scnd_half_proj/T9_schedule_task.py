# T9_schedule_task.py

import subprocess

def create_tasks():
    task_names = ["Task1", "Task2", "Task3"]
    executable_path = r"dist\main_script.exe"
    start_times = ["14:05", "14:07", "14:10"]  # Adjust start times as needed

    for task_name, start_time in zip(task_names, start_times):
        # Command to create a new scheduled task
        command = f"schtasks /create /tn {task_name} /tr {executable_path} /sc once /st {start_time}"

        # Execute the command
        subprocess.run(command, shell=True)

if __name__ == "__main__":
    create_tasks()
