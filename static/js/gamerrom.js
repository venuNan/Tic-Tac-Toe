let para;
const socket = io.connect("http://localhost:5000", {query:para});
let yourTurn = false;

document.querySelectorAll('.cell').forEach(cell => {
    cell.addEventListener('click', function() {
        if (!this.textContent && yourTurn) {
            yourTurn = false;
            this.textContent = 'X';
        }
    });
});