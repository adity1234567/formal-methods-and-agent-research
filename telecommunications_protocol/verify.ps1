param([string]$Solver = 'glucose')

$ErrorActionPreference = 'Stop'
$runner = Join-Path $PSScriptRoot 'verify.py'
& python $runner --solver $Solver
exit $LASTEXITCODE
