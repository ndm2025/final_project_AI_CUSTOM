# Test.ps1 - Validacion CAG (PowerShell)
Write-Output "Running CAG validation tests."
Write-Output "If these fail, the CAG integration is incomplete or does not match the expected API contract."
$env:PYTHONPATH = "."
python -m unittest discover -s tests/validation -p "test_*.py"
