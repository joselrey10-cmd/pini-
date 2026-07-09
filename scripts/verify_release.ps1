$ErrorActionPreference = "Stop"

$root = Split-Path $PSScriptRoot -Parent
Set-Location $root

$env:PYTHONPATH=".;apps\desktop"

python -m pytest -q