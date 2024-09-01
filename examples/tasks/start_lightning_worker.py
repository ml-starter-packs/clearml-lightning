import os

import requests

from lightning_sdk import Studio, Machine
from clearml import Task, TaskTypes

task = Task.init(
    project_name="lightning-services",
    task_name="start-lightning-worker",
    continue_last_task=False,
    task_type=TaskTypes.service,
)

params = task.connect(
    {
        "machine": "CPU_SMALL",
        "containers_per_machine": 1,
    }
)
machine_type = params.get("machine")
machine = getattr(Machine, machine_type)

num_containers = params["containers_per_machine"]

# start studio
s = Studio("clearml-opensource-worker")
# s.start()

# use the jobs plugin
jobs_plugin = s.installed_plugins["jobs"]

cmd = f"cd agent && ./generate-compose.sh {num_containers} && make up && make connect"
jobs_plugin.run(cmd, name="test-launch", machine=machine)
