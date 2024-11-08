from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room
import random

app = Flask(__name__)
socketio = SocketIO(app)

# Game state
game_state = {
    'players': {},
    'bingo_numbers': list(range(1, 76)),
    'drawn_numbers': [],
    'current_player': None
}

def generate_bingo_board():
    # Generate numbers for each column of the Bingo board
    columns = {
        "B": random.sample(range(1, 16), 5),
        "I": random.sample(range(16, 30), 5),
        "N": random.sample(range(31, 45), 5),
        "G": random.sample(range(46, 60), 5),
        "O": random.sample(range(61, 75), 5),
    }

    # Place a "free space" in the center of the board
    columns["N"][2] = "FREE"
    
    # Convert columns to rows for easier display in HTML
    board = [[columns[col][i] for col in columns] for i in range(5)]
    return board



# Function to shuffle and draw a number
def draw_number():
    if game_state['bingo_numbers']:
        number = random.choice(game_state['bingo_numbers'])
        game_state['bingo_numbers'].remove(number)
        game_state['drawn_numbers'].append(number)
        return number
    return None

@app.route('/')
def index():
    # Show the start screen when the user accesses the site
    return render_template('proovibingo.html')
def bingo():
    board = generate_bingo_board()
    return render_template('proovibingo.html', board=board)

# Handle a player joining the game
@socketio.on('join_game')
def handle_join_game(data):
    player_id = data['player_id']
    game_state['players'][player_id] = {
        'card': random.sample(range(1, 76), 25),
        'marked': set()
    }
    join_room(player_id)
    emit('game_state', game_state, room=player_id)

# Handle marking a number on the player's card
@socketio.on('mark_number')
def handle_mark_number(data):
    player_id = data['player_id']
    number = data['number']
    if number in game_state['players'][player_id]['card']:
        game_state['players'][player_id]['marked'].add(number)
        emit('game_state', game_state, broadcast=True)

# Handle drawing a new Bingo number
@socketio.on('draw_number')
def handle_draw_number():
    number = draw_number()
    if number:
        emit('new_number', number, broadcast=True)
    else:
        emit('game_over', "No more numbers to draw!", broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)
