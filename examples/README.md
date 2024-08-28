# Examples

The examples herein are provided to demonstrate some of the trickier parts of using ClearML, namely:
- how to pass UI parameters in pipelines to underlying tasks
- how to create pipelines that can be scaled (horizontally), which will be useful for testing remote worker scaling.
- covers a practical example of common operations (map/reduce), demonstrating most of the ClearML Task + Pipeline workflow features:
  - Metrics
  - Models
  - Artifacts
  - Pipelines
  - Monitoring
- how to leverage the ClearML API to scale tasks and aggregate results from many experiments


## Credentialing

Settings > Workspace in ClearML's web UI.

Then generate new app credentials. 
Copy / paste the section it gives you into `~/clearml.conf`

Once completed, you are ready to run `python <example-name>.py` and various other clearml-related commands.

