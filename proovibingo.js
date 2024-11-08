const socket = io.connect('http://localhost:5001');

let playerId = '';
let card = [];

function joinGame() {
    playerId = document.getElementById('playerId').value;
    if (playerId) {
        socket.emit('join_game', { 'player_id': playerId });
        document.getElementById('startScreen').style.display = 'none';
        document.getElementById('gameArea').style.display = 'block';
    }
}

// Receive game state and render Bingo card
socket.on('game_state', function(state) {
    if (state.players[playerId]) {
        card = state.players[playerId].card;
        displayBingoCard();
    }
});

// Display the Bingo card
function displayBingoCard(card) {
    let cardHtml = '<table>';
    const columns = ['B', 'I', 'N', 'G', 'O'];
    for (let i = 0; i < 5; i++) {
        cardHtml += '<tr>';
        for (let col of columns) {
            cardHtml += `<td>${card[col][i]}</td>`;
        }
        cardHtml += '</tr>';
    }
    cardHtml += '</table>';
    document.getElementById('bingoCard').innerHTML = cardHtml;
}
// Draw a new Bingo number
function drawNumber() {
    socket.emit('draw_number');
}

// Leave the game
function leaveGame() {
    socket.emit('leave_game', { 'player_id': playerId });
    document.getElementById('gameArea').style.display = 'none';
    document.getElementById('startScreen').style.display = 'block';
}

socket.on('game_state', function(data) {
    displayBingoCard(data.card);
    // Display any drawn numbers
    const drawnNumbersDiv = document.getElementById('drawnNumbers');
    drawnNumbersDiv.innerHTML = data.drawn_numbers.map(n => `<p>${n}</p>`).join('');
});
// Receive the new number drawn
socket.on('new_number', function(number) {
    const drawnNumbersDiv = document.getElementById('drawnNumbers');
    drawnNumbersDiv.innerHTML += `<p>${number}</p>`;
});
