# Stack Overflow Enterprise Search Logs
A Python script for Stack Overflow Enterprise that creates a report (CSV file) of search history from users. You can see an [example](https://github.com/jklick-so/soe_search_logs/blob/main/Examples/search_logs.csv) of what the output looks like in the Examples directory.

## Requirements
* Stack Overflow Enterprise and a user account with admin permissions
* Python 3.8 or higher ([download](https://www.python.org/downloads/))
* Operating system: Linux, MacOS, or Windows
* Chrome browser

## Setup
[Download](https://github.com/jklick-so/soe_search_logs/archive/refs/heads/main.zip) and unpack the contents of this repository

To install the required open source libraries for Python:
* Open a terminal window (or, for Windows, a command prompt)
* Navigate to the directory where you unpacked the files
* Install the dependencies: `pip3 install -r requirements.txt`

## Usage
In a terminal window, navigate to the directory where you unpacked the script. 
Run the script using the following format, replacing the URL with your own:

`python3 soe_search_logs.py --url "https://SUBDOMAIN.stackenterprise.co"`

At the beginning of the script, a small Chrome window will appear, prompting you to login to your instance of Stack Overflow Enterpise. After logging in, the Chrome window will disappear and the script will proceed in the terminal window.

The script typically takes less than a minute to run. As it runs, it will continue to update the terminal window with the status. When the script completes, it will indicate the the CSV has been exported, along with the name of file. You can see an [example](https://github.com/jklick-so/soe_search_logs/blob/main/Examples/search_logs.csv) of what the output looks like in the Examples directory.

## Support, security, and legal
Disclaimer: the creator of this project works at Stack Overflow, but it is a labor of love that comes with no formal support from Stack Overflow. 

If you run into issues using the script, please [open an issue](https://github.com/jklick-so/soe_search_logs/issues). You are also welcome to edit the script to suit your needs, steal the code, or do whatever you want with it. It is provided as-is, with no warranty or guarantee of any kind. If the creator wasn't so lazy, there would likely be an MIT license file included.

All data is handled locally on the device from which the script is run. The script does not transmit data to other parties, such as Stack Overflow.
