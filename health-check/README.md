# Run Local:
```bash
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
source ~/.bashrc
pyenv local 3.11.0
poetry run uvicorn main:app --host 0.0.0.0 --port 8080
```