## Setup

```bash
python -m venv .venv
source .venv/bin/activate 
pip install -e .
```

## Build

**CTRL + SHIFT + P** > Select Interpreter > Select **.venv**

This is not necessary if environment is already activated before running vscode.

**CTRL + SHIFT + P** > Task: Run Task > Select **Docker: build downloader**

This is to create a local cache of large files for downstream images to install without having to download it all the time.
It is not good enough to use .cac  he for this or the cached layer because it is prone to be deleted.

**CTRL + SHIFT + P** > Task: Run Task > Select **Docker: build container_base**

The devcontainer image is not reusable because it is built with the context of the current directory.
This is to create a base image that can be reused by downstream devcontainer build.
NOTE: This is different from `Rebuild Container` which is used for the current context and remember that Rebuild Container does not rebuild the base image.

**Check** 

Some basic rule of thumbs to check if the setup is completed successfully:
    - `venv` should be activated.
    - `pip list | grep numpy` should be version 1.26.4
        If this has been upgraded to version 2.* then something must have gone wrong with dependencies.

