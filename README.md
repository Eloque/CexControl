## CexControl
### Description
CexControl is a simple utility script to manage mining reinvestments on Cex.IO, simply put, it takes the full profit from BTC and NMC minig and automatically uses that to buy more GHS. It has some nice features that calculate prices and try to optimize orders.
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

### Support & Donations
I code this for my own benefit as much as the communities. I firmly believe there should be more alternatives for every problem that software can tackle, so people have choice. Also I don't believe an idea, an algorithm or such can be owned. As such, this simple thing is opensource. If you do feel like tipping me, that can be done in a few different ways.

First of all, BitCoins: 

1Lehv8uMSMyYyY7ZFTN1NiRj8X24E56rvV
<img style="float:right" src="https://raw.github.com/Eloque/CexControl/master/donate.png" />

You could also start using Cex.IO via my referral code: https://cex.io/r/1/Eloque/0/.
Vouchers via Cex.IO can of coure also be used.

I will accept and appreciate every and all donations.

### Version history
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

