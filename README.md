# Navigator POC

## Table of Contents

- [Navigator POC - Automation Tool](#navigator-poc---automation-tool)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Purpose of the Tool](#purpose-of-the-tool)
  - [Environment](#environment)
  - [Dependencies](#dependencies)
  - [Technologies Used](#technologies-used)
  - [Dependencies](#dependencies-1)
  - [Usage](#usage)
    - [Using Arguments](#using-arguments)
    - [Without Arguments](#without-arguments)
  - [Workflow](#workflow)
  - [Execution Flow](#execution-flow)
    - [Driver Script (`driver.py`)](#driver-script-driverpy)
    - [Navigator Script (`navigator.ps1`)](#navigator-script-navigatorps1)
    - [Directory Generation Script (`directorygeneration.ps1`)](#directory-generation-script-directorygenerationps1)
    - [Hash Check Script (`hashCheck.py`)](#hash-check-script-hashcheckpy)
  - [Additional Notes](#additional-notes)
    - [Example `VMName.json` File](#example-vmnamejson-file)
    - [Example `rules.json` File](#example-rulesjson-file)
    - [Example `urls-1.txt` and `urls-2.txt` Files](#example-urls-1txt-and-urls-2txt-files)
  - [Author](#author)

## Introduction

The `Navigator` tool is a Python and PowerShell-based automation framework designed for executing web navigation tasks, capturing screen recordings, network packets, and handling downloaded files across multiple virtual machine (VM) environments.

## Purpose of the Tool

This tool is used to automate the process of navigating a list of URLs, capturing relevant data (such as screenshots, network traffic, and downloaded files), and storing this data in a structured directory format for further analysis. It is particularly useful for testing environments where multiple VMs are used to replicate user behavior and network interactions.

## Environment

The tool is designed to run in a Windows environment with the following requirements.

## Dependencies

- Windows 10 or later
- Python 3.x
- PowerShell 7.x or later
- [Ungoogled Chromium Web Browser](https://ungoogled-software.github.io/ungoogled-chromium-binaries/) (Installed in the specified `dependencies` directory)
- Sufficient disk space for storing large volumes of captured data.

## Technologies Used

- **Python**: Core scripting and automation tasks.
- **PowerShell**: System operations and interaction with the Windows environment.
- **FFmpeg**: For screen recording and screenshot capture.
- **Wireshark/Dumpcap**: For packet capture.
- **Google Chrome**: For web navigation.

## Dependencies

Before using the tool, ensure the following dependencies are installed and configured:

1. **Python Packages**: None required specifically by the tool.
2. **PowerShell Modules**: Included within the project directory.
3. **FFmpeg**: Download and place in the `dependencies\ffmpeg\bin\` directory.
4. **Wireshark**: Ensure `dumpcap.exe` is accessible from the system PATH.
5. **Rclone**: Ensure `rclone.exe` is accessible from the system PATH and is properly configured to perform file upload to a remote storage like control server or Google drive.

## Usage

### Using Arguments

To run the tool, you must provide a test name as a command-line argument:

```bash
python driver.py <TestName>

Example: python driver.py T01-B01-I01-TEST-AR
```
This will initiate the tool with the provided test name, generating directories and handling the subsequent tasks accordingly.

### Without Arguments

If no arguments are provided, the tool will not execute and will return an error:

```bash
--ERROR--TESTNAME IS REQUIRED
```

## Workflow

1. **Environment Preparation**: The script sets up the required environment by determining the VM and IP configurations.
2. **Directory Generation**: A unique directory is generated for each test to store results.
3. **Rule Application**: Rules are applied based on predefined criteria.
4. **URL Navigation**: Each URL is navigated, and the relevant data is captured.
5. **Data Handling**: Screenshots, packet captures, and downloaded files are stored in the respective directories.
6. **Post-Processing**: Data is processed, hashed, and prepared for upload.

## Execution Flow

### Driver Script (`driver.py`)

- **Purpose**: The main orchestrator script that handles the entire workflow from environment setup to post-processing.
- **Key Functions**:
  - **Directory Generation**: Calls PowerShell script `directorygeneration.ps1` to create necessary folders.
  - **URL Navigation**: Uses the `navigator.ps1` script to navigate URLs and capture data.
  - **Process Management**: Kills unnecessary processes to prevent resource conflicts.
  - **File Handling**: Manages renaming and moving downloaded files.

### Navigator Script (`navigator.ps1`)

- **Purpose**: Handles the web navigation tasks, including opening URLs, capturing screenshots, and recording screen activity.
- **Key Features**:
  - **Browser Control**: Launches Chrome in incognito mode for each URL.
  - **Screen Recording**: Initiates screen recording using FFmpeg.
  - **Packet Capture**: Starts capturing network packets using Wireshark/Dumpcap.
  - **Screenshot Capture**: Captures screenshots at specific intervals.
  - **Error Handling**: Logs any navigation or capture errors.

### Directory Generation Script (`directorygeneration.ps1`)

- **Purpose**: Creates the necessary directory structure for storing results, ensuring all folders are correctly set up before the test begins.
- **Key Directories**:
  - `recordings`
  - `screenshots`
  - `packetcaptures`
  - `downloadedFiles`

### Hash Check Script (`hashCheck.py`)

- **Purpose**: Generates hash values (MD5 and SHA256) for URLs and downloaded files, ensuring data integrity and allowing for subsequent verification.
- **Key Functions**:
  - **File Hashing**: Calculates hash values for downloaded files.
  - **URL Hashing**: Generates hash values based on the URL content.
  - **Process Management**: Kills unnecessary processes before hashing to avoid conflicts.

## Additional Notes

### Example `VMName.json` File

This file should contain a list of VMs with their corresponding IP addresses and names:

```json
[
  {
    "name": "VM1",
    "ip": ["172.16.0.11", "172.16.0.21"]
  },
  {
    "name": "VM2",
    "ip": ["172.16.0.12", "172.16.0.22"]
  }
]
```

### Example `rules.json` File

Defines the rules applied during the execution:

```json
{
  "rules": [
    {
      "name": "Rule1",
      "testID": ["Test1", "Test2"],
      "status": true,
      "duration": 10,
      "timeout": 30,
      "split-urls": true
    }
  ]
}
```

### Example `urls-1.txt` and `urls-2.txt` Files

These files contain the URLs to be navigated by each VM:

```text
http://example.com
https://testsite.com
```

---

## Author
[Aayush Rajthala](https://github.com/AayushRajthala99)
