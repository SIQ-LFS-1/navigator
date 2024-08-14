import psutil
import subprocess


def killProcess():
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] == 'ffmpeg.exe':
                proc.terminate()
            if proc.info['name'] == 'dumpcap.exe':
                proc.terminate()
            if proc.info['name'] == 'chrome.exe':
                proc.terminate()
            if proc.info['name'] == 'pwsh.exe':
                proc.terminate()
            if proc.info['name'] == 'powershell.exe':
                proc.terminate()

        except Exception as error:
            pass

    return


killProcess()
