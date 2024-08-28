# clearml-lightning

This repository serves as a reference deployment for the `ClearML` docker-compose service on [lightning.ai](https://lightning.ai) Studios.

The purpose is to document the platform-specific steps required to get the ClearML experiment tracking service robustly deployed on lightning.ai, and explain the options available to users.

## getting started

For the impatient:
> assuming `docker`, `docker-compose`, `python3` and `make` are installed... clone the repo, `cd` into it, run `make up` then skip to Step 5.

We first go over the steps for a basic single-machine deployment, and then expand to scaling up compute with a second Studio, following much the same pattern.

The first deployment pattern we cover will begin with `localhost` as the configured host for clearml, and will use SSH tunnels to establish communications.

1. Start a new Lightning Studio and clone this repository.
2. Run `make .env`.
    
    This command copies `.env.template` to `.env`, ensuring to populate `CLEARML_AGENT_ACCESS_KEY` and `CLEARML_AGENT_ACCESS_SECRET` with secure credentials.

    Note: These keys are set with the following command (in case you already have a `.env` and want to set new keys):
    ```bash
    make keys >> .env
    ```

3. Optionally, if using a private repo for your ClearML workloads, populate `.env` with your git credential tokens.

4. Start ClearML with `make up`, query the docker container statuses with `make status`.

5. To connect: Download `connect.sh` and move it to `~/.local/bin/connect` on your system (ensuring `chmod +x` has been run on it and that `~/.local/bin` is in your `PATH`) on any machines that need to connect to ClearML (including the one that is running your web browser)

    The following will print a connection command for you:
    ```bash
    make host
    ```
6. Connect to `localhost:8080` to visit the web front-end of ClearML. By default, there will be no security on this page, so you can create a new user from the welcome screen.
    
    Go to `Settings > Workspace` in ClearML's web UI (press the user-profile icon in the top right corner)

    Then generate new app credentials. Copy the config file to `clearml.conf`

7. You are now ready to run examples: `make examples`

Note: if you're running `make fresh` to test out brand-new deployments, make sure to clear your browser cookies (or start a new private browser) when connecting to ClearML.

## environment
`.env` contains the (bare minimum) environment variables that the docker-compose stack will be relying on.
(These are all set at the Studio level).

By default, we have `localhost` configured, but the `.env` file also shows how to leverage `$LIGHTNING_CLOUDSPACE_HOST` / `$LIGHTNING_CLOUD_SPACE_ID` to demonstrate the use of the Lightning reverse proxy with the default exposed ports for ClearML. This is not yet supported. See [`PROXY.md`](PROXY.md) for more information.

## clearml
`sh setup.sh` to prepare the studio (this is even run as part of `on_start.sh` since docker settings don't persist).
`docker compose up -d` after setting and sourcing your environment variables. Wait about 30-60s and then visit


## example task
Navigate to [`examples/README.md`](examples/README.md) for instructions on populating your ClearML instance with some content that can be used to stress test the system.
