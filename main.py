from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Function to run Pygame
def run_pygame():
    os.system('cd start_project/ && python3 main.py')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-game')
def start_game():
    run_pygame()
    return "Game Closed"

if __name__ == '__main__':
    app.run(debug=True)
