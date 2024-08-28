"""A Pipeline of Pipelines!"""

import json

from clearml import PipelineController

source_task = PipelineController.get(pipeline_project="dev/tests", pipeline_name="dynamic-test #21")
pipe = PipelineController(name="meta-pipe", project="dev/tests", add_pipeline_tags=True)

pipe.add_parameter(
    name="num_copies",
    default=[1],
)
pipe.add_parameter(
    name="features",
    default=[["a", "b"]],
)

default_params = pipe.get_parameters()
dynamic_params = pipe._task.get_parameters_as_dict().get("Args", default_params)
num_copies = dynamic_params.get("num_copies")
features = dynamic_params.get("features")

if not isinstance(num_copies, list):
    num_copies = num_copies.replace("[", "").replace("]", "").split(",")
if not isinstance(features, list):  # an alternative approach
    features = json.loads(features)
    assert isinstance(features[0], list), "expecting list of lists"

for idx in range(len(num_copies)):
    nc, fl = num_copies[idx], features[idx]
    pipe.add_step(
        name=f"P{idx:03d}",
        base_task_id=source_task.id,
        parameter_override={
            "Args/num_copies": nc,
            "Args/feature_list": fl,
        },
        execution_queue="default",
    )
pipe.start(queue="default")
