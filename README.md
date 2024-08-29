# clearml-lightning

This repository serves as a reference deployment for the `ClearML` docker-compose service on [lightning.ai](https://lightning.ai) Studios.

The purpose is to document the platform-specific steps required to get the ClearML experiment tracking service robustly deployed on lightning.ai, and explain the options available to users.

## getting started

For the impatient:
> assuming `docker`, `docker-compose`, `python3` and `make` are installed... clone the repo, `cd` into it, run `make install` and `make up` then skip to Step 5.

We first go over the steps for a basic single-machine deployment, and then expand to scaling up compute with a second Studio, following much the same pattern.

The first deployment pattern we cover will begin with `localhost` as the configured host for clearml, and will use SSH tunnels to establish communications.

1. Start a new Lightning Studio and clone this repository.
2. Run the setup script and copy some config files to the `~/.lightning_studio/` directory:

    ```bash
    make install
    ```

    Under the hood, this runs `make .env` first.
    
    This command copies `.env.template` to `.env`, ensuring to populate `CLEARML_AGENT_ACCESS_KEY` and `CLEARML_AGENT_ACCESS_SECRET` with secure credentials.

    Note: These keys are set with the following command (in case you already have a `.env` and want to set new keys):
    ```bash
    make keys >> .env
    ```

3. Optionally, if using a private repo for your ClearML workloads, populate `.env` with your git credential tokens. Whatever `git remote -v` shows you is what ClearML will use when it attempts to clone. If you cloned a public repo but used `git@github.com...`, you can modify the configuration in the task definition (when in Draft state), change your remote, or use an app password anyway.

4. Start ClearML with `make up`, query the docker container statuses with `make status`.

5. To connect: Download `connect.sh` and move it to `~/.local/bin/connect` on your system (ensuring `chmod +x` has been run on it and that `~/.local/bin` is in your `PATH`) on any machines that need to connect to ClearML (including the one that is running your web browser)

    The following will print a connection command for you:
    ```bash
    make host
    ```

6. With your tunnel established, connect to `localhost:8080` to visit the web front-end of ClearML. By default, there will be no security on this page, so you can create a new user from the welcome screen.
    
    Go to `Settings > Workspace` in ClearML's web UI (press the user-profile icon in the top right corner)

    Then generate new app credentials. Copy the config file to `clearml.conf` on the computer you plan to run scripts from (tunnels must be used for each of these, more on this later).

7. You are now ready to run examples: 

    Navigate to [`examples/README.md`](examples/README.md) for instructions on populating your ClearML instance with some content that can be used to stress test the system.

8. You may notice experiments not completing, because we have not yet deployed agents. See the section below.


> Note: if you're running `make fresh` to test out brand-new deployments, make sure to clear your browser cookies (or start a new private browser) when connecting to ClearML.

## agents
TODO: automate this entirely.

Fill in `agents/.env` (`cd agents && make .env`, then edit it) with 
```bash
CLEARML_API_ACCESS_KEY
CLEARML_API_SECRET_KEY
```
set to the contents of `CLEARML_AGENT_ACCESS_KEY`/`CLEARML_AGENT_ACCESS_SECRET` in `.env` at the root of this repository, or with App credentials associated to user (ideally one created for the purpose of remote workers).

Then:
```bash
cd agents/
make up
```

## deployment considerations

### user creation
Let's tear down our initial instance and create a new one with basic user authentication.

TODO....


### agents on separate studios
TODO ...

### developers on separate studios
TODO ...

### security:
TODO: set non-default credentials for `secure.conf`. can use env vars to override them, and a bash script to populate.


### automating startup / shutdown
`sh setup.sh` to prepare the studio (this is even run as part of `on_start.sh` since docker settings don't persist).
`docker compose up -d` after setting and sourcing your environment variables. Wait about 30-60s and then visit
