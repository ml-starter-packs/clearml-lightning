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
