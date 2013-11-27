## CexControl
### Description
CexControl is a simple utility script to manage mining reinvestments on Cex.IO, simply put, it takes the full profit from BTC and NMC minig and automatically uses that to buy more GHS.

This is Beta software. Use at your own risk.

### Installation
Put all the files in a user writeable directory. 

### User guide
#### To start
Run the script on a commandline, ie, "python ./CexControl.py"
The script will detect if there is a configuration file or not, and prompt for user input if not.

#### To configre
To create a new configuration, start with "python ./CexControl.py newconfig", this will delete the existing configuration.

### Features
The script will run and check every 5 minutes if there are more then 0.0001 BTC or NMC available. 

If that is the case, the script will retrieve both Bid and Ask prices and average those in a on order spending as close to maximum as possible. If those orders are not fulfilled within 5 minutes, they will be canceled and new orders put in.

### Version history
#### Version 0.4.5
- Introduced trade NMC to BTC to GHS or NMC to GHS optimization
- General code improvements

#### Version 0.3.4
- Added more error handling.
- Added configuration by script.
- Added newconfig argument

#### Version 0.3.2
- Initial version pushed to GitHub.

