from typing import Any, Dict

from clearml import Task
from clearml.automation import PipelineController

from clearml_pipe_utils import deserialize_dict


def do_something(task_num):
    print(f"task_num: {task_num}")
    return task_num


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


def demo_parameter_updates(pipe, key: str = "Args") -> PipelineController:
    print("______DEFAULT PIPELINE PARAMS_____")
    default_params = pipe.get_parameters()
    print(default_params)  # notice this ignores UI-based updates
    print("______DYNAMIC PARAMS_____")
    dynamic_params = pipe._task.get_parameters_as_dict().get(key)
    print(dynamic_params)


def get_pipeline_params(
    pipe: PipelineController, key: str = "Args"
) -> PipelineController:
    # the following returns pipe._pipeline_args -> not updated.
    default_params = pipe.get_parameters()
    dynamic_params = pipe._task.get_parameters_as_dict().get(key, default_params)
    return deserialize_dict(dynamic_params)


def set_default_pipe_params(
    pipe: PipelineController, project_name: str = "scale-tests"
) -> PipelineController:
    task_name = "test-function-steps"
    execution_queue = "default"
    num_tasks = 4  # not having an impact in UI
    pipe.add_parameter(name="num_tasks", default=num_tasks)
    pipe.add_parameter(name="execution_queue", default=execution_queue)
    pipe.add_parameter(name="function_step_project", default=project_name)
    pipe.add_parameter(name="task_name", default=task_name)

    # this works as far as dynamic pipelines go, but not via UI.
    # params = pipe.connect_configuration(
    #     {
    #         "num_tasks": num_tasks,
    #         "execution_queue": execution_queue,
    #         "project": project_name,
    #         "task_name": task_name,
    #     }
    # )

    return pipe


def add_steps(pipe: PipelineController, params: Dict[str, Any]) -> PipelineController:

    for idx in range(params["num_tasks"]):
        pipe.add_function_step(
            name=f"task-{idx}",
            project_name=params["function_step_project"],
            function=do_something,
            function_kwargs={"task_num": idx},
            function_return=["output_value"],
            execution_queue=params["execution_queue"],
            cache_executed_step=True,
        )

    inputs = (
        "("
        + ",".join([f"${{task-{idx}.id}}" for idx in range(params["num_tasks"])])
        + ")"
    )

    pipe.add_function_step(
        name="collection",
        function=sum_all,
        project_name=params["function_step_project"],
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

    return pipe


if __name__ == "__main__":

    pipe = PipelineController(
        name="dynamic-pipeline",
        project="scale-tests",
        version="0.0.1",
        add_pipeline_tags=True,
    )

    pipe = set_default_pipe_params(pipe)
    demo_parameter_updates(pipe, key="Args")
    params = get_pipeline_params(pipe, key="Args")
    pipe = add_steps(pipe, params)

    pipe.start(queue="default")
    # pipe.start_locally()
    print("Done.")
