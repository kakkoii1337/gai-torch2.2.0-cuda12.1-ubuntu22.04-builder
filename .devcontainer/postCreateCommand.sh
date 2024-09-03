# Install utils so that we can run vscode tasks.
whoami

source ~/.venv/bin/activate
pip install -e .

pip list | grep numpy
pip list | grep gai-sdk
pip list | grep torch