#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8000}"

curl -s "${BASE_URL}/health" | jq

USER=$(curl -s -X POST "${BASE_URL}/auth/signup" \
  -H 'Content-Type: application/json' \
  -d @examples/signup.json)

USER_ID=$(echo "$USER" | jq -r '.id')

echo "User ID: $USER_ID"

curl -s -X POST "${BASE_URL}/auth/login" \
  -H 'Content-Type: application/json' \
  -d @examples/login.json | jq

PRODUCT=$(curl -s -X POST "${BASE_URL}/products" \
  -H 'Content-Type: application/json' \
  -d @examples/product.json)

PRODUCT_ID=$(echo "$PRODUCT" | jq -r '.id')

echo "Product ID: $PRODUCT_ID"

ORDER=$(jq --arg user "$USER_ID" --arg product "$PRODUCT_ID" \
  '.user_id=$user | .items[0].product_id=$product' examples/order.json)

echo "$ORDER" > /tmp/order.json

curl -s -X POST "${BASE_URL}/orders" \
  -H 'Content-Type: application/json' \
  -d @/tmp/order.json | jq

curl -s "${BASE_URL}/recommendations/${USER_ID}" | jq
