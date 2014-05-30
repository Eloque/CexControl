#------------------------------------------------------------------------------
# Name:       CexControl
# Purpose:    Automatically add mined coins on Cex.IO to GHS pool
#
# Author:     Eloque
#
# Created:    19-11-2013
# Copyright:  (c) Eloque 2013
# Licence:    Free to use, copy and distribute as long as I'm credited
#             Provided as is, use at your own risk and for your own benefit
# Donate BTC: 1Lehv8uMSMyYyY7ZFTN1NiRj8X24E56rvV
#-------------------------------------------------------------------------------

from __future__ import print_function

import cexapi
import re
import time
import json
import sys

## just place till P3
import urllib2

version = "0.9.2"

## Get Loggin obect
from Log import Logger
log = Logger()
settings = []

class CexControl:

    def __init__(self):

        ## Initialize class
        Trading = "GUI"

class Coin:

    def __init__(self, Name, Threshold, Reserve):

        self.Name = Name
        self.Threshold = Threshold
        self.Reserve = Reserve


class Settings:

    def __init__(self):

        self.BTC = Coin("BTC", 0.00001, 0.00)
        self.NMC = Coin("NMC", 0.00010, 0.00)
        self.IXC = Coin("IXC", 0.10000, 0.00)
        self.LTC = Coin("LTC", 0.10000, 0.00)

        self.EfficiencyThreshold = 1.0

        self.username    = ""
        self.api_key     = ""
        self.api_secret  = ""

        self.HoldCoins = False
        self.Trial = False

    def LoadSettings(self):

        log.Output ("Attempting to load Settings")

        try:

            fp = open("CexControlSettings.conf")
            LoadedFromFile = json.load(fp)

            self.username    = str(LoadedFromFile['username'])
            self.api_key     = str(LoadedFromFile['key'])
            self.api_secret  = str(LoadedFromFile['secret'])

            try:
                self.NMC.Threshold = float(LoadedFromFile['NMCThreshold'])
            except:
                log.Output ("NMC Threshold Setting not present, using default")

            try:
                self.NMC.Reserve = float(LoadedFromFile['NMCReserve'])
            except:
                log.Output ("NMC Reserve Setting not present, using default")

            try:
                self.BTC.Threshold = float(LoadedFromFile['BTCThreshold'])
            except:
                log.Output ("BTC Threshold Setting not present, using default")

            try:
                self.BTC.Reserve = float(LoadedFromFile['BTCReserve'])
            except:
                log.Output ("BTC Reserve Setting not present, using default")


            try:
                self.EfficiencyThreshold = float(LoadedFromFile['EfficiencyThreshold'])
            except:
                log.Output ("Efficiency Threshold Setting not present, using default")

            try:
                self.HoldCoins = bool(LoadedFromFile['HoldCoins'])
            except:
                log.Output ("Hold Coins Setting not present, using default")


            try:
                self.IXC.Threshold = float(LoadedFromFile['IXCThreshold'])
            except:
                log.Output ("IXC Threshold Setting not present, using default")

            try:
                self.IXC.Reserve = float(LoadedFromFile['IXCReserve'])
            except:
                log.Output ("IXC Reserve Setting not present, using default")

            if ( LoadedFromFile ):
                log.Output ("File found, loaded")

            try:
                self.LTC.Threshold = float(LoadedFromFile['LTCThreshold'])
            except:
                log.Output ("LTC Threshold Setting not present, using default")

            try:
                self.LTC.Reserve = float(LoadedFromFile['LTCReserve'])
            except:
                log.Output ("LTC Reserve Setting not present, using default")

            if ( LoadedFromFile ):
                log.Output ("File found, loaded")

        except IOError:
            log.Output ("Could not open file, attempting to create new one")
            self.CreateSettings()
            self.LoadSettings()

        ## Dunno, if I should...
        self.WriteSettings()

    def CreateSettings(self):

        log.Output ("")
        log.Output ("Please enter your credentials")
        log.Output ("")
        self.username     = raw_input("Username: ")
        self.api_key      = raw_input("API Key: ")
        self.api_secret   = raw_input("API Secret: ")

        self.CreateTresholds()

        self.WriteSettings()

    def WriteSettings(self):

        ToFile = { "username"               :str(self.username),
                   "key"                    :str(self.api_key),
                   "secret"                 :str(self.api_secret),
                   "BTCThreshold"           :str(self.BTC.Threshold),
                   "BTCReserve"             :str(self.BTC.Reserve),
                   "NMCThreshold"           :str(self.NMC.Threshold),
                   "NMCReserve"             :str(self.NMC.Reserve),
                   "IXCThreshold"           :str(self.IXC.Threshold),
                   "IXCReserve"             :str(self.IXC.Reserve),
                   "LTCThreshold"           :str(self.LTC.Threshold),
                   "LTCReserve"             :str(self.LTC.Reserve),
                   "EfficiencyThreshold"    :str(self.EfficiencyThreshold),
                   "HoldCoins"              :bool(self.HoldCoins),
                 }

        try:
            log.Output ("")
            log.Output ("Configuration created, attempting save")
            json.dump(ToFile, open("CexControlSettings.conf", 'w'))
            log.Output ("Save successfull, attempting reload")
        except:
            log.Output (sys.exc_info())
            log.Output ("Failed to write configuration file, giving up")
            exit()

    def CreateTresholds(self):

        log.Output ("")
        log.Output ("Please enter your thresholds")
        log.Output ("")

        self.BTC.Threshold = raw_input("Threshold to trade BTC: ")
        self.BTC.Reserve   = raw_input("Reserve for BTC: ")

        self.NMC.Threshold = raw_input("Threshold to trade NMC: ")
        self.NMC.Reserve   = raw_input("Reserve for NMC: ")

        self.IXC.Threshold = raw_input("Threshold to trade IXC: ")
        self.IXC.Reserve   = raw_input("Reserve for IXC: ")

        self.LTC.Threshold = raw_input("Threshold to trade LTC: ")
        self.LTC.Reserve   = raw_input("Reserve for LTC: ")

        self.EfficiencyThreshold   = raw_input("Efficiency at which to arbitrate: ")
        self.HoldCoins = raw_input("Hold Coins at low efficiency (Yes/No): ")

        if (self.HoldCoins == "Yes" ):
            self.HoldCoins = True
        else:
            self.HoldCoins = False

        self.WriteSettings()

    ## Simply return the context, based on user name, key and secret
    def GetContext(self):

        return cexapi.api(self.username, self.api_key, self.api_secret)

def main():

    log.Output ("======= CexControl version %s =======" % version)

    ## First, try to get the configuration settings in the settings object
    global settings
    settings = Settings()
    settings.LoadSettings()

    ParseArguments(settings)

    try:
        context = settings.GetContext()
        balance = context.balance()

        log.Output ("========================================")

        log.Output ("Account       : %s" % settings.username )
        log.Output ("GHS balance   : %s" % balance['GHS']['available'])

        log.Output ("========================================")

        log.Output ("BTC Threshold: %0.8f" % settings.BTC.Threshold)
        log.Output ("BTC Reserve  : %0.8f" % settings.BTC.Reserve)

        log.Output ("NMC Threshold: %0.8f" % settings.NMC.Threshold)
        log.Output ("NMC Reserve  : %0.8f" % settings.NMC.Reserve)

        log.Output ("IXC Threshold: %0.8f" % settings.IXC.Threshold)
        log.Output ("IXC Reserve  : %0.8f" % settings.IXC.Reserve)

        log.Output ("LTC Threshold: %0.8f" % settings.IXC.Threshold)
        log.Output ("LTC Reserve  : %0.8f" % settings.IXC.Reserve)

        log.Output ("Efficiency Threshold: %s" % settings.EfficiencyThreshold)
        log.Output ("Hold coins below efficiency threshold: %s" % settings.HoldCoins)

    except:
        log.Output ("== !! ============================ !! ==")
        log.Output ("Error:")

        try:
            ErrorMessage = balance['error']
        except:
            ErrorMessage = ("Unkown")

        log.Output(ErrorMessage)

        log.Output ("")

        log.Output ("Could not connect Cex.IO, exiting")
        log.Output ("== !! ============================ !! ==")
        exit()

    while True:
        try:
            TradeLoop(context, settings)

        except urllib2.HTTPError, err:
            log.Output ("HTTPError :%s" % err)

        except:
            log.Output ("Unexpected error:")
            log.Output ( sys.exc_info()[0] )
            log.Output ("An error occurred, skipping cycle")

        log.Output("")

        cycle = 150
        log.Output("Cycle completed, idle for %s seconds" % cycle)

        while cycle > 0:
            time.sleep(10)
            cycle = cycle - 10

    pass

## Externalised tradeloop
def TradeLoop(context, settings):
    now = time.asctime( time.localtime(time.time()) )

    log.Output ("")
    log.Output ("Start cycle at %s" % now)

    CancelOrder(context)

    ##balance = context.balance()
    GHSBalance = GetBalance(context, 'GHS')
    log.Output ("GHS balance: %s" % GHSBalance)
    log.Output ("")

    TargetCoin = GetTargetCoin(context)

    log.Output ("Target Coin set to: %s" % TargetCoin[0])
    log.Output ("")

    log.Output ( "Efficiency threshold: %s" % settings.EfficiencyThreshold )
    log.Output ( "Efficiency possible: %0.2f" % TargetCoin[1] )

    if (TargetCoin[1] >= settings.EfficiencyThreshold ):
        arbitrate = True
        log.Output ("Arbitration desired, trade coins for target coin")
    else:
        arbitrate = False
        if ( settings.HoldCoins == True ):
            log.Output ("Arbitration not desired, hold non target coins this cycle")
        else:
            log.Output ("Arbitration not desired, reinvest all coins this cycle")

    PrintBalance( context, "BTC")
    PrintBalance( context, "NMC")
    PrintBalance( context, "IXC")
    PrintBalance( context, "LTC")

    ## Trade in IXC
    ReinvestCoinByClass(context, settings.IXC, "BTC")

    ## Trade in LTC
    ReinvestCoinByClass(context, settings.LTC, "BTC")

    ## Trade for BTC
    if (TargetCoin[0] == "BTC"):
        if ( arbitrate ):
            ## We will assume that on arbitrate, we also respect the Reserve
            ReinvestCoinByClass(context, settings.NMC, TargetCoin[0] )

        else:
            if ( settings.HoldCoins == False ):
                ReinvestCoinByClass(context, settings.NMC, "GHS")

        ReinvestCoinByClass(context, settings.BTC, "GHS" )

    ## Trade for NMC
    if (TargetCoin[0] == "NMC"):
        if ( arbitrate ):
            ## We will assume that on arbitrate, we also respect the Reserve
            ReinvestCoinByClass(context, settings.BTC, TargetCoin[0] )
        else:
            if ( settings.HoldCoins == False ):
                ReinvestCoinByClass(context, settings.BTC, "GHS" )

        ReinvestCoinByClass(context, settings.NMC, "GHS" )


## Convert a unicode based float to a real float for us in calculations
def ConvertUnicodeFloatToFloat( UnicodeFloat ):

    ## I need to use a regular expression
    ## get all the character from after the dot
    position = re.search( '\.', UnicodeFloat)
    if ( position ):
        first = position.regs
        place = first[0]
        p = place[0]
        p = p + 1

        MostSignificant  = float(UnicodeFloat[:p-1])
        LeastSignificant = float(UnicodeFloat[p:])

        Factor = len(UnicodeFloat[p:])
        Divider = 10 ** Factor

        LeastSignificant = LeastSignificant / Divider

        NewFloat = MostSignificant + LeastSignificant
    else:
        NewFloat = float(UnicodeFloat)

    return NewFloat

def CancelOrder(context):
    ## BTC Order cancel
    order = context.current_orders("GHS/BTC")
    for item in order:
        try:
            context.cancel_order(item['id'])
            log.Output ("GHS/BTC Order %s canceled" % item['id'])
        except:
            log.Output ("Cancel order failed")

    ## NMC Order cancel
    order = context.current_orders("GHS/NMC")
    for item in order:
        try:
            context.cancel_order(item['id'])
            log.Output ("GHS/NMC Order %s canceled" % item['id'])
        except:
            log.Output ("Cancel order failed")

    ## NMC Order cancel
    order = context.current_orders("NMC/BTC")
    for item in order:
        try:
            context.cancel_order(item['id'])
            log.Output ("BTC/NMC Order %s canceled" % item['id'])
        except:
            log.Output ("Cancel order failed")

## Get the balance of certain type of Coin
def GetBalance(Context, CoinName):

    balance = ("NULL")

    ## log.Output("Attempting to retreive balance for %s" % CoinName)

    try:

        balance = Context.balance()

        Coin =  balance[CoinName]
        Saldo = ConvertUnicodeFloatToFloat(Coin["available"])

    except:
        ## log.Output (balance)
        Saldo = 0

    return Saldo

## Return the Contex for connection
def GetContext():

    try:
        settings = LoadSettings()
    except:
        log.Output ("Could not load settings, exiting")
        exit()

    username    = str(settings['username'])
    api_key     = str(settings['key'])
    api_secret  = str(settings['secret'])

    try:
        context = cexapi.api(username, api_key, api_secret)

    except:
        log.Output (context)

    return context

def ParseArguments(settings):
    arguments = sys.argv

    if (len(arguments) > 1):
        log.Output ("CexControl started with arguments")
        log.Output ("")

        ## Remove the filename itself
        del arguments[0]

        for argument in arguments:

            if argument == "newconfig":
                log.Output ("newconfig:")
                log.Output ("  Delete settings and create new")
                settings.CreateSettings()

            if argument == "setthreshold":
                log.Output ("setthreshold:")
                log.Output ("  Creeate new threshold settings")
                settings.CreateTresholds()
                settings.LoadSettings()

            if argument == "version":
                log.Output ("Version: %s" % version )
                exit()

            if argument == "trial":
                log.Output ("trial:")
                log.Output ("  Trial mode, do not execute any real actions")
                settings.Trial = True


## log.Output the balance of a Coin
def PrintBalance( Context, CoinName):

    Saldo = GetBalance(Context, CoinName)

    message = "%s " % CoinName
    message = message + "Balance: %.8f" % Saldo

    log.Output ( message )


## Holder Class, to reinvest Coin by class
def ReinvestCoinByClass(Context, Coin, TargetCoin ):

    CoinName   = Coin.Name
    Threshold  = Coin.Threshold
    TargetCoin = TargetCoin

    Saldo = GetBalance(Context, CoinName)
    InvestableSaldo = Saldo - Coin.Reserve


    if ( InvestableSaldo > Threshold ):
        TradeCoin( Context, CoinName, TargetCoin, InvestableSaldo )


## Reinvest a coin
def ReinvestCoin(Context, CoinName, Threshold, TargetCoin ):

    log.Output("Old function used, please issue a bug report, mention ReinvestCoin used")

##    Saldo = GetBalance(Context, CoinName)
##    if ( Saldo > Threshold ):
##        TradeCoin( Context, CoinName, TargetCoin )


## Trade one coin for another
def TradeCoin( Context, CoinName, TargetCoin, Amount ):
    global settings

    ## Get the Price of the TargetCoin
    Price = GetPriceByCoin( Context, CoinName, TargetCoin )

    log.Output ("----------------------------------------")
    log.Output ( CoinName + " for " + TargetCoin )

    ## Get the balance of the coin
    TotalBalance = GetBalance(Context, CoinName)

    ## Calculate the reserve, if any, we already have the amount
    Saldo = Amount

    ## The hack we are using right now is going to be to add 2 percent to the PRICE of the
    ## targetcoin,
    FeePrice = Price * 1.02

    ## Caculate what to buy
    AmountToBuy = Saldo / FeePrice
    AmountToBuy = round(AmountToBuy-0.000005,6)

    ## Calculate the total amount
    Total = AmountToBuy * FeePrice

    ## Adjusted to compensate for floating math conversion
    while ( Total > Saldo ):
        AmountToBuy = AmountToBuy - 0.0000005
        AmountToBuy = round(AmountToBuy-0.000005,6)

        log.Output ("")
        log.Output ("To buy adjusted to : %.8f" % AmountToBuy)

        ## Hack to adjust for 2% fee
        Total = AmountToBuy * FeePrice

    TickerName = GetTickerName( CoinName, TargetCoin )

    ## Hack, to differentiate between buy and sell
    action = ''
    Gain = 0.0
    if TargetCoin == "BTC":
        action = 'sell'
        AmountToBuy = Saldo ## sell the complete balance!
        log.Output ("Amount to sell %.08f" % AmountToBuy)

        ## I am selling my Coin, for FeePrice BTC per Coin
        ## So, I get AmounToBuy / FeePrice BTC
        Gain = AmountToBuy * FeePrice

    else:
        action = 'buy'
        log.Output ("Amount to buy %.08f" % AmountToBuy)

        ## I am buying Coin, for FeePrice per Coin
        ## So, I get AmounToBuy
        Gain = AmountToBuy

    if settings.Trial == False:
        result = Context.place_order(action, AmountToBuy, Price, TickerName )
    else:
        log.Output ("No real trade, trial mode")


    log.Output ("")
    log.Output ("Placed order at %s" % TickerName)

    if TargetCoin == "BTC":
        log.Output ("   Sell %.8f" % AmountToBuy)
    else:
        log.Output ("   Buy %.8f" % AmountToBuy)

    log.Output ("   at %.8f" % Price)
    log.Output ("   Total %.8f" % Total)
    log.Output ("   Funds %.8f" % TotalBalance)

    log.Output ("")
    string = "   Gain %.8f " % Gain
    string = string + TargetCoin
    log.Output ( string )

    try:
        if settings.Trial == False:
            OrderID = result['id']
            log.Output ("Order ID %s" % OrderID)

    except:
        log.Output (result)
        log.Output (AmountToBuy)
        log.Output ("%.7f" % Price)
        log.Output (TickerName)


    log.Output ("----------------------------------------")

## Simply reformat a float to 8 numbers behind the comma
def FormatFloat( number):

    number = unicode("%.8f" % number)
    return number

## Get TargetCoin, reveal what coin we should use to buy GHS
def GetTargetCoin(Context):
    ## Get the Price NMC/BTC

    GHS_NMCPrice = GetPrice(Context, "GHS/NMC")
    GHS_BTCPrice = GetPrice(Context, "GHS/BTC")
    NMC_BTCPrice = GetPrice(Context, "NMC/BTC")

    BTC_NMCPrice = 1/NMC_BTCPrice

    GHS_NMCPrice = 1/GHS_NMCPrice
    GHS_BTCPrice = 1/GHS_BTCPrice

    log.Output ("1 NMC is %s GHS" % FormatFloat(GHS_NMCPrice))
    log.Output ("1 NMC is %s BTC" % FormatFloat(NMC_BTCPrice))
    log.Output ("1 BTC is %s GHS" % FormatFloat(GHS_BTCPrice))
    log.Output ("1 BTC is %s NMC" % FormatFloat(BTC_NMCPrice))

    NMCviaBTC = NMC_BTCPrice * GHS_BTCPrice
    BTCviaNMC = BTC_NMCPrice * GHS_NMCPrice

    BTCviaNMCPercentage = BTCviaNMC / GHS_BTCPrice * 100
    NMCviaBTCPercentage = NMCviaBTC / GHS_NMCPrice * 100

    log.Output ("")
    log.Output ("1 BTC via NMC is %s GHS" % FormatFloat(BTCviaNMC) )
    log.Output ("Efficiency : %2.2f" % BTCviaNMCPercentage)
    log.Output ("1 NMC via BTC is %s GHS" % FormatFloat(NMCviaBTC) )
    log.Output ("Efficiency : %2.2f" % NMCviaBTCPercentage)

    if NMCviaBTCPercentage > BTCviaNMCPercentage:
        coin = "BTC"
        efficiency = NMCviaBTCPercentage - 100
    else:
        coin = "NMC"
        efficiency = BTCviaNMCPercentage - 100

    returnvalue = (coin, efficiency)

    log.Output ("")
    log.Output ("Buy %s then use that to buy GHS" % coin )


    return returnvalue

## Get the price of a coin for a market value
def GetPriceByCoin(Context, CoinName, TargetCoin ):

    Ticker = GetTickerName( CoinName, TargetCoin )

    return GetPrice(Context, Ticker)

## Fall back function to get TickerName
def GetTickerName( CoinName, TargetCoin ):

    Ticker = ""

    if CoinName == "NMC" :
        if TargetCoin == "GHS" :
            Ticker = "GHS/NMC"
        if TargetCoin == "BTC" :
            Ticker = "NMC/BTC"

    if CoinName == "BTC" :
        if TargetCoin == "GHS" :
            Ticker = "GHS/BTC"
        if TargetCoin == "NMC" :
            Ticker = "NMC/BTC"

    if CoinName == "IXC" :
        Ticker = "IXC/BTC"

    if CoinName == "LTC" :
        Ticker = "LTC/BTC"

    return Ticker

## Get Price by ticker
def GetPrice(Context, Ticker):

    ## Get price
    ticker = Context.ticker(Ticker)

    ## Ask = ConvertUnicodeFloatToFloat(ticker["ask"])
    ## Bid = ConvertUnicodeFloatToFloat(ticker["bid"])

    Ask = ticker["ask"]
    Bid = ticker["bid"]

    ## Get average
    Price = (Ask+Bid) / 2

    ## Change price to 7 decimals
    Price = round(Price,7)

    return Price


if __name__ == '__main__':
    main()
