"""Script that clones a pipeline and runs it for a set of inputs."""

from clearml import PipelineController, Task

list_of_experiments = [
    ["a", "b"],
    ["c", "d"],
    ["e", "f"],
]

list_num_copies = [1, 2, 3]

source_task = PipelineController.get(
    pipeline_project="dev/tests", pipeline_name="dynamic-test #1"
)
print(f"Source task: {source_task.id}")

for idx in range(3):
    num_copies = list_num_copies[idx]
    feature_list = list_of_experiments[idx]
    task = Task.clone(source_task=source_task.id)
    task.set_name(f"dynamic21.{idx}")
    task.set_parameter("Args/feature_list", feature_list)
    task.set_parameter("Args/num_copies", num_copies)
    Task.enqueue(task, queue_name="default")
