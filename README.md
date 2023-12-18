# CPUMon-win-py-ino
A simple Windows CPU usage querier &amp; preprocessor in Python, for an Arduino program. Sample Arduino program included.

Currently not finished, some bugs and behaviours need polishing. Should work well on Linux with light changes.

## How to run

In PowerShell or Command Prompt, issue these commands within the directory where main.py is located.

(optionally) `python3 -m venv env && .\env\Scripts\activate`

`pip3 install -r requirements.txt`

`python3 main.py`

Check main.log if you suspect any errors. For Linux users, the venv activation is normally done as such: `source env/bin/activate`.
