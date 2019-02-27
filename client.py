from auth import token
import json
from websocket import create_connection
import ssl
import time
import pyautogui

########################
#   EEG Application    #
#   Kevin Cui          #
########################

thought = ""

print("\n============================")
print("Connecting to websocket...")
receivedData = create_connection("wss://emotivcortex.com:54321", sslopt={"cert_reqs": ssl.CERT_NONE})

print("Checking headset connectivity...")

receivedData.send(json.dumps({
    "jsonrpc": "2.0",
    "method": "queryHeadsets",
    "params": {},
    "id": 1
}))

print(receivedData.recv())

print("\nCreating session...")

receivedData.send(json.dumps({
    "jsonrpc": "2.0",
    "method": "createSession",
    "params": {
        "_auth": token,
        "status": "open",
        "project": "test"
    },
    "id": 1
}))

print(receivedData.recv())

print("\nSubscribing to session...")

receivedData.send(json.dumps({
    "jsonrpc": "2.0",
    "method": "subscribe",
    "params": {
        "_auth": token,
        "streams": [
            "sys"
        ]
    },
    "id": 1
}))

print(receivedData.recv())

print("\nGetting detection info...")

receivedData.send(json.dumps({
    "jsonrpc": "2.0",
    "method": "getDetectionInfo",
    "params": {
        "detection": "mentalCommand"
    },
    "id": 1
}))

print(receivedData.recv())


def train_command(request):
    print("Training " + request + " command...")
    receivedData.send(json.dumps( {
     "jsonrpc": "2.0", 
     "method": "training", 
     "params": {
       "_auth":token,
       "detection":"mentalCommand",
       "action":request,
       "status":"start"
     }, 
     "id": 1
     }))

    print(receivedData.recv())
    time.sleep(5)
    print(receivedData.recv())
    time.sleep(10)
    print(receivedData.recv())

    receivedData.send(json.dumps( {
     "jsonrpc": "2.0", 
     "method": "training", 
     "params": {
         "_auth":token,
         "detection":"mentalCommand",
         "action":request,
         "status":"accept"
     }, 
     "id": 1
     }
    ))

    print(receivedData.recv())
    time.sleep(2)
    print(receivedData.recv())


while True:
    while True:
        try:
            startCode = input('\n\nTo train commands, type "1". To begin the game, type "2"\n>>> ')
            if startCode == "1" or startCode == "2":
                break
            else:
                print("Invalid input")
        except ValueError:
            print("Invalid input")

    if startCode == "1":
        while True:
            try:
                req = input("Which command would you like to train? (Neutral, Left, Right, Lift, Drop, Push)\n>>> ").lower()         

                if req == "neutral" or req == "lift" or req == "drop" or req == "left" or req == "right" or req == "push":
                    train_command(req)
                    break
                else:
                    print("Invalid input")
            except:
                print("Invalid input")
                
    elif startCode == "2":

        print("Getting USER login...")

        receivedData.send(json.dumps({
            "jsonrpc": "2.0",
            "method": "getUserLogin",
            "id": 1
        }))

        profile = json.loads(receivedData.recv())["result"][0]
        print(profile)
        
        receivedData.send(json.dumps({
            "jsonrpc": "2.0",
            "method": "subscribe",
            "params": {
                "_auth": token,
                "streams": [
                    "com"
                ]
            },
            "id": 1
        }))

        print("Subscription:", receivedData.recv())

        receivedData.send(json.dumps({
            "jsonrpc": "2.0",
            "method": "setupProfile",
            "params": {
                "_auth": token,
                "profile": profile,
                "status": "create"
            },
            "id": 1
        }))

        print("Profile Set-up:", receivedData.recv())

        receivedData.send(json.dumps({
            "jsonrpc": "2.0",
            "method": "mentalCommandBrainMap",
            "params": {
                "_auth": token,
                "profile": profile

            },
            "id": 1
        }))

        synapseData = receivedData.recv()

        print("Mental Command Brain Map:", synapseData)

        while True:
            thought = json.loads(receivedData.recv())["com"][0]
            print(thought)

            maxX, maxY = pyautogui.size()

            try:
                x, y = pyautogui.position()      
            except KeyboardInterrupt:
                print('\n')

            if thought == "left" and x>0:
                pyautogui.move(-4, None)
            elif thought == "right" and x<maxX:
                pyautogui.move(4, None)
            elif thought == "lift" and y<maxY:
                pyautogui.move(None, -4)
            elif thought == "drop" and y>0:
                pyautogui.move(None, 4)
            elif thought == "neutral":
                pyautogui.move(None, None)
            elif thought == "push":
                pyautogui.click()
                            
