# Browser Automation using Powershell & FFMPEG [ V2.1 (Desktop) ]

<h4 align='center'>This Project is only for Educational Purposes. Malwares are harmful & can create Security Risks.</h4>
<h3 align='center'>Use At Your OWN RISK!!!</h3>
<br>

(o) Objective:

- To Download MALWARE files from URLs listed in a .txt file via Powershell.
- To Record Screen & Capture Screenshots of the entire activity.
- Capture Header Responses as Logs for each URLs.

(o) Done:

- Added MALWARE Download functionality after browser navigation to URL.
- Added Screen Record & Screenshot Functionality.
- Record Header Responses in './responses/' based on timestamps.
- Added Packet Capture Functionality for every URL.
- Added MD5 & SHA256 Hash Value Generation functionality for Downloaded Files.
<h3 align='center'>ENVIRONMENT VARIABLES & PATH</h3>
<h4 align='center'>FFMPEG: "C:\ffmpeg\bin\"</h4>
<h4 align='center'>Google Chrome: "C:\Program Files\Google\Chrome\Application\"</h4>
<h5 align='center'>Set Google Chrome Download Path As: "..\navigator\tempDownloadFolder"</h5>
<h4 align='center'>TSHARK: "C:\Program Files\Wireshark\"</h4>
(o) Pre-requisites:

FFMPEG

```
https://ffmpeg.org/download.html [ Guide :: https://www.wikihow.com/Install-FFmpeg-on-Windows ]
```

POWERSHELL >= v7.0

```
https://learn.microsoft.com/en-us/powershell/
```

Note: If you're running the script for the first time, do the following steps once.

1. Execute run-me-first.ps1
2. Execute dependencies.exe located at dependencies/dependencies.exe

To Execute the Script

```shell
> python driver.py <testName> [Enter]
```
