import json

# Read the file containing the data
with open('core/demo/output.json', 'r') as file:
    data = json.load(file)

# Define the bank data
bank_data = [
{
"id": "5d6fe57a4099cc4b210bbeb1",
"name": "First Bank of Nigeria"
},
{
"id": "5d6fe57a4099cc4b210bbeae",
"name": "Ecobank Nigeria"
},
{
"id": "5d6fe57a4099cc4b210bbeb0",
"name": "Fidelity Bank"
},
{
"id": "5d6fe57a4099cc4b210bbeb2",
"name": "First City Monument Bank"
},
{
"id": "5d6fe57a4099cc4b210bbeb3",
"name": "Guaranty Trust Bank"
},
{
"id": "5d6fe57a4099cc4b210bbeb4",
"name": "Heritage Bank"
},
{
"id": "5d6fe57a4099cc4b210bbeb6",
"name": "Stanbic IBTC Bank"
},
{
"id": "5d6fe57a4099cc4b210bbeb8",
"name": "Sterling Bank"
},
{
"id": "5d6fe57a4099cc4b210bbeb9",
"name": "Union Bank of Nigeria"
},
{
"id": "5d6fe57a4099cc4b210bbeb5",
"name": "Polaris Bank"
},
{
"id": "5d6fe57a4099cc4b210bbeb7",
"name": "Standard Chartered Bank"
},
{
"id": "5d6fe57a4099cc4b210bbeba",
"name": "Keystone Bank"
},
{
"id": "5d6fe57a4099cc4b210bbebb",
"name": "United Bank For Africa"
},
{
"id": "5d6fe57a4099cc4b210bbebe",
"name": "Alat"
},
{
"id": "5d6fe57a4099cc4b210bbebf",
"name": "Providus Bank"
},
{
"id": "5d6fe57a4099cc4b210bbebc",
"name": "Wema Bank"
},
{
"id": "5d6fe57a4099cc4b210bbebd",
"name": "Unity Bank"
},
{
"id": "5d6fe57a4099cc4b210bbec2",
"name": "Zenith Bank"
},
{
"id": "5d6fe57a4099cc4b210bbec0",
"name": "Access Bank"
},
{
"id": "5f0cf73e8a8bcc18b8156ad7",
"name": "Kuda Bank"
},
{
"id": "5f11487e847b28538bfc6c5f",
"name": "Rubies Bank"
},
{
"id": "5f63f473d550180010a14bf1",
"name": "Diamond Bank"
},
{
"id": "5f7cf82be07d4a80c432bc7f",
"name": "Standard Bank"
},
{
"id": "5f7cf986e07d4a80c432bc80",
"name": "Absa Bank"
},
{
"id": "5f7dd068e07d4a80c432bc81",
"name": "Nedbank"
},
{
"id": "5f7eee62e07d4a80c432bc82",
"name": "Investec"
},
{
"id": "5f7eefb3e07d4a80c432bc83",
"name": "First National Bank"
},
{
"id": "5f7ef093e07d4a80c432bc84",
"name": "Tyme Bank"
},
{
"id": "5f7ef153e07d4a80c432bc85",
"name": "Capitec Bank"
},
{
"id": "5f7ff8b7e07d4a80c432bc87",
"name": "Equity Bank"
},
{
"id": "5f7ff97ce07d4a80c432bc88",
"name": "Kenya Commercial Bank"
},
{
"id": "5f7ffb57e07d4a80c432bc8a",
"name": "National Bank"
},
{
"id": "5f7ffd7ee07d4a80c432bc8b",
"name": "NIC Bank"
},
{
"id": "5f7ffddfe07d4a80c432bc8c",
"name": "CBA Bank"
},
{
"id": "5f7ffe3fe07d4a80c432bc8d",
"name": "Cooperative Bank"
},
{
"id": "5f7ffec1e07d4a80c432bc8e",
"name": "DTB"
},
{
"id": "5fad03e18a795405d628156f",
"name": "V Bank"
},
{
"id": "5fb906f78c486a00b987ec06",
"name": "Jaiz Bank"
},
{
"id": "60d3b07f48171162e342ae3d",
"name": "N/A"
},
{
"id": "610080715958c61031f37737",
"name": "Titan Trust Bank"
},
{
"id": "6101a35312015634f5c23adf",
"name": "Paga"
},
{
"id": "61187bdc92628e026f7ddb5f",
"name": "Paystack"
},
{
"id": "611e3b8632657e7e2dd15636",
"name": "Carbon"
},
{
"id": "604f9bc66b259900ab5b0d1a",
"name": "SBM"
},
{
"id": "611ff0ee412b11f1b2143bc5",
"name": "CitiBank Nigeria"
},
{
"id": "611ff0ee412b11f1b2143bd3",
"name": "Haggai Mortgage Bank Limited"
},
{
"id": "611ff0ee412b11f1b2143be0",
"name": "Zinternet KongaPay"
},
{
"id": "611ff0ee412b11f1b2143bed",
"name": "Lagos Building Investment Company"
},
{
"id": "611ff0ee412b11f1b2143bfa",
"name": "AG MORTGAGE BANK PLC"
},
{
"id": "611ff0ef412b11f1b2143c07",
"name": "Innovectives Kesh"
},
{
"id": "611ff0ef412b11f1b2143c1e",
"name": "FinaTrust Microfinance Bank"
},
{
"id": "611ff0ef412b11f1b2143c3f",
"name": "Xslnce Microfinance Bank"
},
{
"id": "611ff0f0412b11f1b2143c59",
"name": "BC Kash Microfinance Bank"
},
{
"id": "611ff0f0412b11f1b2143c66",
"name": "Ndiorah Microfinance Bank"
},
{
"id": "611ff0f0412b11f1b2143c72",
"name": "Money Trust Microfinance Bank"
},
{
"id": "611ff0f1412b11f1b2143c7e",
"name": "Allworkers Microfinance Bank"
},
{
"id": "611ff0f1412b11f1b2143ce1",
"name": "Richway Microfinance Bank"
},
{
"id": "611ff0f1412b11f1b2143cf4",
"name": "PecanTrust Microfinance Bank"
},
{
"id": "611ff0f1412b11f1b2143cff",
"name": "Yes Microfinance Bank"
},
{
"id": "611ff0f1412b11f1b2143d15",
"name": "ACCESS YELLO & BETA"
},
{
"id": "611ff0f4412b11f1b2143d63",
"name": "Enterprise Bank"
},
{
"id": "611ff0f4412b11f1b2143d6f",
"name": "SunTrust Bank"
},
{
"id": "611ff0f5412b11f1b2143d9e",
"name": "Globus Bank"
},
{
"id": "611ff0f5412b11f1b2143da9",
"name": "EMPIRE MFB"
},
{
"id": "611ff0f5412b11f1b2143db4",
"name": "TCF MICROFINANCE BANK"
},
{
"id": "611ff0f5412b11f1b2143dbf",
"name": "Ohafia Microfinance Bank"
},
{
"id": "611ff0f5412b11f1b2143dca",
"name": "Wetland Microfinance Bank"
},
{
"id": "611ff0f6412b11f1b2143dd5",
"name": "Sagamu Microfinance Bank"
},
{
"id": "611ff0f6412b11f1b2143de0",
"name": "FAST MICROFINANCE BANK"
},
{
"id": "611ff0f6412b11f1b2143deb",
"name": "NIP NEWBANK TSQ"
},
{
"id": "611ff0f8412b11f1b2143e2b",
"name": "Ibile Microfinance Bank"
},
{
"id": "611ff0f9412b11f1b2143e45",
"name": "Eartholeum"
},
{
"id": "611ff0f9412b11f1b2143e51",
"name": "ChamsMobile"
},
{
"id": "611ff0f9412b11f1b2143e5c",
"name": "Stanbic IBTC @ease Wallet"
},
{
"id": "611ff0f9412b11f1b2143e67",
"name": "OPAY"
},
{
"id": "611ff0f9412b11f1b2143e72",
"name": "eTranzact"
},
{
"id": "611ff0f9412b11f1b2143e7f",
"name": "Ecobank Xpress Account"
},
{
"id": "611ff0fa412b11f1b2143e90",
"name": "FortisMobile"
},
{
"id": "611ff0fa412b11f1b2143e9b",
"name": "Firstmonie Wallet"
},
{
"id": "611ff0fa412b11f1b2143ea6",
"name": "ReadyCash (Parkway)"
},
{
"id": "611ff0fa412b11f1b2143eb6",
"name": "FCMB Easy Account"
},
{
"id": "611ff0fa412b11f1b2143ec1",
"name": "Mkudi"
},
{
"id": "611ff0fa412b11f1b2143ecf",
"name": "FET"
},
{
"id": "611ff0fa412b11f1b2143edc",
"name": "GTMobile"
},
{
"id": "611ff0fb412b11f1b2143ee9",
"name": "Cellulant"
},
{
"id": "611ff0fb412b11f1b2143f01",
"name": "TeasyMobile"
},
{
"id": "611ff0fb412b11f1b2143f0c",
"name": "VTNetworks"
},
{
"id": "611ff0fb412b11f1b2143f17",
"name": "ZenithMobile"
},
{
"id": "611ff0fb412b11f1b2143f22",
"name": "Access Money"
},
{
"id": "611ff0fb412b11f1b2143f2d",
"name": "Hedonmark"
},
{
"id": "611ff0fc412b11f1b2143f38",
"name": "MoneyBox"
},
{
"id": "611ff0fc412b11f1b2143f44",
"name": "GoMoney"
},
{
"id": "611ff0fc412b11f1b2143f5a",
"name": "TagPay"
},
{
"id": "611ff0fc412b11f1b2143f65",
"name": "PayAttitude Online"
},
{
"id": "611ff0fc412b11f1b2143f70",
"name": "miMONEY"
},
{
"id": "611ff0fc412b11f1b2143f7c",
"name": "9 PAYMENT SERVICE BANK"
},
{
"id": "611ff0fd412b11f1b2143f89",
"name": "CONPRO MICROFINANCE BANK"
},
{
"id": "611ff0fd412b11f1b2143f95",
"name": "ILISAN MICROFINANCE BANK"
},
{
"id": "611ff0fd412b11f1b2143fa0",
"name": "Bridgeway Microfinance Bank"
},
{
"id": "611ff0fd412b11f1b2143fab",
"name": "ASO Savings and Loans"
},
{
"id": "611ff0fd412b11f1b2143fb6",
"name": "Jubilee Life Mortgage Bank"
},
{
"id": "611ff0fd412b11f1b2143fc1",
"name": "SafeTrust Mortgage Bank"
},
{
"id": "611ff0fd412b11f1b2143fcc",
"name": "CEMCS Microfinance Bank"
},
{
"id": "611ff0fd412b11f1b2143fd7",
"name": "FBN Mortgage Bank (First Trust Mortgage Bank)"
},
{
"id": "611ff0fe412b11f1b2143fe2",
"name": "Imperial Homes Mortgage Bank"
},
{
"id": "611ff0fe412b11f1b2144001",
"name": "Rand Merchant Bank"
},
{
"id": "611ff0fe412b11f1b214400d",
"name": "Trustbond Mortgage Bank (First Trust Mortgage Bank)"
},
{
"id": "611ff0fe412b11f1b2144018",
"name": "Parralex"
},
{
"id": "611ff0fe412b11f1b2144024",
"name": "Covenant Microfinance Bank"
},
{
"id": "611ff0fe412b11f1b214402f",
"name": "NPF MicroFinance Bank"
},
{
"id": "611ff0fe412b11f1b214403c",
"name": "Coronation Merchant Bank"
},
{
"id": "611ff0ff412b11f1b2144047",
"name": "Page MFBank"
},
{
"id": "611ff0ff412b11f1b2144053",
"name": "New Prudential Bank"
},
{
"id": "611ff0ff412b11f1b214406c",
"name": "Abbey Mortgage Bank"
},
{
"id": "611ff0ff412b11f1b2144077",
"name": "Fidifund Microfinance Bank"
},
{
"id": "611ff0ff412b11f1b2144085",
"name": "Verite Microfinance Bank"
},
{
"id": "611ff0ff412b11f1b214409e",
"name": "Gateway Mortgage Bank"
},
{
"id": "611ff100412b11f1b21440ab",
"name": "Al-Barakah Microfinance Bank"
},
{
"id": "611ff100412b11f1b21440b8",
"name": "Consumer Microfinance Bank"
},
{
"id": "611ff100412b11f1b21440c4",
"name": "Hasal Microfinance Bank"
},
{
"id": "611ff100412b11f1b21440cf",
"name": "Refuge Mortgage Bank"
},
{
"id": "611ff100412b11f1b21440da",
"name": "Personal Trust Microfinance Bank"
},
{
"id": "611ff100412b11f1b21440e7",
"name": "BAOBAB MICROFINANCE BANK"
},
{
"id": "611ff100412b11f1b21440f3",
"name": "Visa Microfinance Bank"
},
{
"id": "611ff101412b11f1b21440fe",
"name": "Royal Exchange Microfinance Bank"
},
{
"id": "611ff101412b11f1b2144109",
"name": "Seed Capital Microfinance Bank"
},
{
"id": "611ff101412b11f1b2144115",
"name": "Boctrust Microfinance Bank"
},
{
"id": "611ff101412b11f1b2144120",
"name": "Stanford Microfinance Bank"
},
{
"id": "611ff101412b11f1b214412b",
"name": "Daylight Microfinance Bank"
},
{
"id": "611ff101412b11f1b2144136",
"name": "Alpha Kapital Microfinance Bank"
},
{
"id": "611ff101412b11f1b2144141",
"name": "Reliance Microfinance Bank"
},
{
"id": "611ff101412b11f1b214414d",
"name": "Malachy Microfinance Bank"
},
{
"id": "611ff102412b11f1b2144165",
"name": "Rahama Microfinance Bank"
},
{
"id": "611ff102412b11f1b2144171",
"name": "AMJU UNIQUE MFB"
},
{
"id": "611ff102412b11f1b214417e",
"name": "LAPO MICROFINANCE BANK"
},
{
"id": "611ff102412b11f1b214418a",
"name": "ESAN MICROFINANCE BANK"
},
{
"id": "611ff103412b11f1b2144195",
"name": "BAINES CREDIT MFB"
},
{
"id": "611ff103412b11f1b21441a1",
"name": "LA FAYETTE MICROFINANCE BANK"
},
{
"id": "611ff103412b11f1b21441ad",
"name": "KCMB MICROFINANCE BANK"
},
{
"id": "611ff103412b11f1b21441b8",
"name": "MIDLAND MICROFINANCE BANK"
},
{
"id": "611ff103412b11f1b21441c3",
"name": "UNICAL MICROFINANCE BANK"
},
{
"id": "611ff103412b11f1b21441ce",
"name": "NAGARTA MICROFINANCE BANK"
},
{
"id": "611ff103412b11f1b21441d9",
"name": "RENMONEY MICROFINANCE BANK"
},
{
"id": "611ff103412b11f1b21441e6",
"name": "Bosak Microfinance Bank"
},
{
"id": "611ff104412b11f1b21441f1",
"name": "FSDH Merchant Bank Limited"
},
{
"id": "611ff104412b11f1b21441fc",
"name": "Accion Microfinance Bank"
},
{
"id": "611ff104412b11f1b214420a",
"name": "Platinum Mortgage Bank"
},
{
"id": "611ff104412b11f1b2144217",
"name": "GREENBANK MICROFINANCE BANK"
},
{
"id": "611ff104412b11f1b2144222",
"name": "NIRSAL Microfinance Bank"
},
{
"id": "611ff104412b11f1b214422f",
"name": "UNN Microfinance Bank"
},
{
"id": "611ff104412b11f1b214423c",
"name": "Alekun Microfinance Bank"
},
{
"id": "611ff105412b11f1b2144247",
"name": "Stellas Microfinance Bank"
},
{
"id": "611ff105412b11f1b2144254",
"name": "Quickfund Microfinance Bank"
},
{
"id": "611ff105412b11f1b214426a",
"name": "Auchi Microfinance Bank"
},
{
"id": "611ff105412b11f1b2144275",
"name": "AB Microfinance Bank"
},
{
"id": "611ff105412b11f1b2144280",
"name": "Nigerian Navy Microfinance Bank"
},
{
"id": "611ff105412b11f1b214428b",
"name": "Brent Mortgage Bank"
},
{
"id": "611ff106412b11f1b2144296",
"name": "Lovonus Microfinance Bank"
},
{
"id": "611ff106412b11f1b21442a1",
"name": "Greenville Microfinance Bank"
},
{
"id": "611ff106412b11f1b21442ad",
"name": "Adeyemi College Staff Microfinance Bank"
},
{
"id": "611ff106412b11f1b21442b9",
"name": "GROOMING MICROFINANCE BANK"
},
{
"id": "611ff106412b11f1b21442c4",
"name": "EMERALDS MICROFINANCE BANK"
},
{
"id": "611ff106412b11f1b21442cf",
"name": "TRUSTFUND MICROFINANCE BANK"
},
{
"id": "611ff106412b11f1b21442da",
"name": "New Dawn Microfinance Bank"
},
{
"id": "611ff106412b11f1b21442e6",
"name": "TAJ Bank"
},
{
"id": "611ff107412b11f1b2144365",
"name": "Lavender Microfinance Bank"
},
{
"id": "611ff107412b11f1b2144370",
"name": "Olabisi Onabanjo University Microfinance Bank"
},
{
"id": "611ff107412b11f1b214437b",
"name": "Omiye Microfinance Bank"
},
{
"id": "611ff107412b11f1b2144386",
"name": "Astrapolaris Microfinance Bank"
},
{
"id": "611ff107412b11f1b2144391",
"name": "Nova Merchant Bank"
},
{
"id": "611ff108412b11f1b214439c",
"name": "Pillar Microfinance Bank"
},
{
"id": "611ff108412b11f1b21443a7",
"name": "SAFE HAVEN MICROFINANCE BANK"
},
{
"id": "611ff108412b11f1b21443b2",
"name": "BRIGHTWAY MICROFINANCE BANK"
},
{
"id": "611ff108412b11f1b21443be",
"name": "Alert Microfinance Bank"
},
{
"id": "611ff108412b11f1b21443c9",
"name": "MINT-FINEX MFB"
},
{
"id": "611ff108412b11f1b21443d4",
"name": "Sparkle"
},
{
"id": "611ff108412b11f1b21443df",
"name": "EdFin Microfinance Bank"
},
{
"id": "611ff108412b11f1b21443ec",
"name": "PALMPAY"
},
{
"id": "611ff109412b11f1b21443f7",
"name": "BALOGUN GAMBARI MFB"
},
{
"id": "611ff109412b11f1b2144404",
"name": "EVANGEL MICROFINANCE BANK"
},
{
"id": "611ff109412b11f1b2144412",
"name": "TRUST MICROFINANCE BANK"
},
{
"id": "611ff109412b11f1b214441d",
"name": "OCHE MICROFINANCE BANK"
},
{
"id": "611ff109412b11f1b2144429",
"name": "EYOWO MICROFINANCE BANK"
},
{
"id": "611ff109412b11f1b2144434",
"name": "EVERGREEN MICROFINANCE BANK"
},
{
"id": "611ff109412b11f1b214443f",
"name": "Neptune Microfinance Bank"
},
{
"id": "611ff10a412b11f1b214444a",
"name": "UNAAB MICROFINANCE BANK"
},
{
"id": "611ff10a412b11f1b2144456",
"name": "IKENNE MICROFINANCE BANK"
},
{
"id": "611ff10a412b11f1b2144461",
"name": "Mayfair MFB"
},
{
"id": "611ff10a412b11f1b214446d",
"name": "REPHIDIM MICROFINANCE BANK"
},
{
"id": "611ff10a412b11f1b2144478",
"name": "KONTAGORA MICROFINANCE BANK"
},
{
"id": "611ff10a412b11f1b2144484",
"name": "CASHCONNECT MFB"
},
{
"id": "611ff10a412b11f1b2144490",
"name": "NUTURE MICROFINANCE BANK"
},
{
"id": "611ff10a412b11f1b214449e",
"name": "BIPC MICROFINANCE BANK"
},
{
"id": "611ff10b412b11f1b21444ab",
"name": "IKIRE MICROFINANCE BANK"
},
{
"id": "611ff10b412b11f1b21444b9",
"name": "MOLUSI MICROFINANCE BANK"
},
{
"id": "611ff10b412b11f1b21444c6",
"name": "LEGEND MICROFINANCE BANK"
},
{
"id": "611ff10b412b11f1b21444d1",
"name": "FEDERAL UNIVERSITY DUTSE MICROFINANCE BANK"
},
{
"id": "611ff10b412b11f1b21444dc",
"name": "COASTLINE MICROFINANCE BANK"
},
{
"id": "611ff10b412b11f1b21444e7",
"name": "Purple Money Microfinance Bank"
},
{
"id": "611ff10b412b11f1b21444f2",
"name": "MERIDIAN MFB"
},
{
"id": "611ff10c412b11f1b21444fe",
"name": "Fullrange Microfinance Bank"
},
{
"id": "611ff10c412b11f1b214450a",
"name": "FBNQUEST MB"
},
{
"id": "611ff10c412b11f1b2144516",
"name": "Petra Microfinance Bank"
},
{
"id": "611ff10c412b11f1b2144522",
"name": "First Royal Microfinance Bank"
},
{
"id": "611ff10c412b11f1b214452e",
"name": "ADDOSSER MICROFINANCE BANK"
},
{
"id": "611ff10c412b11f1b2144539",
"name": "FFS Microfinance"
},
{
"id": "611ff10c412b11f1b2144546",
"name": "Trident Microfinance Bank"
},
{
"id": "611ff10d412b11f1b2144552",
"name": "Mutual Trust Microfinance Bank"
},
{
"id": "611ff10d412b11f1b214455e",
"name": "IRL Microfinance Bank"
},
{
"id": "611ff10d412b11f1b2144569",
"name": "Infinity Trust Mortgage Bank"
},
{
"id": "611ff10d412b11f1b2144575",
"name": "Hackman Microfinance Bank"
},
{
"id": "611ff10d412b11f1b2144580",
"name": "First Generation Mortgage Bank"
},
{
"id": "611ff10d412b11f1b214458b",
"name": "CIT Microfinance Bank"
},
{
"id": "611ff10d412b11f1b2144596",
"name": "Chikum Microfinance Bank"
},
{
"id": "611ff10d412b11f1b21445a2",
"name": "Apeks Microfinance Bank"
},
{
"id": "611ff10e412b11f1b21445ae",
"name": "Bowen Microfinance Bank"
},
{
"id": "611ff10e412b11f1b21445b9",
"name": "Omoluabi Mortgage Bank"
},
{
"id": "611ff10e412b11f1b21445c5",
"name": "Gowans Microfinance Bank"
},
{
"id": "611ff10e412b11f1b21445d4",
"name": "Ekondo Microfinance Bank"
},
{
"id": "611ff10e412b11f1b21445df",
"name": "AMML MFB"
},
{
"id": "611ff10e412b11f1b21445ec",
"name": "Regent Microfinance Bank"
},
{
"id": "611ff10e412b11f1b21445f8",
"name": "CREDIT AFRIQUE MICROFINANCE BANK"
},
{
"id": "611ff10f412b11f1b2144604",
"name": "Contec Global Infotech Limited"
},
{
"id": "611ff10f412b11f1b2144610",
"name": "e-BARCS MICROFINANCE BANK"
},
{
"id": "611ff10f412b11f1b214461d",
"name": "NIP Virtual Bank"
},
{
"id": "611ff10f412b11f1b2144628",
"name": "Bainescredit MFB"
},
{
"id": "611ff10f412b11f1b214463d",
"name": "Firmus MFB"
},
{
"id": "611ff10f412b11f1b2144648",
"name": "Kredi Money MFB LTD"
},
{
"id": "611ff10f412b11f1b2144653",
"name": "Links MFB"
},
{
"id": "611ff110412b11f1b2144669",
"name": "Parallex Bank"
},
{
"id": "611ff110412b11f1b2144675",
"name": "Paycom"
},
{
"id": "6155de8e8b740800a304c48b",
"name": "Okra, Inc"
},
{
"id": "62028144ac2b39359fc3cf49",
"name": "Bidvest Bank"
},
{
"id": "620383c7ac2b39359fc99309",
"name": "African Bank"
},
{
"id": "6215fa7c6709f197ad344b8e",
"name": "Lotus Bank"
},
{
"id": "62365abc55cfdd29194c76db",
"name": "Discovery Bank"
}
]


# Create a dictionary of banks for quick lookup
banks = {bank['id']: bank['name'] for bank in bank_data}

# Update the bank names in the data
for key in data:
    bank_id = data[key]['bank']
    if bank_id in banks:
        data[key]['bank'] = banks[bank_id]

# Write the updated data back to the file
with open('data.json', 'w') as file:
    json.dump(data, file, indent=4)
