try {
    Write-Output "`n--UPLOAD OPERATION STARTED--"
    $uploadNature = [string]$args[0]
    $directory = [string]$args[1]
    rclone copy --stats 5s --create-empty-src-dirs --transfers 20 --stats-log-level NOTICE C:\Users\secureiqlab\Documents\navigator\uploadables\ ctrl:2023-ACFW-PUBLIC/$uploadNature/$directory/ --log-file "C:\Users\secureiqlab\Documents\navigator\rclone.log"
    Write-Output "`n--Upload Operation Completed-->> DONE"

    # Moving Successful Results to BACKUP
    Move-Item -Force C:\Users\secureiqlab\Documents\navigator\uploadables\* C:\Users\secureiqlab\Documents\navigator\BACKUP\
}
catch [System.Exception] {
    Write-Output "`n--ERROR--$_"
}