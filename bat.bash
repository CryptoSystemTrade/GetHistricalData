#! bin/bash
source .venv/bin/activate
cd gethistricaldata
python main.py "$@" 

deactivate