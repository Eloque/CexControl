CexControl
==========
Python utility to connect to Cex.IO

Be warned, this is a rough Beta version. Use at your own risk.

==========
Instructions & Installation

To start, run the script on a commandline, ie, "python ./CexControl.py"
The script will detect if there is a configuration file or not, and prompt for user input if not.

To create a new configuration, start with "python ./CexControl.py newconfig", this will delete the existing configuration.

The script will run and check every 5 minutes if there are more then 0.0001 BTC or NMC available. 

If that is the case, the script will retrieve both Bid and Ask prices and average those in a on order spending as close to maximum as possible. If those orders are not fulfilled within 5 minutes, they will be canceled and new orders put in.

==========
Version 0.3.4
Added more error handling.
Added configuration by script.
Added newconfig argument


Version 0.3.2
Initial version pushed to GitHub.

