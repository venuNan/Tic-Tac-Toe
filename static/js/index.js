console.log("script loaded");
let playername;
let roomname;
function createRoom(player_name, room_name) {
    fetch('/create-room', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ "player_name": player_name, "room_name": room_name }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data["status"]==="room_exists"){
            document.getElementById("room-error-message").style.display = "block";
        }
        else if (data["status"]==="room_created"){
            document.getElementById("room-created-message").style.display = "block";
        }
        
    })
    .catch(error => {
        console.error('Error creating room:', error);
    });
}


function joinRoom(player_name, room_name) {
    fetch('/join-room', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ "player_name": player_name, "room_name": room_name}),
    })
    .then(response => response.json())
    .then(data => {
        if (data["status"]==="room_full"){
            document.getElementById("room-error-message").style.display = "block";
        }
        else if (data["status"]==="room_not_exist"){
            document.getElementById("room-created-message").style.display = "block";
        }
        
    })
    .catch(error => {
        console.error('Error joining room:', error);
    });
}

document.querySelector(".myform").addEventListener("submit", function(event) {
    event.preventDefault();

    const player_name = document.getElementById("playername").value;
    const room_name = document.getElementById("roomname").value;

    const clickedButton = event.submitter.id;

    if (clickedButton === "create-room-button") {
        playername = player_name;
        roomname = room_name;
        createRoom(player_name, room_name);

        console.log("create room button clicked");
        
    } else if (clickedButton === "join-room-button") {
        playername = player_name;
        roomname = room_name;
        joinRoom(player_name, room_name);

        console.log("join room button clicked");
    }
    return false;
});

document.querySelectorAll('.inputs').forEach(ele => {
    ele.addEventListener("input", function() {
        
        const h2Elements = document.getElementsByTagName("h2");
        for (let i = 0; i < h2Elements.length; i++) {
            h2Elements[i].style.display = "none";
        }
    });
});