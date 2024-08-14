$pcapFLag = $args[0]
$packetcapturePath = $args[1]
$filename = $args[2]
$duration = $args[3]

if ($pcapFLag -eq 1) {
    $pcapFilePath = "$packetcapturePath\$filename.pcap"
    & .\dependencies\wireshark\tshark.exe -i TRAFFIC -f "not(port 22 or port 3389)" -q -w $pcapFilePath -a duration:$duration
}

if ($pcapFLag -eq 0) {
    Out-Null | Stop-Process -Name dumpcap -Force
    Get-Job | Stop-Job
    Remove-Job *
}