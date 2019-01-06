#!/usr/bin/python

# run with:
#   export FLASK_APP=forum.py FLASK_ENV=development
#   flask run --port 1666

from flask import Flask, redirect, url_for

app = Flask(__name__)

LOGGED_NONE     = 0
LOGGED_VICTIM   = 1
LOGGED_ATTACKER = 2
LOGGED_AS       = LOGGED_NONE

# List of (id, message)
MESSAGES = []

def account_exists(user_id):
	global LOGGED_ATTACKER
	global LOGGED_VICTIM
	if user_id == LOGGED_ATTACKER or user_id == LOGGED_VICTIM:
		return True

	return False

@app.route('/login/<int:user_id>')
def login(user_id):
	global LOGGED_AS
	if account_exists(LOGGED_AS):
		return 'Already logged in'

	if not account_exists(user_id):
		return 'Invalid account'

	LOGGED_AS = user_id

	return redirect(url_for('thread'))

@app.route('/logout')
def logout():
	global LOGGED_AS
	global LOGGED_NONE
	if not account_exists(LOGGED_AS):
		return 'Not logged in'

	LOGGED_AS = LOGGED_NONE

	return 'Logged out'

@app.route('/thread')
def thread():
	global LOGGED_AS
	if not account_exists(LOGGED_AS):
		return 'Not logged in'

	text = ''
	for entry in MESSAGES:
		text += str(entry[0]) + ': ' + entry[1] + '<br/>'

	return text

@app.route('/post/<path:message>')
def post(message):
	global LOGGED_AS
	global MESSAGES
	if not account_exists(LOGGED_AS):
		return 'Not logged in'

	MESSAGES.append((LOGGED_AS, message))

	return 'Posted successfully'
