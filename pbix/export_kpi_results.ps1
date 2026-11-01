# Export KPI results from an already-open, refreshed RetailSales project.
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$package = Get-AppxPackage -Name Microsoft.MicrosoftPowerBIDesktop -ErrorAction SilentlyContinue
$bin = if ($package) { Join-Path $package.InstallLocation 'bin' } else { 'C:\Program Files\Microsoft Power BI Desktop\bin' }
$sourceLibrary = Join-Path $bin 'Microsoft.PowerBI.AdomdClient.dll'
if (-not (Test-Path -LiteralPath $sourceLibrary)) { throw 'Power BI Desktop ADOMD library not found. Open the project in an installed Power BI Desktop first.' }
$libraryDir = Join-Path ([System.IO.Path]::GetTempPath()) 'RetailSales-KpiVerification'
New-Item -ItemType Directory -Path $libraryDir -Force | Out-Null
$libraryCopy = Join-Path $libraryDir 'Microsoft.PowerBI.AdomdClient.dll'
Copy-Item -LiteralPath $sourceLibrary -Destination $libraryCopy -Force
$null = [System.Reflection.Assembly]::LoadFrom($libraryCopy)
$workspaceRoots = @(
    (Join-Path $env:USERPROFILE 'Microsoft\Power BI Desktop Store App\AnalysisServicesWorkspaces'),
    (Join-Path $env:LOCALAPPDATA 'Microsoft\Power BI Desktop\AnalysisServicesWorkspaces')
) | Where-Object { Test-Path -LiteralPath $_ }
$portFiles = @(Get-ChildItem -LiteralPath $workspaceRoots -Filter msmdsrv.port.txt -Recurse | Sort-Object LastWriteTime -Descending)
$selectedConnection = $null
foreach ($portFile in $portFiles) {
    $enginePort = (Get-Content -LiteralPath $portFile.FullName -Encoding Unicode -Raw).Trim()
    $connection = [Microsoft.AnalysisServices.AdomdClient.AdomdConnection]::new("Data Source=localhost:$enginePort")
    try {
        $connection.Open()
        $command = $connection.CreateCommand()
        $command.CommandText = 'EVALUATE ROW("Orders", [Total Orders], "YoY", [Sales YoY %])'
        $reader = $command.ExecuteReader()
        $valid = $reader.Read() -and $reader.GetValue(0) -eq 5009
        $reader.Close()
        if ($valid) {
            $selectedConnection = $connection
            Write-Output "Selected verified RetailSales engine on port $enginePort"
            break
        }
    } catch {
        Write-Output "Skipped engine $enginePort because it does not contain the validated current model"
    }
    $connection.Dispose()
}
if (-not $selectedConnection) { throw 'No refreshed RetailSales model with valid DAX found' }
try {
    $command = $selectedConnection.CreateCommand()
    $command.CommandText = Get-Content -LiteralPath (Join-Path $repo 'pbix\validate_kpis.dax') -Raw
    $reader = $command.ExecuteReader()
    $results = [System.Collections.Generic.List[object]]::new()
    while ($reader.Read()) {
        $record = [ordered]@{}
        for ($i=0; $i -lt $reader.FieldCount; $i++) {
            $name = $reader.GetName($i) -replace '^\[|\]$',''
            $record[$name] = if ($reader.IsDBNull($i)) { $null } else { $reader.GetValue($i) }
        }
        $results.Add([pscustomobject]$record)
    }
    $reader.Close()
    ConvertTo-Json -InputObject $results.ToArray() -Depth 10 | Set-Content -LiteralPath (Join-Path $repo 'docs\kpi_powerbi_actual.json') -Encoding utf8
    $command.CommandText = 'EVALUATE ROW("Zero denominator is blank", ISBLANK(DIVIDE(100,0)), "Zero numerator stays zero", DIVIDE(0,100)=0)'
    $reader = $command.ExecuteReader()
    while ($reader.Read()) {
        for ($i=0; $i -lt $reader.FieldCount; $i++) {
            Write-Output "$($reader.GetName($i)): $($reader.GetValue($i))"
            if (-not $reader.GetValue($i)) { throw 'DIVIDE edge case failed' }
        }
    }
    $reader.Close()
} finally { $selectedConnection.Dispose() }
