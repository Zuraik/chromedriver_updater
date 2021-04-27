import requests
import sys
import os
import zipfile
import io
from bs4 import BeautifulSoup

def download_chrome_driver(version=None, path=None):
    """ Call this function to download one of the LATEST FOUR ChromeDriver versions.
    "version" parameter is the first 2 digits of the chrome version (example: 87)
    "path" parameter is to specify to download in a specific folder
    """
    if path is not None:
        os.chdir(path)
    driver_type = None
    if sys.platform == "linux":
        driver_type = "chromedriver_linux64.zip"
    elif sys.platform == "win32":
        driver_type = "chromedriver_win32.zip"
    if driver_type is None:
        print("Missing OS Type")
        return
    page = requests.get("https://chromedriver.chromium.org/downloads").content
    soup = BeautifulSoup(page, "html.parser")
    links = soup.select(".n8H08c.UVNKR li a[href]")
    version = version if version is not None else "latest"
    for link in links:        
        if str(link.text.split(" ")[1].split(".")[0]) == str(version) or version == "latest":
            print("Trying to download the new driver version: {}".format(version))
            download_link = "https://chromedriver.storage.googleapis.com/"
            download_link += link.text.split(" ")[1] + "/" + driver_type
            print("Downloading from {}".format(download_link))
            file_url = requests.get(download_link, stream=True)
            with open(driver_type, "wb") as wd:
                for chunk in file_url.iter_content(chunk_size=512):
                    wd.write(chunk)
            print("Unzipping file...")
            if sys.platform == "linux":
                zipfile.ZipFile(driver_type).extract("chromedriver")
            elif sys.platform == "win32":
                zipfile.ZipFile(driver_type).extract("chromedriver.exe")
            else:
                print("No known file to extract.")
            os.remove(driver_type)
            print("Removing zip...")
            if sys.platform == "linux":
                os.system("chmod +x {}".format("chromedriver"))
            return
    print("Unable to find a new driver for version {}".format(version))
