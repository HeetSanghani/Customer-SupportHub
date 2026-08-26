import requests
import uuid

WEBHOOK_URL = "http://localhost:8000/api/v1/webhooks/email"
IMAGE_PATH = "/home/python/.gemini/antigravity/brain/e6d4f91f-8203-44cb-bdf5-14e0e03fe596/broken_router_1786533778457.png"

def simulate_mailgun_webhook():
    print(f"Sending mock email with attachment to {WEBHOOK_URL}...")
    
    # Mailgun sends data as multipart/form-data
    data = {
        "sender": "John Doe <john.doe@example.com>",
        "subject": "My internet router is completely broken!",
        "body-plain": "Hi SupportHub,\n\nMy internet router stopped working today. The red light is blinking, and I think the antenna is cracked. I've attached a picture for your reference.\n\nCan you please send a replacement?\n\nThanks,\nJohn",
        "Message-Id": f"<test-message-{uuid.uuid4().hex}@sandbox.mailgun.org>",
        "attachment-count": "1"
    }
    
    try:
        with open(IMAGE_PATH, "rb") as f:
            files = {
                "attachment-1": ("broken_router.png", f, "image/png")
            }
            response = requests.post(WEBHOOK_URL, data=data, files=files)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                print("\n✅ Success! The simulated email and attachment were received by the backend.")
                print("Check your Admin Dashboard > Global Inbox to see the new email ticket with the attached image!")
            else:
                print("\n❌ Failed to send webhook.")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    simulate_mailgun_webhook()
