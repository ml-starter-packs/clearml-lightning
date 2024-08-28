
- [X] document how to get the initial API key working (services)
- [X] port examples
- [ ] validate examples
- [X] switch back to ~/opt
- [ ] try upgrading clearml versions
- [ ] elastic logs not working with `~/usr` due to permissions. (this fails: `~/usr/share/elasticsearch/logs:/usr/share/elasticsearch/logs`)
- [ ] agent setup (automatic)
- [X] authentication
- [ ] docs for examples (reflect new script names)
- [X] .env file
- [X] Why does agent-services only run one container at a time?
- [ ] multiple users documented

The default secret for the system's apiserver component can be overridden by setting the following environment variable: CLEARML__SECURE__CREDENTIALS__APISERVER__USER_SECRET="my-new-secret"