import time

import matplotlib.pyplot as plt
import numpy as np

from clearml import Task


def do_work(task, params):
    logger = task.get_logger()
    logger.report_text("Running main function")
    N = params.get("N", 10)

    A = np.arange(N)
    B = np.random.rand(N)
    fig, ax = plt.subplots(1, 1)
    ax.plot(A, B, color="xkcd:shocking pink")
    # plt.show()
    # Debug Samples Tab
    logger.report_matplotlib_figure(
        title="metric",  # Shows up as "Metric:" in UI
        series="series",  # label under the image
        figure=fig,
        iteration=None,  # defaults to 0, collapsable element in UI
        report_interactive=False,
        report_image=True,
    )

    # Plotly Figure (automatic conversion under the hood)
    fig2, ax2 = plt.subplots(1, 1)
    ax2.plot(A, B, color="xkcd:shocking pink")
    logger.report_matplotlib_figure(
        title="title",
        series="interactive",
        figure=fig2,
        report_interactive=True,
        report_image=False,
    )

    # Standard Image (PNG)
    fig3, ax3 = plt.subplots(1, 1)
    ax3.plot(A, B, color="xkcd:shocking pink")
    logger.report_matplotlib_figure(
        title="title",  # this title will show up in the figure with "title/series" formatting
        series="noninteractive",
        figure=fig3,
        report_interactive=False,
        report_image=False,
    )

    logger.report_text("Done")
    # Artifact(s)
    # basic numpy objects stored in .npz
    task.upload_artifact(
        name="array-artifact",
        artifact_object=B,
        metadata={"test-meta": "something_here"},
    )

    # as soon as the structure becomes more complicated, .pkl is used
    task.upload_artifact(
        name="list-artifact",
        artifact_object=[A, B],
        metadata={"test-meta": "something_here"},
    )


def init_task_params(task: Task) -> Task:
    """Demonstrates multiple ways to pass arguments to task via UI"""
    params = {
        "N": 100,
    }
    params = task.connect(params, name="ShapeParameters")
    print(f"Param (dict) connection: {params}, type: {type(params)}")

    # this will be of type 'list'
    # Note: despite this being a list, it's reported as a dictionary in the UI
    _list_conf = ["my", "list", "of", "features"]
    list_conf = task.connect_configuration(
        configuration=_list_conf, name="feature_list"
    )

    # this will be of type 'clearml.utilities.proxy_object.ProxyDictPostWrite'
    _dict_config = {f"feature_{k:02d}": (np.random.rand() > 0.5) for k in range(10)}
    dict_conf = task.connect_configuration(
        configuration=_dict_config, name="feature_dict"
    )
    print(f"List Config: {list_conf}, type: {type(list_conf)}")
    print(f"Dict Config: {dict_conf}, type: {type(dict_conf)}")
    return task, params, list_conf, dict_conf


if __name__ == "__main__":
    start_time = time.time()
    # Task.force_requirements_env_freeze(force=True, requirements_file="requirements.txt")
    task = Task.init(
        project_name="dev/tests",
        task_name="demo-task",
        task_type=Task.TaskTypes.data_processing,
        auto_connect_arg_parser=True,
    )
    task.set_repo(repo="https://github.com/ml-starter-packs/clearml-lightning.git")
    print(f"Time elapsed for task init: {time.time() - start_time}")
    task, params, list_conf, dict_conf = init_task_params(task)
    print(f"Time elapsed until parameter connection: {time.time() - start_time}")
    task.set_comment("this populates the description field")
    # task.execute_remotely()  # same networking issues with remote vs local execution.

    print(f"Time elapsed until work starts: {time.time() - start_time}")
    do_work(task, params)
    print("Exit")
    task.close()
