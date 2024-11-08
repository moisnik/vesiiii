<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multiplayer Bingo</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.min.js"></script>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div id="startScreen">
        <h1>Welcome to Multiplayer Bingo!</h1>
        <p>Enter your Player ID to join the game:</p>
        <input type="text" id="playerId" placeholder="Player ID">
        <button onclick="joinGame()">Join Game</button>
    </div>

    <div id="gameArea" style="display:none;">
        <h2>Your Bingo Card:</h2>
        <div id="bingoCard"></div>
        <h3>Drawn Numbers:</h3>
        <div>
            <body>
                <h1 style="text-align: center;">Bingo!</h1>
                <table>
                    <tr>
                        <th>B</th><th>I</th><th>N</th><th>G</th><th>O</th>
                    </tr>
                    {% for i in range(5) %}
                    <tr>
                        {% for j in range(5) %}
                        {% if i == 2 and j == 2 %}
                        <td class="center-cell"><img src="{{ url_for('static', filename='taht.jpg') }}" alt="Täheke"></td>
                        {% else %}
                        <td>{{ board[i][j] }}</td>
                        {% endif %}
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </table>
            </body>
        </div>
        <div id="drawnNumbers"></div>
        <button onclick="drawNumber()">Draw Number</button>
        <button onclick="leaveGame()">Leave Game</button>
    </div>

    <script src="{{ url_for('static', filename='js/proovibingo.js') }}"></script>
</body>
</html>

