param([string]$out)
$lines = [System.IO.File]::ReadAllLines($PSScriptRoot + "\_src_app.txt", [System.Text.Encoding]::UTF8)
[System.IO.File]::WriteAllLines($out, $lines, [System.Text.Encoding]::UTF8)
Write-Host "done"
