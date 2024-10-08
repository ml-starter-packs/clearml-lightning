"""A Pipeline of Pipelines!"""

import json

from clearml import PipelineController


def main():
    pipe = PipelineController(
        name="meta-pipe", project="dev/tests", add_pipeline_tags=True
    )
    pipe._task.set_repo(
        repo="https://github.com/ml-starter-packs/clearml-lightning.git"
    )

    pipe.add_parameter(
        name="num_copies",
        default=[5, 6],
    )
    pipe.add_parameter(
        name="features",
        default=[["a", "b"], ["c", "d", "e"]],
    )
    pipe.add_parameter(
        name="task_queue",
        default="scale",
    )

    default_params = pipe.get_parameters()
    dynamic_params = pipe._task.get_parameters_as_dict().get("Args", default_params)
    num_copies = dynamic_params.get("num_copies")
    features = dynamic_params.get("features")
    task_queue = dynamic_params.get("task_queue")

    # this should grab the most recently executed one:
    SOURCE_TASK = PipelineController.get(
        pipeline_project="dev/tests", pipeline_name="dynamic-test"
    )
    print(f"source pipeline: {SOURCE_TASK}")

    if not isinstance(num_copies, list):
        num_copies = num_copies.replace("[", "").replace("]", "").split(",")
    if not isinstance(features, list):  # an alternative approach
        features = json.loads(features)
        assert isinstance(features[0], list), "expecting list of lists"

    for idx in range(len(num_copies)):
        nc, fl = num_copies[idx], features[idx]
        pipe.add_step(
            name=f"P{idx:03d}",
            base_task_id=SOURCE_TASK.id,
            parameter_override={
                "Args/num_copies": nc,
                "Args/feature_list": fl,
                "Args/task_queue": task_queue,
            },
            execution_queue="services",
        )

    pipe.start(queue="services")


if __name__ == "__main__":
    main()
