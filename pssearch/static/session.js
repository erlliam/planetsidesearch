let button = document.getElementById("session-button");
let webSocket;

button.addEventListener("click", startSession);

function idToName(num) {
	xhttp = new XMLHttpRequest();
	
	xhttp.open("GET", "/id_to_name?id=" + num);
	xhttp.send();
	xhttp.onreadystatechange = function () {
		console.log(this.status);
		if (this.status == 200) {
			omfg = JSON.parse(this.responseText);
			console.log("wtf bor", omfg.name);
		}
	}
}

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
		let kills = [];
		let deaths = [];

		webSocket.onmessage = function (event) {
			let message = JSON.parse(event.data);
			if (message.hasOwnProperty("payload")) {
				let payload = message.payload;
				if (payload.attacker_character_id == characterId) { // kill
					console.log("kill");
					kills.push(idToName(payload.character_id));
				} else if (payload.attacker_character_id != characterId) { // death
					console.log("die");
					deaths.push(idToName(payload.attacker_character_id));
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

