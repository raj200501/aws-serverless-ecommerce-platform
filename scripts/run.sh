#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="${ROOT_DIR}/src"

ENV_FILE="${ENV_FILE:-.env}"
if [[ -f "${ROOT_DIR}/${ENV_FILE}" ]]; then
  export $(grep -v '^#' "${ROOT_DIR}/${ENV_FILE}" | xargs)
fi

python -m ecommerce_platform.cli init-db

if [[ "${SEED_DEMO:-true}" == "true" ]]; then
  python -m ecommerce_platform.cli seed
fi

exec python -m ecommerce_platform.server
