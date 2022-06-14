#! bin/bash
cd ~/Cron/GetHistricalData
source .venv/bin/activate
cd gethistricaldata
python main.py "$@" 

deactivate
