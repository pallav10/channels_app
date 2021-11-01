import json
import websocket

# import _thread
import time


def on_message(ws, message):
    if not message:
        numbers = input("Enter numbers separated by spaces: ")
        ws.send(numbers)
    else:
        print("message is ", json.loads(message).get("message"))
        on_open(ws)

def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    on_message(ws, message=None)


if __name__ == "__main__":
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        "ws://127.0.0.1:8080/ws/rearrange/1",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever()
