from db import cursor,mydb

NIFTY50 = [

    "ADANIENT",
    "ADANIPORTS",
    "APOLLOHOSP",
    "ASIANPAINT",
    "AXISBANK",

    "BAJAJ-AUTO",
    "BAJFINANCE",
    "BAJAJFINSV",
    "BEL",
    "BHARTIARTL",

    "CIPLA",
    "COALINDIA",
    "DRREDDY",
    "EICHERMOT",
    "ETERNAL",

    "GRASIM",
    "HCLTECH",
    "HDFCBANK",
    "HDFCLIFE",
    "HEROMOTOCO",

    "HINDALCO",
    "HINDUNILVR",
    "ICICIBANK",
    "INDUSINDBK",
    "INFY",

    "ITC",
    "JIOFIN",
    "JSWSTEEL",
    "KOTAKBANK",
    "LT",

    "M&M",
    "MARUTI",
    "NESTLEIND",
    "NTPC",
    "ONGC",

    "POWERGRID",
    "RELIANCE",
    "SBILIFE",
    "SBIN",
    "SHRIRAMFIN",

    "SUNPHARMA",
    "TATACONSUM",
    "TATAMOTORS",
    "TATASTEEL",
    "TCS",

    "TECHM",
    "TITAN",
    "TRENT",
    "ULTRACEMCO",
    "WIPRO"
]
NIFTYNEXT50 = [

    "ABB",
    "ADANIENSOL",
    "ADANIGREEN",
    "ADANIPOWER",
    "AMBUJACEM",

    "BAJAJHLDNG",
    "BANKBARODA",
    "BPCL",
    "BRITANNIA",
    "BOSCHLTD",

    "CANBK",
    "CGPOWER",
    "CHOLAFIN",
    "DABUR",
    "DLF",

    "DMART",
    "GAIL",
    "GODREJCP",
    "HAL",
    "HAVELLS",

    "ICICIGI",
    "ICICIPRULI",
    "INDIGO",
    "IOC",
    "IRCTC",

    "JINDALSTEL",
    "LICI",
    "LODHA",
    "MOTHERSON",
    "NAUKRI",

    "NHPC",
    "NMDC",
    "PAGEIND",
    "PATANJALI",
    "PEL",

    "PIDILITIND",
    "PNB",
    "RECLTD",
    "SAIL",
    "SHREECEM",

    "SIEMENS",
    "SRF",
    "TORNTPHARM",
    "TVSMOTOR",
    "UNITDSPR",

    "VEDL",
    "VBL",
    "ZYDUSLIFE",
    "BAJAJHFL",
    "HINDPETRO"

]

nifty_midcap_symbols = [
    "ASHOKLEY",
    "HEROMOTOCO",
    "POLYCAB",
    "BHARATFORG",
    "LUPIN",
    "MARICO",
    "INDUSTOWER",
    "BHEL",
    "GMRAIRPORT",
    "BSE",
    "INDIANB",
    "GVT&D",
    "SUZLON",
    "COCHINSHIP",
    "APLAPOLLO",
    "TIINDIA",
    "THERMAX",
    "MFSL",
    "EXIDEIND",
    "BLUESTARCO",
    "OFSS",
    "AUBANK",
    "FEDERALBNK",
    "IDFCFIRSTB",
    "MPHASIS",
    "PERSISTENT",
    "DIXON",
    "PAYTM",
    "TATAELXSI",
    "VOLTAS",
    "ZEEL",
    "LICHSGFIN",
    "NMDC",
    "OIL",
    "RECLTD",
    "PFC",
    "SJVN",
    "NHPC",
    "IRCTC",
    "RVNL",
    "CONCOR",
    "SOLARINDS",
    "PIIND",
    "DEEPAKNTR",
    "COROMANDEL",
    "PAGEIND",
    "RELAXO",
    "JUBLFOOD",
    "ABCAPITAL",
    "MUTHOOTFIN"
]
nifty_smallcap_symbols = [
    "AFFLE",
    "IEX",
    "CDSL",
    "CENTURYPLY",
    "CAMS",
    "RBLBANK",
    "CYIENT",
    "BLS",
    "RAINBOW",
    "EIDPARRY",
    "FSL",
    "CREDITACC",
    "KARURVYSYA",
    "FINPIPE",
    "JPPOWER",
    "IRB",
    "HFCL",
    "NBCC",
    "RCF",
    "CENTRALBK",
    "NATCOPHARM",
    "PVRINOX",
    "CHALET",
    "KAYNES",
    "LATENTVIEW",
    "ANGELONE",
    "CLEAN",
    "DATAPATTERNS",
    "NETWORK18",
    "BIRLACORPN",
    "TRIDENT",
    "SCI",
    "GRSE",
    "TEJASNET",
    "TANLA",
    "REDINGTON",
    "MMTC",
    "RITES",
    "PCBL",
    "SONATSOFTW",
    "HAPPSTMNDS",
    "CERA",
    "WELCORP",
    "EASEMYTRIP",
    "JYOTHYLAB",
    "INOXWIND",
    "PNBHOUSING",
    "POLYMED",
    "ASTERDM",
    "MAHSEAMLES"
]



query = """

INSERT INTO nifty_smallcap
(symbol)

VALUES (%s)

"""

for stock in nifty_smallcap_symbols:

    cursor.execute(
        query,
        stock
    )

mydb.commit()

