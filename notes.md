# Additional Deployment Notes

## [WIP] tunneling
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
