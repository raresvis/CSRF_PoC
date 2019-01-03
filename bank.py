#!/usr/bin/python

# run with:
#   export FLASK_APP=bank.py FLASK_ENV=development
#   flask run --port 1999

from flask import Flask, redirect, url_for

app = Flask(__name__)

LOGGED_NONE     = 0
LOGGED_VICTIM   = 1
LOGGED_ATTACKER = 2
LOGGED_AS       = LOGGED_NONE

# List of (id, message)
DEPOSITS = {}
DEPOSITS[LOGGED_VICTIM]   = 100
DEPOSITS[LOGGED_ATTACKER] = 100

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

	return redirect(url_for('deposits'))

@app.route('/logout')
def logout():
	global LOGGED_AS
	global LOGGED_NONE
	if not account_exists(LOGGED_AS):
		return 'Not logged in'

	LOGGED_AS = LOGGED_NONE

	return 'Logged out'

@app.route('/transfer/<int:user_id>/<int:amount>')
def transfer(user_id, amount):
	global LOGGED_AS
	if not account_exists(LOGGED_AS):
		return 'Not logged in'

	if not account_exists(user_id):
		return 'Invalid account'

	DEPOSITS[LOGGED_AS] -= amount
	DEPOSITS[user_id]   += amount

	return redirect(url_for('deposits'))

@app.route('/deposits')
def deposits():
	global LOGGED_AS
	if not account_exists(LOGGED_AS):
		return 'Not logged in'

	text = str(LOGGED_VICTIM) + ': ' + str(DEPOSITS[LOGGED_VICTIM])
	text += '<br/>'
	text += str(LOGGED_ATTACKER) + ': ' + str(DEPOSITS[LOGGED_ATTACKER])

	return text
