#-------------------------------------------------------------------------------
# Name:       CexControl
# Purpose:    Automatically add mined coins on Cex.IO to GHS pool
#
# Author:     Eloque
#
# Created:    19-11-2013
# Copyright:  (c) Eloque 2013
# Licence:    Free to use, copy and distribute as long as I'm credited
#             Provided as is, use at your own risk and for your own benefit
# Donate BTC: 17w7oe38d8Rm3pHYLwNZLn8TFSBVEaogJA
#-------------------------------------------------------------------------------

import cexapi
import re
import time
import json
import sys

INTEGERMATH = 100000000

version = "0.4.12"

NMCThreshold = 0.00010000
BTCThreshold = 0.00000100

def LoadSettings():

    print "Attempting to load Settings"

    try:

        fp = open("CexControlSettings.conf")
        settings = json.load(fp)

        if ( settings ):
            print "File found, loading"

    except IOError:
        print "Could not open file, attempting to create new one"
        CreateSettings()
        settings = LoadSettings()

    return settings

def CreateSettings():

    print ""
    print "Please enter your credentials"
    print ""
    username = raw_input("Username: ")
    key      = raw_input("API Key: ")
    secret   = raw_input("API Secret: ")

    settings = { "username":str(username), "key":str(key), "secret":str(secret) }

    try:
        json.dump(settings, open("CexControlSettings.conf", 'w'))
        print ""
        print "Configuration file created, attempting reload"
        print ""
    except:
        print sys.exc_info()
        print "Failed to write configuration file, giving up"
        exit()

def main():

    print ("======= CexControl version %s =======") % version

    ParseArguments()

    try:
        settings = LoadSettings()
    except:
        print "Could not load settings, exiting"
        exit()

    username    = str(settings['username'])
    api_key     = str(settings['key'])
    api_secret  = str(settings['secret'])

    try:
        context = cexapi.api(username, api_key, api_secret)
        balance = context.balance()

        print ("========================================")

        print "Account       : %s" % username
        print "GHS balance   : %s" % balance['GHS']['available']

        print ("========================================")

    except:
        print ("== !! ============================ !! ==")
        print "Error:",

        try:
            ErrorMessage = balance['error']
        except:
            ErrorMessage = "Unkown"

        print ErrorMessage

        print ""

        print "Could not connect Cex.IO, exiting"
        print ("== !! ============================ !! ==")
        exit()

    while True:
        now = time.asctime( time.localtime(time.time()) )

        print ""
        print "%s" % now

        CancelOrder(context)

        ##balance = context.balance()
        GHSBalance = GetBalance(context, 'GHS')
        print "GHS balance: %s" % GHSBalance ##  balance['GHS']['available']
        print ""

        TargetCoin = GetTargetCoin(context)

        print "Target Coin set to: %s" % TargetCoin
        print ""

        if (TargetCoin == "BTC"):
            ReinvestCoin(context, "NMC", NMCThreshold, TargetCoin )
            ReinvestCoin(context, "BTC", BTCThreshold, "GHS" )

        if (TargetCoin == "NMC"):
            ReinvestCoin(context, "BTC", BTCThreshold, TargetCoin )
            ReinvestCoin(context, "NMC", NMCThreshold, "GHS" )

        cycle = 150

        while cycle > 0:
            cycle = cycle - 1
            time.sleep(1)


    pass

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
            print "GHS/BTC Order %s canceled" % item['id']
        except:
            print "Cancel order failed"

    ## NMC Order cancel
    order = context.current_orders("GHS/NMC")
    for item in order:
        try:
            context.cancel_order(item['id'])
            print "GHS/NMC Order %s canceled" % item['id']
        except:
            print "Cancel order failed"

    ## NMC Order cancel
    order = context.current_orders("NMC/BTC")
    for item in order:
        try:
            context.cancel_order(item['id'])
            print "BTC/NMC Order %s canceled" % item['id']
        except:
            print "Cancel order failed"

## Get the balance of certain type of Coin
def GetBalance(Context, CoinName):

    balance = "NULL"

    try:

        balance = Context.balance()

        Coin =  balance[CoinName]
        Saldo = ConvertUnicodeFloatToFloat(Coin["available"])

    except:
        print balance
        Saldo = 0

    return Saldo

## Return the Contex for connection
def GetContext():

    try:
        settings = LoadSettings()
    except:
        print "Could not load settings, exiting"
        exit()

    username    = str(settings['username'])
    api_key     = str(settings['key'])
    api_secret  = str(settings['secret'])

    try:
        context = cexapi.api(username, api_key, api_secret)

    except:
        print context

    return context

def ParseArguments():
    arguments = sys.argv

    if (arguments.__len__ > 1):
        print "CexControl started with arguments"
        print ""

        ## Remove the filename itself
        del arguments[0]

        for argument in arguments:

            if argument == "newconfig":
                print "newconfig:"
                print "  Delete settings and create new"
                CreateSettings()

## Reinvest a coin
## only does a saldo check now....
def ReinvestCoin(Context, CoinName, Threshold, TargetCoin ):

    Saldo = GetBalance(Context, CoinName)

    print "%s" % CoinName,
    print "balance: %.8f" % Saldo

    if ( Saldo > Threshold ):

        TradeCoin( Context, CoinName, TargetCoin )


## Trade one coin for another
def TradeCoin( Context, CoinName, TargetCoin ):

    ## Get the Price of the TargetCoin
    Price = GetPriceByCoin( Context, CoinName, TargetCoin )

    print ("----------------------------------------")

    ## Get the balance of the coin
    Saldo = GetBalance( Context, CoinName)
    print CoinName,
    print "Balance %.8f" % Saldo

    ## Caculate what to buy
    AmountToBuy = Saldo / Price
    AmountToBuy = round(AmountToBuy-0.0000005,7)

    print "Amount to buy %.08f" % AmountToBuy

    ## This is an HACK
    Total = AmountToBuy * Price

    while ( Total > Saldo ):
        AmountToBuy = AmountToBuy - 0.0000005
        AmountToBuy = round(AmountToBuy-0.0000005,7)

        print ""
        print "To buy adjusted to : %.8f" % AmountToBuy
        Total = AmountToBuy * Price

    TickerName = GetTickerName( CoinName, TargetCoin )

    ## Hack, to differentiate between buy and sell
    action = ''
    if TargetCoin == "BTC":
        action = 'sell'
        AmountToBuy = Saldo ## sell the complete balance!
        print "To sell adjusted to : %.8f NMC" % AmountToBuy
    else:
        action = 'buy'

    result = Context.place_order(action, AmountToBuy, Price, TickerName )

    print ""
    print "Placed order at %s" % TickerName
    print "     Buy %.8f" % AmountToBuy,
    print "at %.10f" % Price
    print "   Total %.8f" % Total
    print "   Funds %.8f" % Saldo

    try:
        OrderID = result['id']
        print "Order ID %s" % OrderID
    except:
        print result

    print ("----------------------------------------")

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

    print "1 NMC is %s GHS" % FormatFloat(GHS_NMCPrice),
    print "1 NMC is %s BTC" % FormatFloat(NMC_BTCPrice)
    print "1 BTC is %s GHS" % FormatFloat(GHS_BTCPrice),
    print "1 BTC is %s NMC" % FormatFloat(BTC_NMCPrice)

    NMCviaBTC = NMC_BTCPrice * GHS_BTCPrice
    BTCviaNMC = BTC_NMCPrice * GHS_NMCPrice

    BTCviaNMCPercentage = BTCviaNMC / GHS_BTCPrice * 100
    NMCviaBTCPercentage = NMCviaBTC / GHS_NMCPrice * 100

    print ""
    print "1 BTC via NMC is %s GHS" % FormatFloat(BTCviaNMC),
    print "Efficiency : %2.2f" % BTCviaNMCPercentage
    print "1 NMC via BTC is %s GHS" % FormatFloat(NMCviaBTC),
    print "Efficiency : %2.2f" % NMCviaBTCPercentage


    if NMCviaBTCPercentage > BTCviaNMCPercentage:
        returnvalue = "BTC"
    else:
        returnvalue = "NMC"

    print ""
    print "Buy", returnvalue,
    print "then use that to buy GHS"

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

    return Ticker

## Get Price by ticker
def GetPrice(Context, Ticker):

    ## Get price
    ticker = Context.ticker(Ticker)

    Ask = ConvertUnicodeFloatToFloat(ticker["ask"])
    Bid = ConvertUnicodeFloatToFloat(ticker["bid"])

    ## Get average
    Price = (Ask+Bid) / 2

    ## Change price to 7 decimals
    Price = round(Price,8)

    ##print Price
    ##Price = int(Price * INTEGERMATH)

    return Price


if __name__ == '__main__':
    main()
