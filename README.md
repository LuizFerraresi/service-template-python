
# Service Template - Python

## Index


## Requirements

- [direnv]()
- [taskfile](https://taskfile.dev/)
- [pyenv]()
- [docker]()

# Folder Structure

```bash
repository /
├── .containers/          # containers for local build
├── .github/              # github repository config dir
├── .helm/                # helm config for kubernetes deploy
├── src/                  # source code dir
├── tests/                # tests dir
├── .env.sample           # environment variables file
├── .envrc                # direnv config to expose variables
├── .pre-commit-hook      # pre-commit hooks config file
├── .python-version       # pyenv python version reference
├── docker-compose.yaml
├── Dockerfile
├── pyproject.toml        # python project config file
├── README.md
└── taskfile.yaml
```
