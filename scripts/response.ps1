$responsePath = $args[0]
$filename = $args[1]
$url = $args[2]
$duration = $args[3]

$response = Invoke-WebRequest $url -TimeoutSec $duration

# Check flags
$arFlag = $response.Headers.'Accept-Ranges' -and $response.Headers.'Accept-Ranges' -notcontains 'none'
$ctFlag = $response.Headers.'Content-Type' -and $response.Headers.'Content-Type'[0] -notmatch 'text'
$cdFlag = $response.Headers.'Content-Disposition'

# Construct response object
$responseObj = $response | Select-Object -Property StatusCode, StatusDescription, RawContent, Headers
$responseObj | Add-Member -Type NoteProperty -Name 'url' -Value $url

# Check if the response is downloadable
$downloadable = ($arFlag -or $cdFlag -or $ctFlag) ? 'True' : 'False'
$responseObj | Add-Member -Type NoteProperty -Name 'Downloadable' -Value $downloadable

# Save the response object to a JSON file
$jsonfile = Join-Path $responsePath "$filename.json"
$responseObj | ConvertTo-Json | Set-Content $jsonfile