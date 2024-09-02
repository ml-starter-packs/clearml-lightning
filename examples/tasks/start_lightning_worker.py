import os
import time

import requests

from lightning_sdk import Studio, Machine, JobsPlugin, Job
from clearml import Task, TaskTypes

LIGHTNING_ENV = f"""
-e LIGHTNING_USER_ID={os.environ.get("LIGHTNING_USER_ID")} \
-e LIGHTNING_API_KEY={os.environ.get("LIGHTNING_API_KEY")} \
-e LIGHTNING_USERNAME={os.environ.get("LIGHTNING_USERNAME")} \
-e LIGHTNING_TEAMSPACE={os.environ.get("LIGHTNING_TEAMSPACE")} \
-e LIGHTNING_CLUSTER_ID={os.environ.get("LIGHTNING_CLUSTER_ID")} \
-e LIGHTNING_ORG={os.environ.get("LIGHTNING_ORG")}
"""

task = Task.init(
    project_name="lightning-services",
    task_name="start-lightning-worker",
    continue_last_task=False,
    task_type=TaskTypes.service,
)
task.set_repo(repo="https://github.com/ml-starter-packs/clearml-lightning.git")
task.set_base_docker(
    docker_image="python:3.10.10",
    docker_arguments=LIGHTNING_ENV,
)
params = task.connect(
    {
        "machine": "CPU_SMALL",
        "containers_per_machine": 1,
        "job_name": "test-launch-remote",
    }
)
task.execute_remotely(queue_name="services")

machine_type = params.get("machine")
job_name = params.get("job_name", "default-job-name")

machine = getattr(Machine, machine_type)

num_containers = params["containers_per_machine"]

# start studio
s = Studio("worker-clearml-opensource")
# s.start()

# use the jobs plugin
# jobs_plugin = s.installed_plugins["jobs"]
jobs_plugin = JobsPlugin("jobs", "", s)

cmd = f"cd agent && ./generate-compose.sh {num_containers} && make up && make connect"
launched_job = jobs_plugin.run(cmd, name=job_name, machine=machine)
# job_name = jobs_plugin.run(cmd, machine=machine)

print(f"Launched job name: {launched_job.name}")

print("Entering infinite execution loop")


def kill_job():
    print("Stopping job")
    j = Job(launched_job.name, s.teamspace)
    j.stop()
    print("Job stopped")


task.register_abort_callback(kill_job, 30)

while True:
    time.sleep(10)
