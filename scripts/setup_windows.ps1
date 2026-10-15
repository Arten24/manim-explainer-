# Run from a Miniforge-enabled PowerShell. Creates a NEW dedicated environment.
[CmdletBinding()]
param([ValidatePattern('^[a-zA-Z0-9_-]+$')][string]$Name = 'quonitron-manim-render')
$ErrorActionPreference = 'Stop'
$Repo = Split-Path -Parent $PSScriptRoot
if (-not (Get-Command conda -ErrorAction SilentlyContinue)) {
    throw 'Conda not found. Install Windows x86-64 Miniforge and open its prompt first.'
}
function Invoke-Conda {
    & conda @args
    if ($LASTEXITCODE -ne 0) { throw "Conda command failed (exit $LASTEXITCODE): $args" }
}
$EnvJson = & conda env list --json
if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect existing Conda environments.' }
$Existing = ($EnvJson | ConvertFrom-Json).envs
foreach ($Path in $Existing) {
    if ((Split-Path -Leaf $Path) -eq $Name) {
        throw "Environment '$Name' already exists. It was NOT modified. Verify it manually or choose -Name with a fresh name."
    }
}
Invoke-Conda env create --name $Name --file (Join-Path $Repo 'environment.windows.yml')
# Compiled/Python dependencies stay Conda-managed; only this project is editable.
Invoke-Conda run --no-capture-output -n $Name python -m pip install --no-deps --no-build-isolation -e $Repo
# Do not overwrite an existing user kernelspec with the same name.
$KernelJson = & conda run -n $Name jupyter kernelspec list --json
if ($LASTEXITCODE -ne 0) { throw 'Could not inspect Jupyter kernels.' }
$Kernels = ($KernelJson | ConvertFrom-Json).kernelspecs
if ($Kernels.PSObject.Properties.Name -contains $Name) {
    throw "Kernelspec '$Name' already exists and was NOT overwritten. Select the environment interpreter in VS Code, or choose a different kernel name manually."
}
Invoke-Conda run --no-capture-output -n $Name python -m ipykernel install --user --name $Name --display-name "QUONITRON Manim ($Name)"
Push-Location $Repo
try {
    Invoke-Conda run --no-capture-output -n $Name python scripts/verify_environment.py --json media/environment-setup/windows-diagnostics.json
    Invoke-Conda run --no-capture-output -n $Name python scripts/verify_renders.py --only minimal themed
} finally {
    Pop-Location
}
Write-Host "Setup AND smoke renders passed. Select 'QUONITRON Manim ($Name)' in VS Code."
Write-Host 'This does not certify Windows inline playback or visual layout. Open notebooks/environment_render_test.ipynb next.'
