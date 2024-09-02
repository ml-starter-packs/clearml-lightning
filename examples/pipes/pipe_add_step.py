"""A dynamic Pipeline that passes UI args to task params + config"""

import json
from typing import Any, Dict

from clearml import PipelineController


def init_params(pipe: PipelineController) -> PipelineController:
    pipe.add_parameter(
        name="num_copies",
        default=1,
        description="number of copies of the task",
        param_type="int",
    )

    # type hints such as 'int' or 'str' seem to work, but "list" ones do not.
    pipe.add_parameter(
        name="feature_list",
        default=["default", "pipe", "feature", "list"],
        description="feature list to be passed to task",
        param_type="List[str]",
    )

    pipe.add_parameter(
        name="task_queue",
        default="default",
        description="execution queue for the tasks",
        param_type="str",
    )
    return pipe


def add_steps(
    pipe: PipelineController, params: Dict[str, str], default_params: Dict[str, Any]
) -> PipelineController:

    # must handle both typed-defaults and strings
    # also entirely up to you to handle user error here...
    num_copies = int(params.get("num_copies", default_params.get("num_copies")))
    if num_copies <= 0:
        raise ValueError("`num_copies` mmust be a positive integer")

    feature_list = params.get("feature_list")
    execution_queue = params.get("task_queue", "default")
    if feature_list is None:
        feature_list = default_params.get("feature_list")
    else:
        feature_list = json.loads(feature_list)
    if not isinstance(feature_list, list):
        raise ValueError("`feature_list` must be a list of strings")

    for i in range(num_copies):
        pipe.add_step(
            name=f"T{i:04d}",
            base_task_name="demo-task",
            base_task_project="dev/tests",
            parameter_override={
                "ShapeParameters/N": 200 + i,
            },
            configuration_overrides={
                "feature_list": json.dumps(
                    feature_list
                ),  # must be string (to deserialize later)
                "feature_dict": {"feature_10": False},  # this is now the new value.
            },
            execution_queue=execution_queue,
        )
    return pipe


if __name__ == "__main__":
    pipe = PipelineController(
        name="dynamic-test",
        project="dev/tests",
        version=None,
        add_pipeline_tags=True,
        always_create_from_code=True,
    )
    pipe._task.set_repo(
        repo="https://github.com/ml-starter-packs/clearml-lightning.git"
    )

    # TODO: get these to be dynamic?
    tag_list = ["tag-a", "tag-b"]
    pipe.add_tags(tag_list)

    pipe = init_params(pipe)

    # notice this does not "see" UI changes
    # Note: may be related to always_create_from_code
    default_params = pipe.get_parameters()

    print("______DEFAULT PIPELINE PARAMS_____")
    print(default_params)
    # Note: Should I just use argparse for all of these?

    print("______DYNAMIC PARAMS_____")
    dynamic_params = pipe._task.get_parameters_as_dict().get("Args", {})
    # these parameters will have UI-based updates, but are strings!
    # so it is up to you to deserialize them appropriately.
    print(dynamic_params)

    # print("processing serialized keys from pipeline task arguments")
    # dynamic_params = deserialize_dict(dynamic_params)
    # assert dynamic_params, "Cannot be empty"
    # print(dynamic_params)

    pipe = add_steps(pipe, dynamic_params, default_params)

    logger = pipe.get_logger()
    logger.report_scalar("title", "series", value=1, iteration=0)
    pipe.start(queue="services")
