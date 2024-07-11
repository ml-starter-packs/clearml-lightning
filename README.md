# clearml-lightning

## environment
`.env` contains the (bare minimum) environment variables that the docker-compose stack will be relying on.
(These are all set at the Studio level).

The `.env` file shows `$LIGHTNING_CLOUDSPACE_HOST` to demonstrate the use of the Lightning reverse proxy with the default exposed ports for ClearML.

## clearml
`sh setup.sh` to prepare the studio (this is even run as part of `on_start.sh` since docker settings don't persist).
`docker compose up -d` after setting and sourcing your environment variables. Wait about 30-60s and then visit

## cloudflare tunnel

Download the latest binary for `cloudflared` from the [Releases page](https://github.com/cloudflare/cloudflared/releases/tag/2024.6.1).

Then run `cloudflared tunnel --url 0.0.0.0:8008` to set up a reverse proxy to the API backend, taking note of the url for the next step.

## example task
After going through the process of creating an access key/secret via the ClearML Web UI (port 8080, see settings), you'll populate `~/clearml.conf` with your settings:

`pip install clearml==1.15.1`

```
# ClearML SDK configuration file
api {
    # web_server on port 8080
    web_server: "https://8080-..."

    # Notice: 'api_server' is the api server (default port 8008), not the web server.
    api_server: "https://8008-..."

    # file server on port 8081
    files_server: "https://8081-..."

    # Credentials are generated using the webapp, http://localhost:8080/profile
    # these are sensitive credentials... do not commit them!

    # for notebooks, these need to be set here, unfortunately.
    credentials {
        "access_key" = ""
        "secret_key" = ""
    }
    # verify host ssl certificate, set to False only if you have a very good reason
    verify_certificate: True
}
```

Run `CLEARML_HOST_IP=<proxy you are testing> python example.py` to override the API host in the `clearml.conf` when testing, switching between `http://0.0.0.0:8008`, the cloudflare tunnel, and the lightning cloudspace hostname.

## tunneling
On a client machine, set `$LIGHTNING_CLOUD_SPACE_ID` to the one in this (server) Studio. Note: if setting from a different Studio, then set it as a prefix before running `connect.sh`.

> Alternatively, just modify this bash script to hard-code the server address for use on client machines.

Make sure `autossh` is installed:

```bash
# brew
brew install autossh

# debian
sudo apt install autossh
```

Then run `./connect.sh` (or `LIGHTNING_CLOUD_SPACE_ID=... ./connect.sh` to create three `autossh` tunnels, and connect to ClearML through `localhost:8080` for web UI, and configure your `clearml.conf` to point to these "local" addresses.

## nginx [not currently compatible with lightning]

ClearML makes strong assumptions about the structure of the domains used to host it. Either the port must be at the end of the string, or the subdomains `files`, `app`, and `web` must be used so that the authentication token issued by the ClearML Web UI can be scoped / shared correctly across services.

Since lightning _prefixes_ domains with port numbers for reverse-proxy purposes, we must work around ClearML's assumption and handle our own subdomains by setting up an nginx server as a sidecar container.

This allows us to only open up a single port on the Studio: Port `8000` for `nginx`.

run `make replace (DOMAIN=mydomain.com)` to run `sed` against the `nginx.conf` file in order to configure it for your Studio. If you do not specify `DOMAIN=...` it will use `8000-$LIGHTNING_CLOUDSPACE_HOST`.

Then `cp nginx.conf ~/` and `git restore nginx.conf` to avoid accidental commits and to place the config file where the `compose.yml` expects it.

