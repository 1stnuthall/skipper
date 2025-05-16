# Basic Slack Bolt + OSM API Key storage app in Python using HashiCorp Vault (AppRole auth)
import os
import base64
import requests
from cryptography.fernet import Fernet
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()

ENCRYPTION_SECRET = os.getenv("ENCRYPTION_SECRET")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
VAULT_ADDR = os.getenv("VAULT_ADDR")  # e.g., http://127.0.0.1:8200
VAULT_ROLE_ID = os.getenv("VAULT_ROLE_ID")
VAULT_SECRET_ID = os.getenv("VAULT_SECRET_ID")
VAULT_SECRET_PATH = os.getenv("VAULT_SECRET_PATH", "secret/data/osm-api-keys/")  # KV v2 path

fernet = Fernet(base64.urlsafe_b64encode(ENCRYPTION_SECRET.encode().ljust(32, b'0')))

def encrypt(text):
    return fernet.encrypt(text.encode()).decode()

def decrypt(token):
    return fernet.decrypt(token.encode()).decode()

def get_vault_token():
    url = f"{VAULT_ADDR}/v1/auth/approle/login"
    payload = {
        "role_id": VAULT_ROLE_ID,
        "secret_id": VAULT_SECRET_ID,
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["auth"]["client_token"]
    except Exception as e:
        raise Exception(f"Vault AppRole authentication failed: {e}")

def store_api_key(user_id, api_key):
    encrypted_key = encrypt(api_key)
    token = get_vault_token()
    url = f"{VAULT_ADDR}/v1/{VAULT_SECRET_PATH}{user_id}"
    headers = {
        "X-Vault-Token": token
    }
    payload = {
        "data": {
            "encrypted_key": encrypted_key
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code not in [200, 204]:
        raise Exception(f"Failed to store secret in Vault: {response.text}")

def get_api_key(user_id):
    token = get_vault_token()
    url = f"{VAULT_ADDR}/v1/{VAULT_SECRET_PATH}{user_id}"
    headers = {
        "X-Vault-Token": token
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None
        data = response.json()
        encrypted_key = data["data"]["data"]["encrypted_key"]
        return decrypt(encrypted_key)
    except Exception as e:
        print(f"Error retrieving secret from Vault: {e}")
        return None

# Initialize Slack app
app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)

# Slash command to trigger setup
@app.command("/setup_osm")
def setup_osm_command(ack, body, client):
    ack()
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "osm_api_key_modal",
            "title": {"type": "plain_text", "text": "Connect to OSM"},
            "submit": {"type": "plain_text", "text": "Save"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "api_key_input",
                    "label": {"type": "plain_text", "text": "Enter your OSM API Key"},
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "osm_api_key",
                        "placeholder": {"type": "plain_text", "text": "e.g., abc123xyz..."},
                    },
                }
            ],
        },
    )

# Handle modal submission
@app.view("osm_api_key_modal")
def handle_view_submission(ack, body, view):
    ack()
    api_key = view["state"]["values"]["api_key_input"]["osm_api_key"]["value"]
    user_id = body["user"]["id"]
    store_api_key(user_id, api_key)
    print(f"Stored API key for user {user_id}")

if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
