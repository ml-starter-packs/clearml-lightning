import logging
from typing import Any, Dict, Optional, Union

from clearml import PipelineController, Task

from utils import deserialize_dict

# Configure the root logger to a higher level
logging.basicConfig(level=logging.WARNING)

# Configure module's logger to DEBUG
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_params(
    obj: Union[Task, PipelineController],
    key="General",
    default_params: Optional[Dict[str, Any]] = None,
):
    if default_params is None:
        logger.debug("No default params supplied. Using empty dict.")
        default_params = {}
    if isinstance(obj, PipelineController):
        obj = obj._task
    param_dict = obj.get_parameters_as_dict()
    avail_keys = list(param_dict.keys())
    if ("pipeline" in avail_keys) and (key not in avail_keys):
        avail_keys.remove("pipeline")
        if len(avail_keys) == 1:
            key = avail_keys[0]
            logger.debug(
                f"Only available (non-pipeline) key is `{key}`, returning its contents."
            )
        logger.debug(f"Key `{key}` not in parameters. Falling back to `Args`.")
        key = "Args"

    params = param_dict.get(key, default_params)
    logger.info("processing serialized keys from task arguments")
    return deserialize_dict(params)
