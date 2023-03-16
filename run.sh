#This file enables us to install the requirements for chatterbot in the background.
# -q installs quietly
echo 'Your personal zackBot is loading...'
pip --disable-pip-version-check install --no-warn-script-location -q -r requirements.txt

# then we have to manually run
python main.py