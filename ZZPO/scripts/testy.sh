#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -d ".venv" ]]; then
  echo "[INFO] Tworze lokalne srodowisko .venv"
  python3 -m venv .venv
fi

source .venv/bin/activate

echo "[INFO] Instalacja zaleznosci projektu"
python -m pip install -e ".[dev]"

echo "[INFO] Uruchamiam testy"
pytest -q
