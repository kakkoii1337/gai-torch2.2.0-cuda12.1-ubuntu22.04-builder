## Setup

```bash
python -m venv .venv
source .venv/bin/activate 
pip install -r requirements.txt
```

## Build

**CTRL + SHIFT + P** > Select Interpreter > Select **.venv**
**CTRL + SHIFT + P** > Task: Run Task > Select **Docker: build**
**CTRL + SHIFT + P** > Task: Run Task > Select **Docker: push**
