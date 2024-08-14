import os
import re
import sys
import json
import shutil
import psutil
import socket
import subprocess
from time import sleep
from datetime import datetime
from os import path as directoryPath

try:
    # Tool Arguments...
    testName = rf"{sys.argv[1]}"

except Exception as error:
    print("--ERROR--TESTNAME IS REQUIRED")
    exit()

# Parse Tool Pre-requisites...
navigatorScript = r"./navigator.ps1"
gitScript = r"../ACFW-DOWNLOADS/git.ps1"
directoryGenerationScript = r"./scripts/directorygeneration.ps1"

# Getting Host Information...
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# Regex Patterns...
VM1_pattern = r"^172\.16\.[0-9]{1,3}\.(?:11|21|201)$"
VM2_pattern = r"^172\.16\.[0-9]{1,3}\.(?:12|22|202|14)$"

# Getting VM Information...
VMInfo = open(directoryPath.abspath("./credentials/VMName.json"), "r")
VMInfoJson = json.load(VMInfo)
VMInfo.close()

# Getting Rules...
rules = open(directoryPath.abspath("./credentials/rules.json"), "r")
rulesJson = json.load(rules)
activeRules = [rule for rule in rulesJson["rules"] if rule["status"]]
rules.close()

print("\n[ HEADLESS-NAVIGATOR ] Developed By Aayush Rajthala!\n")


def getFullPath(pathValue):
    return os.path.normpath(os.path.abspath(pathValue))


def directoryGeneration(name, VMname):
    try:
        if VMname == "":
            return {"status": False, "error": "--ERROR--VM Name is Required!!!"}

        # Writing VMName to VMName.txt for navigator.ps1
        txtFile = open(directoryPath.abspath("./credentials/VMName.txt"), "w")
        txtFile.write(VMname)
        txtFile.close()

        currentdatetime = datetime.now().strftime("%b-%d-%Y-%HH-%Mm-%Ss")
        directoryName = rf"{VMname}-{str(name)}_{currentdatetime}"

        # Executing directorygeneration.ps1
        subprocess.run(["pwsh.exe", "-File", directoryGenerationScript, directoryName])

        # print("DIRECTORY NAME===", directoryName)
        return {"status": True, "name": str(directoryName)}

    except Exception as error:
        return {"status": False, "error": error}


def killProcess():
    for proc in psutil.process_iter(["name"]):
        try:
            if proc.info["name"] == "ffmpeg.exe":
                proc.terminate()
            if proc.info["name"] == "dumpcap.exe":
                proc.terminate()
            if proc.info["name"] == "chrome.exe":
                proc.terminate()

        except Exception as error:
            pass

    return


# Download File Handler...
def renameCopyFile(filename, directoryName):
    # Download File Handling Operations...
    temp_download_folder = "./tempDownloadFolder"
    malware_path = rf"./results/{directoryName}/downloadedFiles/"

    if len(os.listdir(temp_download_folder)) != 0:
        d_name = os.listdir(temp_download_folder)[0]
        download_file_extension = os.path.splitext(d_name)[1]

        # Rename & Move Operation for Downloaded Files...
        rename_value = rf"{filename}-{download_file_extension}"
        os.rename(
            os.path.join(temp_download_folder, d_name),
            os.path.join(temp_download_folder, rename_value),
        )
        shutil.move(os.path.join(temp_download_folder, rename_value), malware_path)

        shutil.rmtree(temp_download_folder)
        os.mkdir(temp_download_folder)
        return


def removeTempFolder():
    temp_download_folder = "./tempDownloadFolder"
    shutil.rmtree(temp_download_folder)
    os.mkdir(temp_download_folder)
    return


VMNumber = None
# For VM1 Instances...
if re.match(VM1_pattern, ip_address):
    VMNumber = 1

# For VM2 Instances...
elif re.match(VM2_pattern, ip_address):
    VMNumber = 2

if VMNumber is None:
    VMNumber = 1
    # print("--ERROR--[ REGEX MATCH FAILED ]")
    # exit()

# Appending VM ID in the Test Name...
testName = rf"{testName}-VM{VMNumber}"

# URLS Retrieve Operation...
urlFilePath = rf"./urls-{VMNumber}.txt"
urlFile = open(directoryPath.abspath(urlFilePath), "r", encoding="utf-8")
urlList = urlFile.read().splitlines()
urlList = [value for value in urlList if len(value.strip()) != 0]
urlFile.close()

urllistlength = len(urlList)

if urllistlength == 0:
    print("--ERROR--[ urls.txt ]--File is Empty!!!")
    exit()

try:
    # Getting VMName...
    VMName = ""
    for info in VMInfoJson:
        if ip_address in info["ip"]:
            VMName = info["name"]
            break

    if VMName == "":
        print("--ERROR--VMName is Required!!!")
        exit()

    # Default Test Variables...
    duration = 7
    timeout = 20
    splitUrl = False

    # Implementing Rules from rules.json ...
    ruleName = ""
    for rule in activeRules:
        if any(testID in testName for testID in rule["testID"]):
            ruleName = rule["name"]
            duration = rule["duration"]
            timeout = rule["timeout"]
            splitUrl = rule["split-urls"]
            break

    if ruleName == "":
        print("No Rules Applied")
    else:
        print(rf"--INFO--[ APPLIED RULE ]--[ {ruleName} ]")

    if splitUrl:
        halfValue = int(len(urlList) / 2)

        # For VM1 Instances...
        if VMNumber == 1:
            urlList = urlList[:halfValue]

        # For VM2 Instances...
        elif VMNumber == 2:
            urlList = urlList[halfValue:]

        # Open the file in write mode
        with open(urlFilePath, "w") as tempFile:
            # Iterate over the list and write each string to a new line in the file
            for string in urlList:
                tempFile.write(string + "\n")

            tempFile.close()

    generationStatus = directoryGeneration(testName, VMName)

    if generationStatus["status"]:
        killProcess()
        directoryName = generationStatus["name"]

        # URL NAVIGATION TIMESTAMP FILE GENERATION...
        File = open(
            getFullPath(f"./results/{directoryName}/urlNavigationTimestamp.txt"), "a+"
        )

        # URL NAVIGATION OPERATION...
        for urlId, url in enumerate(urlList):
            try:
                killProcess()
                removeTempFolder()

                urlId += 1
                urlNavigationTimestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                File.write(f"{urlNavigationTimestamp}\n")

                result = subprocess.run(
                    [
                        "pwsh.exe",
                        "-File",
                        navigatorScript,
                        str(urlId),
                        str(url),
                        str(directoryName),
                        str(testName),
                        str(VMName),
                        str(duration),
                    ],
                    timeout=timeout,
                )

            except subprocess.TimeoutExpired:
                if len(VMName) > 0:
                    print(
                        "--ERROR--NAVIGATION TIMEOUT FOR : ",
                        rf"{VMName}-{testName}-P{str(urlId)}",
                    )
                else:
                    print(
                        "--ERROR--NAVIGATION TIMEOUT FOR : ",
                        rf"{testName}-P{str(urlId)}",
                    )
                pass

            except Exception as error:
                if len(VMName) > 0:
                    print(
                        "--ERROR--EXCEPTION CAUGHT FOR : ",
                        rf"{VMName}-{testName}-P{str(urlId)}",
                        " : ",
                        error,
                    )
                else:
                    print(
                        "--ERROR--EXCEPTION CAUGHT FOR : ",
                        rf"{testName}-P{str(urlId)}",
                        " : ",
                        error,
                    )
                pass

            killProcess()

            try:
                # Download File Handling Operation...
                fileName = rf"{VMName}-{testName}-P{urlId}"
                renameCopyFile(fileName, directoryName)

            except Exception as error:
                pass

        File.close()
        killProcess()

        # RESULT FILES COPY OPERATION...
        shutil.copy(
            directoryPath.abspath(urlFilePath), rf"./results/{directoryName}/urls.txt"
        )

        # Script Call for hashCheck.py...
        os.system(rf"python scripts\hashCheck.py results\{directoryName} {testName}")
        print("---HASH CHECK OPERATION COMPLETED---")

        # hashCheck to urlInfo.csv Conversion...
        # os.system(rf"python scripts/jsontocsv.py results/{directoryName}/")

        # os.remove(directoryPath.abspath(
        #     rf"./results/{directoryName}/urlNavigationTimestamp.txt"))

        shutil.copytree(
            directoryPath.abspath(rf"./results/{directoryName}"),
            directoryPath.abspath(rf"./uploadables/{directoryName}"),
        )

        # Script Call for uploader.py...
        uploader_script = directoryPath.abspath("scripts/uploader.ps1")
        subprocess.run(["pwsh.exe", "-File", uploader_script, "VOLUMETRIC", VMName])

        # Downloaded File Inventory Operation...
        if directoryPath.exists(directoryPath.abspath(rf"../ACFW-DOWNLOADS")):
            if not (
                directoryPath.exists(directoryPath.abspath(rf"../ACFW-DOWNLOADS/Files"))
            ):
                os.mkdir(directoryPath.abspath(rf"../ACFW-DOWNLOADS/Files"))

            fileList = os.listdir(
                rf"{directoryPath.abspath(f'./results/{directoryName}/downloadedFiles/')}"
            )

            if len(fileList) > 0:
                os.makedirs(
                    directoryPath.abspath(rf"../ACFW-DOWNLOADS/Files/{directoryName}")
                )

                for file in fileList:
                    shutil.copy(
                        directoryPath.abspath(
                            rf"./results/{directoryName}/downloadedFiles/{file}"
                        ),
                        directoryPath.abspath(
                            rf"../ACFW-DOWNLOADS/Files/{directoryName}/"
                        ),
                    )
                subprocess.run(["pwsh.exe", "-File", gitScript, str(directoryName)])

        # Test Completed ASCII ART...
        print(
            "╔╦╗╔═╗╔═╗╔╦╗  ╔═╗╔═╗╔╦╗╔═╗╦  ╔═╗╔╦╗╔═╗╔╦╗\n ║ ║╣ ╚═╗ ║   ║  ║ ║║║║╠═╝║  ║╣  ║ ║╣  ║║\n ╩ ╚═╝╚═╝ ╩   ╚═╝╚═╝╩ ╩╩  ╩═╝╚═╝ ╩ ╚═╝═╩╝"
        )
        sleep(5)

    else:
        print(generationStatus["error"])
        raise Exception("--ERROR--DIRECTORY GENERATION FAILURE")

except Exception as error:
    print(error)
    killProcess()
    exit()
