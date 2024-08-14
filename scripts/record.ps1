$duration = [int]$args[0]
$filename = $args[1]

# Screen Record using Browser Title...
# Start-Process ".\dependencies\ffmpeg\bin\ffmpeg.exe" -ArgumentList @('-f', 'gdigrab', '-i', 'title="New Incognito Tab - Chromium"', '-framerate', 10, '-s', 'hd1080', '-loglevel', 'error', '-t', $duration, "$filename") -NoNewWindow

# Screen Record using Desktop...
Start-Process ".\dependencies\ffmpeg\bin\ffmpeg.exe" -ArgumentList @('-f', 'gdigrab', '-i', 'desktop', '-framerate', 24, '-loglevel', 'error', "-c:v", "libx264", "-preset", "fast", '-t', $duration, "$filename") -NoNewWindow

Exit