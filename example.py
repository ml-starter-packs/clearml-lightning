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
    fig, ax = plt.subplots(1,1)
    ax.plot(A, B, color="xkcd:shocking pink")
    # plt.show()
    logger.report_matplotlib_figure(
        "title",
        "series",
        fig,
        report_interactive=False,
        report_image=True,
    )
    logger.report_text("Done")


if __name__ == "__main__":
    start_time = time.time()
    task = Task.init(
        project_name="default",
        task_name="test-task-w-image",
        task_type=Task.TaskTypes.data_processing,
    )
    print(f"Time elapsed for task init: {time.time() - start_time}")

    params = {
        "N": 100,
    }
    params = task.connect(params, name="General")
    print(f"Time elapsed until parameter connection: {time.time() - start_time}")
    # task.execute_remotely()  # same networking issues with remote vs local execution.

    print(f"Time elapsed until work starts: {time.time() - start_time}")
    do_work(task, params)
    print("Exit")
    task.close()
