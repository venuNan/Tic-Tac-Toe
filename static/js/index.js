
function createRoom(playerName, roomName) {
    fetch('/create-room', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ playerName, roomName }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Room created:', data);
    })
    .catch(error => {
        console.error('Error creating room:', error);
    });
}

function joinRoom(playerName, roomName) {
    fetch('/join-room', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ playerName, roomName }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Joined room:', data);
    })
    .catch(error => {
        console.error('Error joining room:', error);
    });
}

document.querySelector(".myform").addEventListener("submit", function(event) {
    event.preventDefault();

    const playerName = document.getElementById("playername").value;
    const roomName = document.getElementById("roomname").value;

    const clickedButton = event.submitter.id;

    if (!playerName || !roomName) {
        document.getElementById("error-message").style.display = "block";
        return;
    }

    if (clickedButton === "create-room-button") {
        createRoom(playerName, roomName);
        
    } else if (clickedButton === "join-room-button") {
        joinRoom(playerName, roomName);
        
    }
    return false;
});

document.getElementById("roomname").addEventListener("input", function() {
    document.getElementById("error-message").style.display = "none";
});
