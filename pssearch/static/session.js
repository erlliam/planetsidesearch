let button = document.getElementById("session-button");
let webSocket;

button.addEventListener("click", startSession);

function startSession() {
	button.removeEventListener("click", startSession);
	button.addEventListener("click", endSession);
	button.innerHTML = "End session";
	webSocket = new WebSocket("wss://push.planetside2.com/streaming?environment=ps2&service-id=s:supafarma");
	let characterId = document.getElementById("char-id").innerHTML;
	let command = {
		service: "event",
		action: "subscribe",
		characters: [characterId],
		eventNames: ["Death"]
	};
	webSocket.onopen = function (event) {
		webSocket.send(JSON.stringify(command));
		let kills = 0;
		let deaths = 0;

		webSocket.onmessage = function (event) {
			let message = JSON.parse(event.data);
			if (message.hasOwnProperty("payload")) {
				let payload = message.payload;
				if (payload.attacker_character_id == characterId) { // kill
					kills = kills + 1;
				} else if (payload.attacker_character_id != characterId) { // death
					deaths = deaths + 1;
				}
				console.log(kills, deaths);
			}
		}
	}
}

function endSession() {
	webSocket.close();	
	console.log(webSocket);
	button.removeEventListener("click", endSession);
	button.addEventListener("click", startSession);
	button.innerHTML = "Start session";
}

