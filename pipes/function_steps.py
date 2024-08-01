from clearml.automation import PipelineController

from clearml import Task


def do_something(task_num):
    print(f"task_num: {task_num}")
    return task_num


for idx in range(params["num_tasks"]):
    pipe.add_function_step(
        name=f"task-{idx}",
        project_name=params["project"],
        function=do_something,
        function_kwargs={"task_num": idx},
        function_return=["output_value"],
        execution_queue=params["execution_queue"],
        cache_executed_step=True,
    )


def sum_all(inputs: str):
    print("SUMMING")
    print(inputs)
    # strip out leading and trailing characters (parenthesis, brackets)
    inputs = inputs[1:-1]
    task_ids = inputs.split(",")
    tasks = [Task.get_task(task_id=task_id) for task_id in task_ids]
    print(tasks[0].get_parameters())
    print(tasks[0].get_registered_artifacts())
    values = [task.get_parameters()["return/output_value"] for task in tasks]
    # need to cast them to float
    values = list(map(float, values))
    return sum(values)


if __name__ == "__main__":

    task_name = "test-function-steps"
    project_name = "scale-tests"
    execution_queue = "default"
    num_tasks = 4  # not having an impact in UI

    pipe = PipelineController(
        name=f"{project_name}-pipeline",
        project=project_name,
        version="0.0.1",
        add_pipeline_tags=False,
    )

    # doesn't seem to lead to interactive node creation: TODO: apply known fix.
    # pipe.add_parameter(name="num_tasks", default=num_tasks)
    # pipe.add_parameter(name="execution_queue", default=execution_queue)
    # pipe.add_parameter(name="project", default=project_name)
    # pipe.add_parameter(name="task_name", default=task_name)
    # params = pipe.get_parameters()

    params = pipe.connect_configuration(
        {
            "num_tasks": num_tasks,
            "execution_queue": execution_queue,
            "project": project_name,
            "task_name": task_name,
        }
    )

    inputs = (
        "("
        + ",".join([f"${{task-{idx}.id}}" for idx in range(params["num_tasks"])])
        + ")"
    )

    pipe.add_function_step(
        name="collection",
        function=sum_all,
        project_name=params["project"],
        function_kwargs={
            "inputs": inputs,
        },
        # function_kwargs={"inputs": "${task-0.output_value}"},  # individual strings work...
        # function_kwargs={  # this works for kwarg_sum_all
        #     f"input-{idx}": f"${{task-{idx}.output_value}}"
        #     for idx in range(params["num_tasks"])
        # },
        # parents=[f"task-{idx}" for idx in range(params["num_tasks"])],  # should be inferred.
        function_return=["sum_output_value"],
        execution_queue=params["execution_queue"],
    )

    # pipe.start()
    pipe.start_locally()
    print("Done.")
