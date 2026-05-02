import socketio
import time

seeker = socketio.Client()
donor = socketio.Client()

@seeker.on('status_update')
def on_seeker_status(data):
    print(f"[SEEKER] {data['msg']}")

@donor.on('new_food_request')
def on_donor_request(data):
    print(f"[DONOR NOTIF] New request from {data['phone']} for {data['type']}")
    print("[DONOR] Accepting request...")
    donor.emit('donor_accept', {'phone': data['phone'], 'donor_name': 'Test Donor'})

def test_flow():
    try:
        seeker.connect('http://localhost:5000')
        donor.connect('http://localhost:5000')
        print("[TEST] Both clients connected")
        
        # Step 1: Seeker starts call
        seeker.emit('trigger_start')
        seeker.emit('select_language', {'lang': 'en'})
        seeker.emit('select_city', {'city': 'bangalore'})
        
        # Step 2: Seeker selects Hunger Domain with Mock Location
        print("[TEST] Seeker selecting Hunger Domain with Location...")
        seeker.emit('select_domain', { 
            'domain': 'hunger',
            'lat': 12.9716, 
            'lng': 77.5946 
        })
        
        # Step 3: Seeker requests food
        print("[TEST] Seeker requesting Food Type: COOKED...")
        seeker.emit('hunger_action', {'action': 'request'})
        seeker.emit('food_type_action', {'type': 'cooked'})
        
        # Wait for donor logic
        time.sleep(2)
        
        # Step 4: Seeker 'dials' the donor (Press 1)
        print("[TEST] Seeker 'dialing' donor (Press 1)...")
        seeker.emit('donor_dial')
        
        time.sleep(3)
        
        seeker.disconnect()
        donor.disconnect()
        print("[TEST] Flow Completed")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    test_flow()
