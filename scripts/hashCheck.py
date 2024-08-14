import os
import re
import sys
import json
import socket
import psutil
import hashlib
from datetime import datetime
from os import path as directoryPath

# from pytz import timezone


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


def urlhashGeneration(url):
    md5hash = hashlib.md5(url.encode()).hexdigest()
    sha256hash = hashlib.sha256(url.encode()).hexdigest()
    return [md5hash, sha256hash]


def filehashGeneration(filename):
    with open(filename, "rb") as f:
        bytes = f.read()  # read entire file as bytes

        # Commented MD%HASH CALCULATION TO REDUCE CPU OVERHEAD
        # md5hash = hashlib.md5(bytes).hexdigest()
        md5hash = ""
        sha256hash = hashlib.sha256(bytes).hexdigest()
        return [md5hash, sha256hash]


def convert_bytes(size):
    """Convert bytes to KB, or MB or GB"""
    for x in ["bytes", "KB", "MB", "GB"]:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0


# Simplify ID extraction using a helper function
def get_id_from_test(testInfoList, prefixes, max_length=4):
    for value in testInfoList:
        if any(prefix in value for prefix in prefixes) and len(value) < max_length:
            return value
    return ""


# def utc_to_pst(time):
# utctime = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

# Create a PST timezone object
# pst_tz = timezone('US/Pacific')

# Localize the UTC datetime to PST
# pst_time = utctime.replace(tzinfo=timezone('UTC')).astimezone(pst_tz)
# pst_time = pst_time.strftime('%Y-%m-%d %H:%M:%S')

# return pst_time


killProcess()

if len(sys.argv) == 3:
    resultDirectory = sys.argv[1]
    testName = sys.argv[2]

    VMInfo = open(directoryPath.abspath("./credentials/VMName.txt"), "r")
    VMName = VMInfo.read().splitlines()
    if len(VMName) > 0:
        VMName = VMName[0]
    VMInfo.close()
    fullID = rf"{VMName}-{testName}"

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    # Using os.path.join for better path handling
    hashFileLocation = os.path.join(resultDirectory, "hashCheck.json")
    urlFileLocation = os.path.join(resultDirectory, "urls.txt")
    urlTimestampLocation = os.path.join(resultDirectory, "urlNavigationTimestamp.txt")
    malwareDirectory = os.path.join(resultDirectory, "downloadedFiles")
    # responseDirectory = os.path.join(resultDirectory, 'responses')

    # Simplify reading and cleaning up file content
    with open(urlFileLocation, "r") as file:
        urlList = [value.strip() for value in file if value.strip()]

    with open(urlTimestampLocation, "r") as file:
        urlTimestampList = [value.strip() for value in file if value.strip()]

    # Simplify file creation or overwriting
    if not os.path.isfile(hashFileLocation):
        with open(hashFileLocation, "w") as f:
            f.write("[]")

    # Always read the file content
    with open(hashFileLocation) as fp:
        obj = json.load(fp)

    # Getting ID Information from testName...
    testInfoList = testName.split("-")
    testID = get_id_from_test(testInfoList, ["T0", "T1"])
    batchID = get_id_from_test(testInfoList, ["B0"])
    iterationID = get_id_from_test(testInfoList, ["I0"])

    # List of files present in malware & response directory...
    malwareList = os.listdir(malwareDirectory)
    # responseList = os.listdir(responseDirectory)

    count = 1
    for i, url in enumerate(urlList):
        if len(url) != 0:
            payloadId = rf"P{str(count)}"
            filename = rf"{fullID}-{payloadId}"

            # Filenames for response files & downloaded files...
            # responseFilename = rf"{filename}.json"
            fileSearchName = re.escape(rf"{filename}-")

            # Get Status Code from Response Files...
            # responseStatusCode = "N/A"
            # responseFilePath = directoryPath.join(responseDirectory, responseFilename)

            # if responseFilename in responseList:
            #     with open(responseFilePath, encoding="utf8") as f:
            #         response = json.load(f)
            #         responseStatusCode = str(response["StatusCode"])
            #         f.close()

            # Template for URL Information...
            hashInfo = {
                "Date": rf"{urlTimestampList[i]}",
                "ID": fullID,
                "Test ID": testID,
                "Batch ID": batchID,
                "Iteration ID": iterationID,
                "Payload ID": payloadId,
                "URL": url,
                "Source IP": rf"{ip_address}",
                # "Response Code": rf"{responseStatusCode}",
                "Result": "",
                "Time To Detect": "",
                "Category": "",
                "Observation": "",
                "Screenshot Link": "",
                "Video Link": "",
                "PCAP Link": "",
                # "Response Link": "",
                # "URL MD5": 'N/A',
                # "URL Sha256": 'N/A',
                # "URL First Submission Date": "",
                # "URL Last Submission Date": "",
                # "URL Last Analysis Date": "",
                # "URL VT Score": "",
                # "Time Difference": "",
                "File Downloaded": None,
                "File Hash Match": "",
                "File Size Match": "",
                "Downloaded File Name": "",
                # "Downloaded File MD5": "",
                "Downloaded File Sha256": "",
                "Downloaded File Size": "",
                "File First Submission Date": "",
                "File Last Submission Date": "",
                "File Last Analysis Date": "",
                "File VT Score": "",
                "Baseline File Size": "",
                "Baseline File Sha256": "",
            }

            # Commented URL HASH CALCULATION TO REDUCE CPU OVERHEAD
            # urlHash = urlhashGeneration(url)
            # hashInfo["URL MD5"] = urlHash[0]
            # hashInfo["URL Sha256"] = urlHash[1]

            # Getting Filename.Extension if exists...
            fullFilename = next(
                (file for file in malwareList if re.search(fileSearchName, file)), None
            )

            if fullFilename:
                filePath = directoryPath.join(malwareDirectory, fullFilename)

                if directoryPath.isfile(filePath):
                    fileHash = filehashGeneration(filePath)
                    filesize = convert_bytes(directoryPath.getsize(filePath))

                    # Commented md5hash value assignment to reduce CPU OVERHEAD
                    hashInfo.update(
                        {
                            "File Downloaded": True,
                            "Downloaded File Name": fullFilename,
                            # "Downloaded File MD5": fileHash[0],
                            "Downloaded File Sha256": fileHash[1],
                            "Downloaded File Size": filesize,
                        }
                    )

                    if VMName == "BASE":
                        hashInfo.update(
                            {
                                "Baseline File Size": filesize,
                                "Baseline File Sha256": fileHash[1],
                            }
                        )
                else:
                    hashInfo["File Downloaded"] = False
            else:
                hashInfo["File Downloaded"] = False

            obj.append(hashInfo)
            count += 1

    with open(hashFileLocation, "w") as json_file:
        json.dump(obj, json_file, indent=2, separators=(",", ": "))

    # Python Script Call for hashCheck.json to urlInfo.csv ...
    os.system(rf"python scripts\jsontocsv.py {resultDirectory}")

else:
    print("Invalid Number of Arguments")
