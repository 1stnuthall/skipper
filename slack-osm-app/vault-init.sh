#!/bin/bash

set -e

VAULT_ADDR=http://localhost:8200
ROLE_NAME=osm-app-role
POLICY_NAME=osm-api-policy
SECRET_PATH=secret/data/osm-api-keys/

echo "Checking Vault status..."
vault status || exit 1

echo "Initializing Vault..."
INIT_OUTPUT=$(vault operator init -format=json -key-shares=1 -key-threshold=1)
UNSEAL_KEY=$(echo "$INIT_OUTPUT" | jq -r '.unseal_keys_b64[0]')
ROOT_TOKEN=$(echo "$INIT_OUTPUT" | jq -r '.root_token')

echo "Unsealing Vault..."
vault operator unseal "$UNSEAL_KEY"

echo "Logging in with root token..."
export VAULT_TOKEN=$ROOT_TOKEN
vault login "$ROOT_TOKEN"

echo "Enabling AppRole..."
vault auth enable approle || echo "AppRole already enabled"

echo "Creating policy: $POLICY_NAME"
vault policy write $POLICY_NAME - <<EOF
path "$SECRET_PATH*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}
EOF

echo "Creating AppRole: $ROLE_NAME"
vault write auth/approle/role/$ROLE_NAME \
  token_policies="$POLICY_NAME" \
  token_ttl=1h \
  token_max_ttl=4h

ROLE_ID=$(vault read -field=role_id auth/approle/role/$ROLE_NAME/role-id)
SECRET_ID=$(vault write -field=secret_id -f auth/approle/role/$ROLE_NAME/secret-id)

echo "✅ Vault initialized and AppRole ready"
echo "VAULT_ROLE_ID=$ROLE_ID"
echo "VAULT_SECRET_ID=$SECRET_ID"
echo "🔐 Save these values in your .env file"
