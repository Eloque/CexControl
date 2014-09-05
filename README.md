## CexControl
### Description
CexControl is a simple utility script to manage mining reinvestments on Cex.IO, simply put, it takes the full profit from BTC and NMC minig and automatically uses that to buy more GHS. It has some nice features that calculate prices and try to optimize orders.
This is Beta software. Use at your own risk.

### Installation
Put all the files in a user writeable directory.

### User guide
#### To start
Run the script on a commandline, ie, "python ./CexControl.py".
Run the script on a commandline with trial flag to run in trial mode, ie, "python ./CexControl.py trial", no real trades will be performed.
The script will detect if there is a configuration file or not, and prompt for user input if not.

To find out what version you are running, run the script on a commandline with the argument parameter, ie, "python ./CexControl.py version"

#### To configure
To create a new configuration, start with "python ./CexControl.py newconfig", this will delete the existing configuration.
To just change the thresholds, start with "python ./CexControl.py setthreshold", this will prompt for new thresholds. Please fill in decimals.


### Features
The script will run and check every 5 minutes if there are more then 0.0001 BTC or NMC available.

If that is the case, the script will retrieve both Bid and Ask prices and average those in a on order spending as close to maximum as possible. If those orders are not fulfilled within 5 minutes, they will be canceled and new orders put in.

The script will log all it's output to file as well. It is recommended to rotate this file.

### Support & Donations
I code this for my own benefit as much as the communities. I firmly believe there should be more alternatives for every problem that software can tackle, so people have choice. Also I don't believe an idea, an algorithm or such can be owned. As such, this simple thing is opensource. If you do feel like tipping me, that can be done in a few different ways.

First of all, BitCoins: 1Lehv8uMSMyYyY7ZFTN1NiRj8X24E56rvV
You could also start using Cex.IO via my referral code: https://cex.io/r/1/Eloque/0/.
Vouchers via Cex.IO can of course also be used.

<img style="float:right" src="https://raw.github.com/Eloque/CexControl/master/donate.png" />

I will accept and appreciate every and all donations.

### Version history

#### Version 0.9.6
- Removed the NMC/GHS market, no longer offered on Cex.IO

#### Version 0.9.2
- Added LTC Trading

#### Version 0.9.1
- Added IXC Trading

#### Version 0.9.0
- Adjusted for 2% fee on trade to more suitable calculation
- Fixed bug with NMC trading not working
- Added Trial mode

#### Version 0.8.6
- Adjusted for 2% fee on trade

#### Version 0.7.2
- Fixed various logging errors

#### Version 0.7.1
- Added timestamp to logfile

#### Version 0.7.0
- Changed logging mechanism
- Added GUI hooks
- Added log to file

#### Version 0.6.6
- Added hold coins
- Fix for price, to round of to 7 decimals
- Fixed bug with empty API key and secret on new config

#### Version 0.6.5
- Added visual confirmation of settings

#### Version 0.6.4
- Added option to set thresholds
- Improved error handling
- Added settings object

#### Version 0.5.6
- Added arbitration threshold at 2.5%
- Improved error handling on first connect
- Function for PrintBalance

#### Version 0.5.4
- Cleaned up unused code
- Improved error handling
- Handle HTTP disconnects
- Changed Print function to account for Python3
- General code improvements

#### Version 0.4.12
- Improved trade functions, now calculate efficiency correctly
- Improved error handling
- Start GUI Hooks
- General code improvements

#### Version 0.4.5
- Introduced trade NMC to BTC to GHS or NMC to GHS optimization
- General code improvements

#### Version 0.3.4
- Added more error handling.
- Added configuration by script.
- Added newconfig argument

#### Version 0.3.2
- Initial version pushed to GitHub.

