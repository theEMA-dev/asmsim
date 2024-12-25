# Kill running instances
Get-Process asmsim -ErrorAction SilentlyContinue | Stop-Process -Force

# Clean with proper error handling
if (Test-Path "dist/asmsim.exe") {
    # Remove read-only attribute if present
    Set-ItemProperty "dist/asmsim.exe" -Name IsReadOnly -Value $false -ErrorAction SilentlyContinue
    Remove-Item "dist/asmsim.exe" -Force -ErrorAction SilentlyContinue
}

# Clean directories
Remove-Item -Recurse -Force .\build\, .\dist\ -ErrorAction SilentlyContinue

# Verify directory structure
if (!(Test-Path "ui")) { New-Item -ItemType Directory -Force -Path "ui" }
if (!(Test-Path "ui/assets")) { New-Item -ItemType Directory -Force -Path "ui/assets" }
if (!(Test-Path "builder")) { New-Item -ItemType Directory -Force -Path "builder" }

# Build with elevated permissions if needed
Start-Process python -ArgumentList "-m PyInstaller --clean asmsim.spec" -Wait -NoNewWindow