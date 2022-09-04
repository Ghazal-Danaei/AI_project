# DO NOT CHANGE THIS FILE.

import json
import traceback
from time import sleep

from gimulator.client import ActorClient
from gimulator.proto_pb2 import *

from agent import Agent

PROC_TIMEOUT_SECS = 600

client = None
def perceive(_self=None):
    global client
    response = client.Get(Key(type="action", name="director", namespace="sbu-ai-2021-snake"))
    return json.loads(response.content)


def main():
    global client

    print("[Actor] Starting init phase")
    
    # client = ActorClient(True, host="127.0.0.1:3333", token="638c8e51-5cd4-4092-ba81-79a402433cab")
    client = ActorClient(True)
    client.ImReady()

    totalRuns = 0
    
    for runMessage in client.Watch(Key(type="world", name="director-run", namespace="sbu-ai-2021-snake")):
        if "total" in runMessage.content:
            totalRuns = int(json.loads(runMessage.content)["total"])
            continue
        runIndex = int(runMessage.content)
        print(f"RUN {runIndex + 1}")

        # PHASE 1: INIT
        me = None

        # Getting agent info from director
        for message in client.Watch(Key(type="world", name="director-init", namespace="sbu-ai-2021-snake")):
            response = json.loads(message.content)
            me = Agent(perceive, 0)
            break

        # Broadcasting our readiness to director
        sleep(.25)
        client.Put(Message(key=Key(type="world", name="actor-init", namespace="sbu-ai-2021-snake"), content="ready"))

        print("[Actor] Init done")
        # END OF PHASE 1: INIT

        # PHASE 2: MAIN
        # Watching director responses and reacting accordingly
        sleep(.25)
        while True:
            sleep(.05)
            try:
                currentState = perceive()
                print([x for x in currentState])
                if currentState['status'] == "victory":
                    print(f"END OF RUN {runIndex + 1} (Victory)")
                    if runIndex == totalRuns - 1: exit(0)
                    else: break
                elif currentState['status'] in ["timed_out", "failed"]: # timed_out || failed
                    print(f"END OF RUN {runIndex + 1} (Error)")
                    exit(0)
                else:
                    print("acting ...")
                    client.Put(Message(key=Key(type="action", name="actor", namespace="sbu-ai-2021-snake"), content=json.dumps({
                        "action": me.act()
                    })))
                    print("done")
            except Exception as e:
                # PutResult
                tb = traceback.format_exc()
                print({
                    "action": "fail",
                    "message": f"Traceback: {tb}\nException: {str(e)}"
                })
                client.Put(Message(key=Key(type="action", name="actor", namespace="sbu-ai-2021-snake"), content=json.dumps({
                    "action": "fail",
                    "message": f"Traceback: {tb}\nException: {str(e)}"
                })))
                exit(0)


if __name__ == '__main__':
    main()