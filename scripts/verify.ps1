$ErrorActionPreference = "Stop"

python -m compileall -q app tests
python -m pytest
Write-Output "Verification passed."
