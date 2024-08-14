$urlId = $args[0]
$url = $args[1].Trim() # Removes white\blank spaces from URLs...
$directoryName = $args[2]
$testName = $args[3].Trim()
$VMName = $args[4].Trim()
$time = [int]$args[5]

# Default Exception Action for Powershell...
$ErrorActionPreference = "SilentlyContinue"

# Formatting Testname...
$testName = "$VMName-$testName"

# Setting Environment Variables...
setx GOOGLE_API_KEY "no" | Out-Null
setx GOOGLE_DEFAULT_CLIENT_ID "no" | Out-Null
setx GOOGLE_DEFAULT_CLIENT_SECRET "no" | Out-Null

# Default Duration Set to 7 Seconds...
$defaultDuration = 7

# Default Duration if missing time value...
if ($time -eq 0) {
    $duration = $defaultDuration
}
else {
    $duration = $time
}

# Screen Record & Screenshot Duration Calulation..
$videoTimeout = $duration
$pcapTimeout = $duration
# $responseTimeout = $duration
$sleepDuration = $duration - 1

# $duration = [timespan]::fromseconds($duration)
# $duration = $duration.ToString("hh\:mm\:ss\.ff")

# Keystrokes Generation Object...
# $wshell = New-Object -ComObject wscript.shell;

# Timestamp, Count for Unique Identity of Files & Directories...
$urlId = [string]$urlId
$filename = "$testName-P$urlId"

$recordingPath = ".\results\$directoryName\recordings"
# $responsePath = ".\results\$directoryName\responses"
$screenshotPath = ".\results\$directoryName\screenshots"
$pcapPath = ".\results\$directoryName\packetcaptures"
# $malwarePath = ".\results\$directoryName\downloadedFiles"
$logPath = ".\results\$directoryName\$testName-logs.txt"

if ($url.Length -gt 0) {
    try {
        # Clear Console Screen
        # Clear-Host

        Write-Output "`n[ $VMName ] Testing Payload: $filename"

        "===============================================================" >> $logPath
        "Payload == $filename" >> $logPath
        "===============================================================" >> $logPath

        $navigationUrl = $url

        # "Response Generation Operation Started!!!" >> $logPath
        # (.\scripts\response.ps1 "$responsePath" "$filename" "$navigationUrl" "$responseTimeout" &) | Out-Null

        "Packet Capture Operation Started!!!" >> $logPath
        (.\scripts\packetcapture.ps1 1 "$pcapPath" "$filename" $pcapTimeout &) | Out-Null

        # Timer Started for URL Navigation...
        $timer = [Diagnostics.Stopwatch]::StartNew()

        # Browser Initialization in Incognito Mode... 
        & .\dependencies\chromium\chrome.exe --incognito --new-window --start-maximized
        
        "Screen Recording Operation Started!!!" >> $logPath
        "---------------------------------------------------------------" >> $logPath
        "                       Recording Log" >> $logPath
        "---------------------------------------------------------------" >> $logPath
        
        $recordFilename = "$recordingPath\$filename.ts"
        Start-Sleep 1.5
        Start-Process pwsh ".\scripts\record.ps1 $videoTimeout $recordFilename" -NoNewWindow

        "Browser Navigating to: $url" >> $logPath
        Start-Sleep 2
        & .\dependencies\chromium\chrome.exe --incognito --start-maximized --new-tab $navigationUrl

        Start-Sleep $sleepDuration

        # # Screenshot Operation Using Browser Title...
        # # FFMPEG Window Title Grab Operation For Screenshot...
        # $titleTimer = [Diagnostics.Stopwatch]::StartNew()
        # $titleFlag = $False
        # while ($titleTimer.Elapsed.TotalSeconds -lt 3) {
        #     $titleObjects = (Get-Process -Name chrome | Select-Object MainWindowTitle).'MainWindowTitle'
        #     ForEach ($value in $titleObjects) {
        #         if ($value.Length -ne 0) {
        #             $title = $value
        #             $titleFlag = $True
        #             break
        #         }
        #     }
        #     if ($titleFlag) {
        #         break
        #     }
        # }
        # $titleTimer.Stop()
        # $titleTimer.Reset()
        # $ffmpegTitle = "title=$title"

        # # Screenshot Operation...
        # "Screenshot Operation Started!!!" >> $logPath
        # & .\dependencies\ffmpeg\bin\ffmpeg.exe -f gdigrab -i $ffmpegTitle -framerate 1 -s hd1080 -loglevel error -vframes 1 $screenshotPath\$filename.jpeg 2>> $logPath

        # Screenshot Operation Using Desktop...
        "Screenshot Operation Started!!!" >> $logPath
        & .\dependencies\ffmpeg\bin\ffmpeg.exe -f gdigrab -i desktop -framerate 1 -s hd1080 -loglevel error -vframes 1 $screenshotPath\$filename.jpeg 2>> $logPath
        
        $timer.Stop()
        $urlNavTime = $timer.'Elapsed'.ToString("hh\:mm\:ss\.ff")
        
        Get-Process chrome | ForEach-Object { $_.CloseMainWindow() | Out-Null }

        if ((Get-Process chrome | Measure-Object).count -gt 0) {
            Get-Process chrome | Stop-Process -Force
        }

        # # Download File Handling Operations...
        # if (((Get-ChildItem ".\tempDownloadFolder\*" | Measure-Object).count -ne 0)) {
        #     $dName = (Get-ChildItem ".\tempDownloadFolder\*" | Select-Object 'Name').Name
        #     $downloadFileExtension = [System.IO.Path]:: GetExtension($dName)

        #     # Rename & Move Operation for Downloaded Files...
        #     $renameValue = "$filename-$downloadFileExtension"
        #     Get-ChildItem ".\tempDownloadFolder\*" | Rename-Item -NewName "$renameValue"
        #     Move-Item -Path ".\tempDownloadFolder\*" -Destination "$malwarePath"
        # }

        "---------------------------------------------------------------" >> $logPath
        "URL NAVIGATION TIME:: $urlNavTime" >> $logPath
        # "File Check Operation Started!!!" >> $logPath
        # # File Check for Recording...
        # if (Test-Path -Path "$recordingPath\$filename.mp4") {
        #     "Screen Recorded Successfully & File Exists!!!" >> $logPath
        # }
        # else {
        #     "--ERROR--Screen Recording File is Missing!!!" >> $logPath
        # }

        # # File Check for Screenshot...
        # if (Test-Path -Path "$screenshotPath\$filename.jpeg") {
        #     "Screenshot Taken & File Exists!!!" >> $logPath
        # }
        # else {
        #     "--ERROR--Screenshot File is Missing!!!" >> $logPath
        # }

        # # File Check for Packet Capture...
        # if (Test-Path -Path "$pcapPath\$filename.pcap") {
        #     "Packet Captured Successfully & File Exists!!!`n" >> $logPath
        # }
        # else {
        #     "--ERROR--PCAP File is Missing!!!`n" >> $logPath
        # }

        Write-Output "Test Completed For : $filename"
        "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" >> $logPath

        Exit
    }
    catch {
        "--ERROR--Exception Caught For $url" >> $logPath
        "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" >> $logPath
        Exit
    }
}

# Clear Console Screen
# Clear-Host