
## cloudflare tunnel as reverse proxy

Download the latest binary for `cloudflared` from the [Releases page](https://github.com/cloudflare/cloudflared/releases/tag/2024.6.1).

Then run `cloudflared tunnel --url 0.0.0.0:8008` to set up a reverse proxy to the API backend, taking note of the url for the next step.


## lightning's reverse proxy
You can configure `.env` to update the public/private interface on which clearml is hosted. 
The snippet that is generated in the ClearML UI when you generate credentials for your user will reflect the environment variables you set.

Note: They do not play nicely when the subdomain `files.`, `app.` and `api.` are not used, so you may need to manually set these yourself.

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


# WIP: ngninx proxy (subdomains in lightning.ai)
```dockerfile
  proxy:
    container_name: clearml-proxy
    image: nginx:latest
    networks:
      - backend
      - frontend
    ports:
      - "8000:80"
    volumes:
      - ~/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - apiserver
      - fileserver
      - webserver
    deploy:
      restart_policy:
        condition: on-failure
    environment:
      NGINX_HOST: 8000-${LIGHTNING_CLOUDSPACE_HOST:-}
      NGINX_PORT: 80
```


Run `CLEARML_HOST_IP=<proxy you are testing> python example.py` to override the API host in the `clearml.conf` when testing, switching between `http://0.0.0.0:8008`, the cloudflare tunnel, and the lightning cloudspace hostname.
