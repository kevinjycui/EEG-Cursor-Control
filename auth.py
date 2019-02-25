import json
import ssl
from websocket import create_connection

receivedData = create_connection("wss://emotivcortex.com:54321", sslopt={"cert_reqs": ssl.CERT_NONE})

receivedData.send(json.dumps({
    "jsonrpc": "2.0",
    "method": "authorize",
    "params": {},
    "id": 1
}))

msg = receivedData.recv()
token = msg[43:-3]

print("Hello USER.")
print("\nThe following set of letters is your session token. In order maintain security, do not share this token:\n\n"+str(token))
print("\n\nThis token has been automatically registered as your session token. You may use the headset as a client")
