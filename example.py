import time

import matplotlib.pyplot as plt
import numpy as np
import polars as pl

from clearml import Task


def do_work(task, params):
    logger = task.get_logger()
    logger.report_text("Running main function")
    N = params.get("N", 10)

    A = np.arange(N)
    B = np.random.rand(N)
    plt.plot(A, B, color="xkcd:shocking pink")
    plt.show()
    logger.report_text("Done")


if __name__ == "__main__":
    start_time = time.time()
    task = Task.init(
        project_name="default",
        task_name="parameterized-example-task",
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
