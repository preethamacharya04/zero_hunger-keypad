import socketio
import time

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")
    sio.emit('trigger_start')
    time.sleep(1)
    sio.emit('select_language', {'lang': 'en'})
    time.sleep(1)
    sio.emit('select_city', {'city': 'bangalore'})
    time.sleep(1)
    sio.emit('select_domain', {'domain': 'agriculture'})
    time.sleep(1)
    sio.emit('agri_action', {'action': 'market_price'})
    time.sleep(2)
    sio.disconnect()

@sio.on('status_update')
def on_status(data):
    print(f"Status Update: {data['msg']}")

if __name__ == '__main__':
    try:
        sio.connect('http://localhost:5000')
        sio.wait()
    except Exception as e:
        print(f"Error: {e}")
