"""
Created: 2020/20/02
Last modified at least: 2022/10/17
Author: Josh Budlender (jbudlender@umass.edu)

This script reads in Stats SA's historic CPI tables and saves into CSV format
Very rough-and-ready and I'm a Python novice -- improvements welcome!
"""

# Load packages
import os
import time
import camelot
from selenium import webdriver

# Working directory
wd = os.getcwd()

# Set up webdriver
chromedriver = 'C:\\myprograms\\chromedriver_win32\\chromedriver'

os.environ["webdriver.chrome.driver"] = chromedriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
prefs = {"profile.default_content_settings.popups": 0,
         "download.default_directory": wd,
         "download.prompt_for_download": False,
         "directory_upgrade": True,
         "plugins.always_open_pdf_externally": True}
options.add_experimental_option("prefs", prefs)

# Check webdriver is working
print(" ")
print("Starting webdriver")
try:
    driver = webdriver.Chrome(chromedriver, options=options)
except Exception:
    raise
else:
    print('Webdriver succesfully initiated')

# Remove historic CPI pdf if it already exists
print(" ")
try:
    os.remove("CPIhistory.pdf")
except Exception:
    if os.path.exists("CPIhistory.pdf"):
        raise
    print('No pre-existing CPIhistory.pdf in wd')
else:
    print('Pre-existing CPIhistory.pdf removed')

# Download historic CPI pdf
print(" ")
print("Starting CPI download")
# driver = webdriver.Chrome(chromedriver, options=options)
url_cpi = 'http://www.statssa.gov.za/publications/P0141/CPIHistory.pdf?'
driver.get(url_cpi)

# Sleep until download is done
i = 0
downloaded = os.path.exists("CPIhistory.pdf")
while downloaded is False and i < 10:
    time.sleep(2)
    i = i + 1
    print(str(2*i) + " seconds elapsed waiting for download")
    downloaded = os.path.exists("CPIhistory.pdf")
    print("CPIhistory downloaded? " + str(downloaded))

if downloaded is False and i == 10:
    print("Download timed out")

# Clean up
driver.close()

# Extract tables
print(" ")
print("Beginning table parsing")
time.sleep(2)
cpitables = camelot.read_pdf('CPIhistory.pdf', pages='1,2,3')

indexdf = cpitables[0].df

ratesdf1 = cpitables[1].df
ratesdf2 = cpitables[2].df
ratesdf = ratesdf1.append(ratesdf2[1:])

# Export as CSV
print(" ")
print("Beginning table export")
export_csv = indexdf.to_csv(r'cpi_index.csv', index=None, header=None)
export_csv = ratesdf.to_csv(r'cpi_rates.csv', index=None, header=None)

print(" ")
print("Done")
