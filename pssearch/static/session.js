var exampleSocket = new WebSocket("wss://push.planetside2.com/streaming?environment=ps2&service-id=s:supafarma");
console.log(exampleSocket);
exampleSocket.onmessage = function (event) {
	console.log(event.data);
}
