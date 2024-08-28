# clearml-lightning

This repository serves as a reference deployment for the `ClearML` docker-compose service on [lightning.ai](https://lightning.ai) Studios.

The purpose is to document the platform-specific steps required to get the ClearML experiment tracking service robustly deployed on lightning.ai, and explain the options available to users.

## getting started

We first go over the steps for a basic single-machine deployment, and then expand to scaling up compute with a second Studio, following much the same pattern.

The first deployment pattern we cover will begin with `localhost` as the configured host for clearml, and will use SSH tunnels to establish communications.

1. Start a new Lightning Studio and clone this repository.


## environment
`.env` contains the (bare minimum) environment variables that the docker-compose stack will be relying on.
(These are all set at the Studio level).

The `.env` file shows `$LIGHTNING_CLOUDSPACE_HOST` to demonstrate the use of the Lightning reverse proxy with the default exposed ports for ClearML.

## clearml
`sh setup.sh` to prepare the studio (this is even run as part of `on_start.sh` since docker settings don't persist).
`docker compose up -d` after setting and sourcing your environment variables. Wait about 30-60s and then visit


## example task
After going through the process of creating an access key/secret via the ClearML Web UI (port 8080, see settings), you'll populate `~/clearml.conf` with your settings:

`pip install clearml==1.15.1`


```bash
python example.py
```
