let button = document.getElementById("session-button");
let webSocket;

button.addEventListener("click", startSession);

function makeTableRow(attacker, target) {
	let tr = document.createElement("tr");
	let tdAttacker = document.createElement("td");
	let tdTarget = document.createElement("td");
	tdAttacker.innerHTML = attacker;
	tdTarget.innerHTML = target;
	tr.appendChild(tdAttacker);
	tr.appendChild(tdTarget);
	document.getElementById("killboard").appendChild(tr);
}

function idToName(num, name, array, killOrDeath) {
	xhttp = new XMLHttpRequest();
	xhttp.open("GET", `/id_to_name?id=${num}`);
	xhttp.send();
	xhttp.onload = function() {
		if (killOrDeath == "kill") {
			makeTableRow(name, xhttp.response);
		} else if (killOrDeath == "death") {
			makeTableRow(xhttp.response, name);
		}
		array.push(xhttp.responseText);
	}
}

function startSession() {
	button.removeEventListener("click", startSession);
	button.addEventListener("click", endSession);
	button.innerHTML = "End session";
	webSocket = new WebSocket("wss://push.planetside2.com/streaming?environment=ps2&service-id=s:supafarma");
	let characterId = document.getElementById("char-id").innerHTML;
	let characterName = document.getElementById("search-name").innerHTML;
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
					console.log(characterName);
					idToName(payload.character_id, characterName, kills, "kill");
					console.log("kill");
				} else if (payload.attacker_character_id != characterId) { // death
					idToName(payload.character_id, characterName, deaths, "death");
					console.log("die");
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

