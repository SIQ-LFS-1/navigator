$directoryName = $args[0]

# Directory Generation...
if (!(Test-Path -Path ".\results")) {
    New-Item ".\results" -itemType Directory | Out-Null
}

if (!(Test-Path -Path ".\uploadables")) {
    New-Item ".\uploadables" -itemType Directory | Out-Null
}

if (!(Test-Path -Path ".\BACKUP")) {
    New-Item ".\BACKUP" -itemType Directory | Out-Null
}

if (Test-Path -Path ".\tempDownloadFolder") {
    Remove-Item ".\tempDownloadFolder" -Recurse -Force | Out-Null
    New-Item ".\tempDownloadFolder" -itemType Directory | Out-Null
}
else {
    New-Item ".\tempDownloadFolder" -itemType Directory | Out-Null 
}

New-Item ".\results\$directoryName" -itemType Directory | Out-Null
New-Item ".\results\$directoryName\recordings" -itemType Directory | Out-Null
# New-Item ".\results\$directoryName\responses" -itemType Directory | Out-Null
New-Item ".\results\$directoryName\screenshots" -itemType Directory | Out-Null
New-Item ".\results\$directoryName\packetcaptures" -itemType Directory | Out-Null
New-Item ".\results\$directoryName\downloadedFiles" -itemType Directory | Out-Null