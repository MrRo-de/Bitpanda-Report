#!/usr/bin/env python 
import csv
import os
#import io
import copy
import pyqrcode
from datetime import datetime #, timedelta
import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # logo
        #self.image('fox_face.png', 10, 8, 25)
        # font
        self.set_font('times', 'B', 20)
        # Title
        self.cell(0, 0, 'Bitpanda Report', ln=True, align = 'C')
        # line break
        self.ln(10)

    def footer(self):
        # set position of the footer
        self.set_y(-15)
        # set font
        self.set_font('times', 'I', 10)
        # Date
        self.cell(0, 10, f'{today.strftime("%d/%m/%Y")}', align = 'L')
        # Page number
        self.cell(0, 10, f'{self.page_no()}/nb', align = 'R')

def removeFiles(gotNames):
    for rows in gotNames:
        if os.path.exists(f"{rows}.png"):
            os.remove(f"{rows}.png")
    if os.path.exists('newTempFile0x123.csv'):
        os.remove('newTempFile0x123.csv')

def generatePieChart(assets_Account, titleName):
    # Pie Chart
    x_list = []
    label_list = []
    for row in range(len(assets_Account)):
        x_list.append(assets_Account[row]["Amount"])
        label_list.append(f'{assets_Account[row]["Asset"]}\n({assets_Account[row]["Amount"]})')
    plt.axis("equal") # Kreisdiagramm rund gestaltet (sonst Standard: oval!)
    plt.pie(x_list, labels=label_list, autopct="%1.1f%%")
    plt.title(titleName)
    plt.savefig(f'{titleName}.png', bbox_inches='tight')
    #print(f'{titleName} generated')
    plt.close()

    return titleName

csv_path_to_file = ''
csv_filename = ''
if csv_path_to_file == '':
    path_input = input("Pfad zur csv-Datei (Drag&Drop, remove ''): ")
    csv_Oldpath = os.path.join(path_input)
else:
    csv_Oldpath = os.path.join(csv_path_to_file, csv_filename)

os_Name = os.name
if os_Name == 'posix':
    csvDf = pd.read_csv(csv_Oldpath, skiprows=6)
elif os_Name == 'nt':
    csvDf = pd.read_csv(csv_Oldpath, skiprows=6)
else:
    csvDf = pd.read_csv(csv_Oldpath, skiprows=6)
csvDf.to_csv('newTempFile0x123.csv', index=False)
newPath_input = 'newTempFile0x123.csv'
csv_path = os.path.join(newPath_input)
input_file = csv.DictReader(open(csv_path))

gitlink = 'https://github.com/MrRo-de/Bitpanda-Report'

disclaimer_eng = '- Disclaimer: All data is without guarantee, errors and changes are reserved. -'
disclaimer_deu = '- Haftungsausschluss: Alle Angaben ohne Gewähr, Irrtümer und Änderungen vorbehalten. -'

today = datetime.today()
print(f"heute ist der {today}\n")

full_name = input('Dein Namen:\n')
street = input('Straße, Hausnummer:\n')
postcode_city = input('PLZ und Ort:\n')
"""
full_name = ''
street = ''
postcode_city = ''
""" 
input_file = csv.DictReader(open(csv_path))
fiat_assets = []
metal_assets = []
crypto_assets = []
stock_assets = []

################################################################################################
#################### Find all Assets [Fiat, Metal, Cryptocurrency, Stocks] #####################
################################################################################################

for row in input_file:
    if row['Asset class'] == 'Fiat':
        fiat_assets.append(row["Asset"])
    elif row['Asset class'] == 'Metal':
        metal_assets.append(row["Asset"])
    elif row['Asset class'] == 'Cryptocurrency':
        crypto_assets.append(row["Asset"])
    elif row['Asset class'] == 'Stock (derivative)':
        stock_assets.append(row["Asset"])
    

fiat_assets = set(fiat_assets)
metal_assets = set(metal_assets)
crypto_assets = set(crypto_assets)
stock_assets = set(stock_assets)

fiat_list = []
#print(fiat_assets)
fiat_paid = 0.00

for asset in fiat_assets:

    input_file = csv.DictReader(open(csv_path))
    fiat_amount = 0.00

    for row in input_file :
        if asset == row["Asset"]:
            if row["Amount Fiat"] == '-':
                row["Amount Fiat"] = '0.00'
            if row['Fee'] == '-':
                row['Fee'] = '0.00'

            if (row['Transaction Type'] == 'buy'):
                fiat_amount += float(row["Amount Fiat"])
            elif (row['Transaction Type'] == 'sell'):
                fiat_amount -= float(row["Amount Fiat"])
            elif (row['Transaction Type'] == 'deposit'):
                fiat_amount += float(row["Amount Fiat"])
            elif (row['Transaction Type'] == 'withdrawal'):
                fiat_amount -= float(row["Amount Fiat"])
            elif (row['Transaction Type'] == 'transfer'):
                if (row['In/Out'] == 'outgoing'):
                    fiat_amount -= float(row["Amount Fiat"])
                elif (row['In/Out'] == 'incoming'):
                    fiat_amount += float(row["Amount Fiat"])

            if (float(row['Fee']) >= 0.00):
                fiat_amount -= float(row['Fee'])

    fiat_amount = '{:.2f}'.format(fiat_amount)
    if float(fiat_amount) > 0.0:
        fiat_list.append({"Asset": asset, "Amount": fiat_amount})

#print(fiat_list)

metal_list = []
#print(metal_assets)
for asset in metal_assets:

    input_file = csv.DictReader(open(csv_path))
    metal_amount = 0.00

    for row in input_file :
        if asset == row["Asset"]:
            if row["Amount Asset"] == '-':
                row["Amount Asset"] = '0.00'
            if row['Fee'] == '-':
                row['Fee'] = '0.00'

            if (row['Transaction Type'] == 'buy'):
                metal_amount += float(row["Amount Asset"])
                fiat_paid -= float(row["Amount Fiat"])
            elif (row['Transaction Type'] == 'sell'):
                metal_amount -= float(row["Amount Asset"])
                fiat_paid += float(row["Amount Fiat"])
            elif (row['Transaction Type'] == 'deposit'):
                metal_amount += float(row["Amount Asset"])
            elif (row['Transaction Type'] == 'withdrawal'):
                metal_amount -= float(row["Amount Asset"])
            elif (row['Transaction Type'] == 'transfer'):
                metal_amount += float(row["Amount Asset"])

            if (float(row['Fee']) >= 0.00):
                metal_amount -= float(row['Fee'])

    metal_amount = '{:.6f}'.format(metal_amount)
    if float(metal_amount) > 0.000000:
        metal_list.append({"Asset": asset, "Amount": metal_amount})

#print(metal_list)

crypto_list = []
#print(crypto_assets)
for asset in crypto_assets:

    input_file = csv.DictReader(open(csv_path))
    crypto_amount = 0.00

    for row in input_file :
        if asset == row["Asset"]:
            if row["Amount Asset"] == '-':
                row["Amount Asset"] = '0.00'
            if row['Fee'] == '-':
                row['Fee'] = '0.00'

            if (row['Transaction Type'] == 'buy'):
                crypto_amount += float(row["Amount Asset"])
                fiat_paid -= float(row["Amount Fiat"])
            elif (row['Transaction Type'] == 'sell'):
                crypto_amount -= float(row["Amount Asset"])
                fiat_paid += float(row["Amount Fiat"])
            elif (row['Transaction Type'] == 'deposit'):
                crypto_amount += float(row["Amount Asset"])
            elif (row['Transaction Type'] == 'withdrawal'):
                crypto_amount -= float(row["Amount Asset"])
            elif (row['Transaction Type'] == 'transfer'):
                crypto_amount += float(row["Amount Asset"])

            if (float(row['Fee']) >= 0.00):
                crypto_amount -= float(row['Fee'])

    crypto_amount = '{:.6f}'.format(crypto_amount)
    if float(crypto_amount) > 0.000000:
        crypto_list.append({"Asset": asset, "Amount": crypto_amount})

#print(crypto_list)

stock_list = []
for asset in stock_assets:

    input_file = csv.DictReader(open(csv_path))
    stock_amount = 0.00

    for row in input_file :
        if asset == row["Asset"]:
            if row["Amount Asset"] == '-':
                row["Amount Asset"] = '0.00'
            if row['Fee'] == '-':
                row['Fee'] = '0.00'

            if (row['Transaction Type'] == 'buy'):
                stock_amount += float(row["Amount Asset"])
                fiat_paid -= float(row["Amount Fiat"])
            elif (row['Transaction Type'] == 'sell'):
                stock_amount -= float(row["Amount Asset"])
                fiat_paid += float(row["Amount Fiat"])
            elif (row['Transaction Type'] == 'deposit'):
                stock_amount += float(row["Amount Asset"])
            elif (row['Transaction Type'] == 'withdrawal'):
                stock_amount -= float(row["Amount Asset"])
            elif (row['Transaction Type'] == 'transfer'):
                stock_amount += float(row["Amount Asset"])

            if (float(row['Fee']) >= 0.00):
                stock_amount -= float(row['Fee'])

    stock_amount = '{:.6f}'.format(stock_amount)
    if float(crypto_amount) > 0.000000:
        stock_list.append({"Asset": asset, "Amount": stock_amount})

#print(stock_list)
#fiat_list = [{'Asset': 'USD', 'Amount': '985.00'}, {'Asset': 'EUR', 'Amount': '-1465.00'}, {'Asset': 'CHZ', 'Amount': '-0.00'}]
for row in fiat_list:
    if row["Asset"] == 'EUR':
        old = float(row["Amount"])
        calc = old + fiat_paid
        if calc == -0.00:
            calc = 0.00
        if calc <= 0.00:
            calc = 0.00
        
        row["Amount"] = '{:.2f}'.format(calc)
        
 
#print(fiat_list)

################################################################################################
################################ Generate Pie Charts ###########################################
################################################################################################


numberOfCharts = 0
listOfPNG = []

temp_fiat_list = copy.deepcopy(fiat_list)
fiat_list.clear()
for row in temp_fiat_list:
    if abs(float(row['Amount'])) != 0.000000:
        fiat_list.append(row)
#print(fiat_list)
if len(fiat_list) > 0:
    listOfPNG.append(generatePieChart(fiat_list, 'Dein Fiat Portfolio'))
    numberOfCharts += 1

temp_metal_list = copy.deepcopy(metal_list)
metal_list.clear()
for row in temp_metal_list:
    if abs(float(row['Amount'])) != 0.000000:
        metal_list.append(row)
#print(metal_list)
if len(metal_list) > 0:
    listOfPNG.append(generatePieChart(metal_list, 'Dein Metal Portfolio'))
    numberOfCharts += 1

temp_crypto_list = copy.deepcopy(crypto_list)
crypto_list.clear()
for row in temp_crypto_list:
    if abs(float(row['Amount'])) != 0.000000:
        crypto_list.append(row)
#print(crypto_list)
if len(crypto_list) > 0:
    listOfPNG.append(generatePieChart(crypto_list, 'Dein Crypto Portfolio'))
    numberOfCharts += 1

temp_stock_list = copy.deepcopy(stock_list)
stock_list.clear()
for row in temp_stock_list:
    if abs(float(row['Amount'])) != 0.000000:
        stock_list.append(row)
#print(stock_list)
if len(stock_list) > 0:
    listOfPNG.append(generatePieChart(stock_list, 'Dein Stock Portfolio'))
    numberOfCharts += 1


################################################################################################
################################# Get all Transactions #########################################
################################################################################################


input_file = csv.DictReader(open(csv_path))
csvDate_format = '%Y-%m-%d'
csvTime_format = '%H:%M:%S'

fiat_in_dict = []
metal_in_dict = []
crypto_in_dict = []
stock_in_dict = []
fiat_out_dict = []
metal_out_dict = []
crypto_out_dict = []
stock_out_dict = [] 

temp_fiat_dict = []
temp_metal_dict = []
temp_crypto_dict = []
temp_stock_dict = []

for row in input_file:
    date = datetime.strptime(row['Timestamp'][:10], csvDate_format)
    time = datetime.strptime(row['Timestamp'][11:19], csvTime_format)
    if row['Asset class'] == 'Fiat':
        if (row['Transaction Type'] == 'buy'):
            fiat_in_dict.append({"Datum": f'{date.date()} {time.time()}', "Transaktion": "Kauf", "Betrag": row["Amount Fiat"], "Asset": row["Fiat"], "Gebühren": row["Fee"]})
        elif (row['Transaction Type'] == 'sell'):
            fiat_out_dict.append({"Datum": f'{date.date()} {time.time()}', "Transaktion": "Verkauf", "Betrag": row["Amount Fiat"], "Asset": row["Fiat"], "Gebühren": row["Fee"]})
        elif (row['Transaction Type'] == 'deposit'):
            fiat_in_dict.append({"Datum": f'{date.date()} {time.time()}', "Transaktion": "einzahlen", "Betrag": row["Amount Fiat"], "Asset": row["Fiat"], "Gebühren": row["Fee"]})
        elif (row['Transaction Type'] == 'withdrawal'):
            fiat_out_dict.append({"Datum": f'{date.date()} {time.time()}', "Transaktion": "auszahlen", "Betrag": row["Amount Fiat"], "Asset": row["Fiat"], "Gebühren": row["Fee"]})
        elif (row['Transaction Type'] == 'transfer'):
            if (row['In/Out'] == 'outgoing'):
                fiat_out_dict.append({"Datum": f'{date.date()} {time.time()}', "Transaktion": "versenden", "Betrag": row["Amount Fiat"], "Asset": row["Fiat"], "Gebühren": row["Fee"]})
            elif (row['In/Out'] == 'incoming'):
                fiat_in_dict.append({"Datum": f'{date.date()} {time.time()}', "Transaktion": "empfangen", "Betrag": row["Amount Fiat"], "Asset": row["Fiat"], "Gebühren": row["Fee"]})
    elif row['Asset class'] == 'Metal':
        if (row['Transaction Type'] == 'buy'):
            metal_in_dict.append({"Datum": f'{date.date()} {time.time()}', "Transaktion": "Kauf", "Betrag": row["Amount Fiat"], "Asset Menge": row["Amount Asset"], "Asset Preis": row["Asset market price"], "Asset": row["Asset"], "Gebühren": row["Fee"]})
        elif (row['Transaction Type'] == 'sell'):
            metal_out_dict.append({"Datum": f'{date.date()} {time.time()}', "Transaktion": "Verkauf", "Betrag": row["Amount Fiat"], "Asset Menge": row["Amount Asset"], "Asset Preis": row["Asset market price"], "Asset": row["Asset"], "Gebühren": row["Fee"]})
        elif (row['Transaction Type'] == 'deposit'):
            metal_in_dict.append({"Datum": f'{date.date()} {time.time()}', "Transaktion": "einzahlen", "Betrag": row["Amount Fiat"], "Asset Menge": row["Amount Asset"], "Asset Preis": row["Asset market price"], "Asset": row["Asset"], "Gebühren": row["Fee"]})
        elif (row['Transaction Type'] == 'withdrawal'):
            metal_out_dict.append({"Datum": f'{date.date()} {time.time()}', "Transaktion": "auszahlen", "Betrag": row["Amount Fiat"], "Asset Menge": row["Amount Asset"], "Asset Preis": row["Asset market price"], "Asset": row["Asset"], "Gebühren": row["Fee"]})
        elif (row['Transaction Type'] == 'transfer'):
            metal_in_dict.append({"Datum": f'{date.date()} {time.time()}', "Transaktion": "erhalten", "Betrag": row["Amount Fiat"], "Asset Menge": row["Amount Asset"], "Asset Preis": row["Asset market price"], "Asset": row["Asset"], "Gebühren": row["Fee"]})
    elif row['Asset class'] == 'Cryptocurrency':
        if (row['Transaction Type'] == 'buy'):
            crypto_in_dict.append({"Datum": f'{date.date()} {time.time()}', "Transaktion": "Kauf", "Betrag": row["Amount Fiat"], "Asset Menge": row["Amount Asset"], "Asset Preis": row["Asset market price"], "Asset": row["Asset"], "Gebühren": row["Fee"]})
        elif (row['Transaction Type'] == 'sell'):
            crypto_out_dict.append({"Datum": f'{date.date()} {time.time()}', "Transaktion": "Verkauf", "Betrag": row["Amount Fiat"], "Asset Menge": row["Amount Asset"], "Asset Preis": row["Asset market price"], "Asset": row["Asset"], "Gebühren": row["Fee"]})
        elif (row['Transaction Type'] == 'deposit'):
            crypto_in_dict.append({"Datum": f'{date.date()} {time.time()}', "Transaktion": "empfangen", "Betrag": row["Amount Fiat"], "Asset Menge": row["Amount Asset"], "Asset Preis": row["Asset market price"], "Asset": row["Asset"], "Gebühren": row["Fee"]})
        elif (row['Transaction Type'] == 'withdrawal'):
            crypto_out_dict.append({"Datum": f'{date.date()} {time.time()}', "Transaktion": "versenden", "Betrag": row["Amount Fiat"], "Asset Menge": row["Amount Asset"], "Asset Preis": row["Asset market price"], "Asset": row["Asset"], "Gebühren": row["Fee"]})
        elif (row['Transaction Type'] == 'transfer'):
            if row['Asset'] == 'BEST':
                crypto_in_dict.append({"Datum": f'{date.date()} {time.time()}', "Transaktion": "Rewards", "Betrag": row["Amount Fiat"], "Asset Menge": row["Amount Asset"], "Asset Preis": row["Asset market price"], "Asset": row["Asset"], "Gebühren": row["Fee"]})
            else:
                crypto_in_dict.append({"Datum": f'{date.date()} {time.time()}', "Transaktion": "erhalten", "Betrag": row["Amount Fiat"], "Asset Menge": row["Amount Asset"], "Asset Preis": row["Asset market price"], "Asset": row["Asset"], "Gebühren": row["Fee"]})
    elif row['Asset class'] == 'Stock (derivative)':
        if (row['Transaction Type'] == 'buy'):
            stock_in_dict.append({"Datum": f'{date.date()} {time.time()}', "Transaktion": "Kauf", "Betrag": row["Amount Fiat"], "Asset Menge": row["Amount Asset"], "Asset Preis": row["Asset market price"], "Asset": row["Asset"], "Gebühren": row["Fee"]})
        elif (row['Transaction Type'] == 'sell'):
            stock_out_dict.append({"Datum": f'{date.date()} {time.time()}', "Transaktion": "Verkauf", "Betrag": row["Amount Fiat"], "Asset Menge": row["Amount Asset"], "Asset Preis": row["Asset market price"], "Asset": row["Asset"], "Gebühren": row["Fee"]})
        elif (row['Transaction Type'] == 'deposit'):
            stock_in_dict.append({"Datum": f'{date.date()} {time.time()}', "Transaktion": "empfangen", "Betrag": row["Amount Fiat"], "Asset Menge": row["Amount Asset"], "Asset Preis": row["Asset market price"], "Asset": row["Asset"], "Gebühren": row["Fee"]})
        elif (row['Transaction Type'] == 'withdrawal'):
            stock_out_dict.append({"Datum": f'{date.date()} {time.time()}', "Transaktion": "versenden", "Betrag": row["Amount Fiat"], "Asset Menge": row["Amount Asset"], "Asset Preis": row["Asset market price"], "Asset": row["Asset"], "Gebühren": row["Fee"]})
        elif (row['Transaction Type'] == 'transfer'):
            if row['Asset'] == 'BEST':  # Ist integriert für den Fall von Dividenden / Muss jedoch angepasst werden.
                stock_in_dict.append({"Datum": f'{date.date()} {time.time()}', "Transaktion": "Rewards", "Betrag": row["Amount Fiat"], "Asset Menge": row["Amount Asset"], "Asset Preis": row["Asset market price"], "Asset": row["Asset"], "Gebühren": row["Fee"]})
            else:
                stock_in_dict.append({"Datum": f'{date.date()} {time.time()}', "Transaktion": "erhalten", "Betrag": row["Amount Fiat"], "Asset Menge": row["Amount Asset"], "Asset Preis": row["Asset market price"], "Asset": row["Asset"], "Gebühren": row["Fee"]})

fiat_in_dict = sorted(fiat_in_dict, key=lambda k: k['Datum'])
fiat_out_dict = sorted(fiat_out_dict, key=lambda k: k['Datum'])
metal_in_dict = sorted(metal_in_dict, key=lambda k: k['Datum'])
metal_out_dict = sorted(metal_out_dict, key=lambda k: k['Datum'])
crypto_in_dict = sorted(crypto_in_dict, key=lambda k: k['Datum'])
crypto_out_dict = sorted(crypto_out_dict, key=lambda k: k['Datum'])
stock_in_dict = sorted(stock_in_dict, key=lambda k: k['Datum'])
stock_out_dict = sorted(stock_out_dict, key=lambda k: k['Datum'])

temp_fiat_dict = fiat_in_dict + fiat_out_dict
temp_metal_dict = metal_in_dict + metal_out_dict
temp_crypto_dict = crypto_in_dict + crypto_out_dict
temp_stock_dict = stock_in_dict + stock_out_dict

temp_fiat_dict = sorted(temp_fiat_dict, key=lambda k: k['Datum'])
temp_metal_dict = sorted(temp_metal_dict, key=lambda k: k['Datum'])
temp_crypto_dict = sorted(temp_crypto_dict, key=lambda k: k['Datum'])
temp_stock_dict = sorted(temp_stock_dict, key=lambda k: k['Datum'])


################################################################################################
############################### Calculate Win and Losses #######################################
################################################################################################


metal_winloss = []
temp_metal_steuern = []
metal_steuern = []
metal_portfolio = []
crypto_winloss = []
temp_crypto_steuern = []
crypto_steuern = []
crypto_portfolio = []
stock_winloss = []
temp_stock_steuern = []
stock_steuern = []
stock_portfolio = []
steuern = []
steuernCalc = []

#{"Asset": asset, "HODL": days.days, "Jahr": year.year, "winLoss": '{:.2f}'.format(temp_win_loss)}
def calcMetalSteuern(asset, winloss):
    temp_year = datetime.strptime('1990-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    temp_toPay = 0.00
    temp_Asset = ''
    for row in winloss:
        if row['Asset'][-1] == '*':
            temp_Asset = row['Asset'][:-1]
        else:
            temp_Asset = row['Asset']
        if asset == temp_Asset:
            if int(row['HODL']) <= 365:
                if row['Jahr'] == temp_year:
                    temp_toPay += float(row['winLoss'])
                else:
                    if temp_toPay != 0.00:
                        steuernCalc.append({"Asset": row['Asset'], "verkaufs Jahr": temp_year, "Betrag": temp_toPay})
                    temp_toPay = float(row['winLoss'])
                    temp_year = row['Jahr']
                    
    if temp_toPay != 0.00:
        steuernCalc.append({"Asset": row['Asset'], "verkaufs Jahr": temp_year, "Betrag": temp_toPay})
    return steuernCalc

def calcCryptoSteuern(asset, winloss):
    temp_year = datetime.strptime('1990-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    temp_toPay = 0.00
    temp_Asset = ''
    for row in winloss:
        if row['Asset'][-1] == '*':
            temp_Asset = row['Asset'][:-1]
        else:
            temp_Asset = row['Asset']
        if asset == temp_Asset:
            if int(row['HODL']) <= 365:
                if row['Jahr'] == temp_year:
                    temp_toPay += float(row['winLoss'])
                else:
                    if temp_toPay != 0.00:
                        steuernCalc.append({"Asset": row['Asset'], "verkaufs Jahr": temp_year, "Betrag": temp_toPay})
                    temp_toPay = float(row['winLoss'])
                    temp_year = row['Jahr'] 
                    
    if temp_toPay != 0.00:
        steuernCalc.append({"Asset": row['Asset'], "verkaufs Jahr": temp_year, "Betrag": temp_toPay})
    return steuernCalc

def calcStockSteuern(asset, winloss):
    temp_year = datetime.strptime('1990-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    temp_toPay = 0.00
    temp_Asset = ''
    for row in winloss:
        if row['Asset'][-1] == '*':
            temp_Asset = row['Asset'][:-1]
        else:
            temp_Asset = row['Asset']
        if asset == temp_Asset:
            if row['Jahr'] == temp_year:
                temp_toPay += float(row['winLoss'])
            else:
                if temp_toPay != 0.00:
                    steuernCalc.append({"Asset": row['Asset'], "verkaufs Jahr": temp_year, "Betrag": temp_toPay})
                temp_toPay = float(row['winLoss'])
                temp_year = row['Jahr']
                    
    if temp_toPay != 0.00:
        steuernCalc.append({"Asset": row['Asset'], "verkaufs Jahr": temp_year, "Betrag": temp_toPay})
    return steuernCalc

def calcWinLoss(in_dict, assets, out_dict, asset_class):

    test = ''
    winloss = []
    steuern_winloss = []
    steuern_metal = []
    steuern_crypto = []
    steuern_stock = []
    temp_winloss = []
    portfolio_dict = []
    for asset in assets:
        hint = False
        temp_in_dict = []
        for row_in in in_dict:
            if row_in['Asset'] == asset:
                if row_in['Betrag'] == '-':
                    row_in['Betrag'] = 0.00
                if row_in['Gebühren'] == '-':
                    row_in['Gebühren'] = 0.00
                if row_in["Transaktion"] == 'empfangen':
                    hint = True
                temp_in_dict.append({"Datum": row_in['Datum'], "Transaktion": row_in['Transaktion'], "Betrag": '{:.2f}'.format(float(row_in["Betrag"])), "Asset Menge": '{:.6f}'.format(float(row_in["Asset Menge"])), "Asset Preis": '{:.2f}'.format(float(row_in["Asset Preis"])), "Asset": row_in["Asset"], "Gebühren": '{:.6f}'.format(float(row_in["Gebühren"]))})


        temp_in_dict = sorted(temp_in_dict, key=lambda k: k['Datum'])

        temp_out_dict = []
        for row_out in out_dict:
            if row_out['Asset'] == asset:
                if row_out['Betrag'] == '-':
                    row_out['Betrag'] = 0.00
                if row_out['Gebühren'] == '-':
                    row_out['Gebühren'] = 0.00
                temp_out_dict.append({"Datum": row_out['Datum'], "Transaktion": row_out['Transaktion'], "Betrag": '{:.2f}'.format(float(row_out["Betrag"])), "Asset Menge": '{:.6f}'.format(float(row_out["Asset Menge"])), "Asset Preis": '{:.2f}'.format(float(row_out["Asset Preis"])), "Asset": row_out["Asset"], "Gebühren": '{:.6f}'.format(float(row_out["Gebühren"]))})

        temp_out_dict = sorted(temp_out_dict, key=lambda k: k['Datum'])

        win_loss = 0.00
        temp_win_loss = 0.00
        temp2_win_loss = 0.00
        #index = 0
        for row_out in temp_out_dict:
            temp_win_loss = 0.00
            if row_out['Asset'] == asset:
                days = datetime.strptime(row_out["Datum"], '%Y-%m-%d %H:%M:%S')-datetime.strptime(temp_in_dict[0]["Datum"], '%Y-%m-%d %H:%M:%S')   
                year = datetime.strptime(row_out['Datum'], '%Y-%m-%d %H:%M:%S')
                if float(row_out['Asset Menge']) == 0.000000:
                    row_out['Asset Menge'] = row_out['Gebühren']
                
                if len(temp_in_dict) > 0:
                    if float(row_out['Asset Menge']) > float(temp_in_dict[0]['Asset Menge']):
                        temp2_win_loss = 0.00
                        while float(row_out['Asset Menge']) > float(temp_in_dict[0]['Asset Menge']):
                            #print(f'1: {len(temp_in_dict)}')
                            if row_out['Transaktion'] == 'Verkauf':
                                temp2_win_loss += (float(temp_in_dict[0]['Asset Menge']) * float(row_out['Asset Preis'])) - float(temp_in_dict[0]['Betrag'])
                            row_out['Betrag'] = '{:.2f}'.format((float(row_out['Asset Menge']) - float(temp_in_dict[0]['Asset Menge'])) * float(row_out['Asset Preis']))
                            row_out['Asset Menge'] = '{:.6f}'.format(float(row_out['Asset Menge']) - float(temp_in_dict[0]['Asset Menge']))
                            
                            if len(temp_in_dict) > 0:
                                del temp_in_dict[0]
                            else:
                                temp_in_dict[0]['Betrag'] = 0.00
                                temp_in_dict[0]['Asset Menge'] = 0.000000
                            
                            if float(row_out['Asset Menge']) < 0.00000:
                                #print('break because of Amount')
                                break
                            #print(f'2: {len(temp_in_dict)}')
                            if len(temp_in_dict) == 0:
                                #print('break because of length')
                                break
                            
                                
                        temp_win_loss += temp2_win_loss

                    if len(temp_in_dict) > 0:
                        if float(row_out['Asset Menge']) == float(temp_in_dict[0]['Asset Menge']):
                            if row_out['Transaktion'] == 'Verkauf':
                                temp_win_loss = temp_win_loss + (float(row_out['Betrag']) - float(temp_in_dict[0]['Betrag']))
                            if len(temp_in_dict) > 0:
                                del temp_in_dict[0]
                            else:
                                temp_in_dict[0]['Betrag'] = 0.00
                                temp_in_dict[0]['Asset Menge'] = 0.000000
                        elif float(row_out['Asset Menge']) < float(temp_in_dict[0]['Asset Menge']):
                            temp_in_dict[0]['Betrag'] = '{:.2f}'.format((float(temp_in_dict[0]['Asset Menge']) - float(row_out['Asset Menge'])) * float(temp_in_dict[0]['Asset Preis']))
                            temp_in_dict[0]['Asset Menge'] = '{:.6f}'.format((float(temp_in_dict[0]['Asset Menge']) - float(row_out['Asset Menge'])))
                            if row_out['Transaktion'] == 'Verkauf':
                                temp_win_loss = temp_win_loss + (float(row_out['Betrag']) - (float(temp_in_dict[0]['Asset Preis']) * float(row_out['Asset Menge'])))

            win_loss += temp_win_loss
            if hint == True:
                steuern_winloss.append({"Asset": f'{asset}*', "HODL": days.days, "Jahr": year.year, "winLoss": '{:.2f}'.format(temp_win_loss)})
                #hint = False
            else:
                steuern_winloss.append({"Asset": asset, "HODL": days.days, "Jahr": year.year, "winLoss": '{:.2f}'.format(temp_win_loss)})

            if asset == test:
                print(win_loss)
                print(temp_win_loss)
        temp_win_loss = 0.00
        temp_winloss.clear()

        if len(temp_in_dict) > 0:
            for row in temp_in_dict:
                if float(row['Asset Menge']) > 0.0:
                    portfolio_dict.append(row)
                
        winloss.append({"Asset": asset, "winLoss": '{:.2f}'.format(win_loss)})

        if win_loss != 0.00:
            if asset_class == 'metal':
                steuern_metal = calcMetalSteuern(asset, steuern_winloss)
            elif asset_class == 'crypto':
                steuern_crypto = calcCryptoSteuern(asset, steuern_winloss)
            elif asset_class == 'stock':
                steuern_stock = calcStockSteuern(asset, steuern_winloss)
        else:
            if asset_class == 'metal':
                steuern_metal.append({"Asset": asset, "verkaufs Jahr": 1990, "Betrag": 0.00})
            elif asset_class == 'crypto':
                steuern_crypto.append({"Asset": asset, "verkaufs Jahr": 1990, "Betrag": 0.00})
            elif asset_class == 'stock':
                steuern_stock.append({"Asset": asset, "verkaufs Jahr": 1990, "Betrag": 0.00})

    
    if asset_class == 'metal':
        return winloss, steuern_metal, portfolio_dict
    if asset_class == 'crypto':
        return winloss, steuern_crypto, portfolio_dict
    if asset_class == 'stock':
        return winloss, steuern_stock, portfolio_dict


################################################################################################
################################## Generate PDF File ###########################################
################################################################################################


# create FPDF object
# Layout ('P', 'L')
# Unit ('mm', 'cm', 'in')
# Format ('A3', 'A4' (default), 'A5', 'Letter', 'Legal', (100,150))
pdf = PDF('P', 'mm')
pdf_width = 210
pdf_height = 297
# get total page numbers
pdf.alias_nb_pages(alias='nb')

# Add a Page
pdf.add_page()

# specify font
# fonts ('times', 'courier', 'helvetica', 'symbol', 'zpfdingbats')
# 'B' (bold), 'U' (underline), 'I' (italic), '' (regular), combination (i.e. ('BU'))
pdf.set_font('times', '', 14)

# Set auto page break
pdf.set_auto_page_break(auto=True, margin = 15)


################################################################################################
##################################### First PDF Page ###########################################
################################################################################################

fiat_assets = sorted(fiat_assets, key=lambda k: k)
metal_assets = sorted(metal_assets, key=lambda k: k)
crypto_assets = sorted(crypto_assets, key=lambda k: k)
stock_assets = sorted(stock_assets, key=lambda k: k)
'''
if os.path.exists("Dein Fiat Portfolio.png"):
    print('Fiat PNG exists')
if os.path.exists("Dein Crypto Portfolio.png"):
    print('Crypto PNG exists')
if os.path.exists("Dein Metal Portfolio.png"):
    print('Metal PNG exists')
if os.path.exists("Dein Stock Portfolio.png"):
    print('Stock PNG exists')
'''
# Add text
# w = width
# h = height
# txt = your text
# ln (0 False; 1 True - move cursor down to next line)
# border (0 False; 1 True - add border around cell)
pdf.ln(5)
pdf.cell(40, 8, f"{full_name}", ln=True, border=False)
pdf.cell(40, 8, f"{street}", ln=True)
pdf.cell(40, 8, f"{postcode_city}", ln=True)
pdf.ln(6)
pdf.set_font('times', 'B', 10)
pdf.cell(40, 8, f"Du hast gehandelt mit:\n", ln=True)
pdf.ln(3)
pdf.set_font('times', 'B', 10)
pdf.cell(40, 8, "Fiat\n", ln=True)
pdf.set_font('times', '', 10)
pdf.cell(40, 8, f"{fiat_assets}\n", ln=True)
pdf.set_font('times', 'B', 10)
pdf.cell(40, 8, "Metal\n", ln=True)
pdf.set_font('times', '', 10)
pdf.cell(40, 8, f"{metal_assets}\n", ln=True)
pdf.set_font('times', 'B', 10)
pdf.cell(40, 8, "Crypto\n", ln=True)
pdf.set_font('times', '', 10)
pdf.cell(40, 8, f"{crypto_assets}\n", ln=True)
pdf.set_font('times', 'B', 10)
pdf.cell(40, 8, "Aktien\n", ln=True)
pdf.set_font('times', '', 10)
pdf.cell(40, 8, f"{stock_assets}\n", ln=True)
if numberOfCharts == 4:
    if os.path.exists("Dein Fiat Portfolio.png"):
        pdf.image('Dein Fiat Portfolio.png', pdf_width-85, 140, 70)
    if os.path.exists("Dein Metal Portfolio.png"):
        pdf.image('Dein Metal Portfolio.png', 15, 200, 70)
    if os.path.exists("Dein Crypto Portfolio.png"):
        pdf.image('Dein Crypto Portfolio.png', 15, 140, 70)
    if os.path.exists("Dein Stock Portfolio.png"):
        pdf.image('Dein Stock Portfolio.png', pdf_width-85, 200, 70)
elif numberOfCharts == 3:
    count = 0
    if os.path.exists("Dein Fiat Portfolio.png"):
        if count == 0:
            pdf.image('Dein Fiat Portfolio.png', 15, 140, 70)
        elif count ==1:
            pdf.image('Dein Fiat Portfolio.png', pdf_width-85, 140, 70)
        else:
            pdf.image('Dein Fiat Portfolio.png', (pdf_width/2)-35, 200, 70)
        count += 1
    if os.path.exists("Dein Metal Portfolio.png"):
        if count == 0:
            pdf.image('Dein Metal Portfolio.png', 15, 140, 70)
        elif count == 1:
            pdf.image('Dein Metal Portfolio.png', pdf_width-85, 140, 70)
        else:
            pdf.image('Dein Metal Portfolio.png', (pdf_width/2)-35, 200, 70)
        count += 1
    if os.path.exists("Dein Crypto Portfolio.png"):
        if count == 0:
            pdf.image('Dein Crypto Portfolio.png', 15, 140, 70)
        elif count == 1:
            pdf.image('Dein Crypto Portfolio.png', pdf_width-85, 140, 70)
        else:
            pdf.image('Dein Crypto Portfolio.png', (pdf_width/2)-35, 200, 70)
        count += 1
    if os.path.exists("Dein Stock Portfolio.png"):
        if count == 0:
            pdf.image('Dein Stock Portfolio.png', 15, 140, 70)
        elif count == 1:
            pdf.image('Dein Stock Portfolio.png', pdf_width-85, 140, 70)
        else:
            pdf.image('Dein Stock Portfolio.png', (pdf_width/2)-35, 200, 70)
        count += 1
elif numberOfCharts == 2:
    count = 0
    if os.path.exists("Dein Fiat Portfolio.png"):
        if count == 0:
            pdf.image('Dein Fiat Portfolio.png', 15, 140, 100)
        else:
            pdf.image('Dein Fiat Portfolio.png', pdf_width-115, 140, 100)
        count += 1
    if os.path.exists("Dein Metal Portfolio.png"):
        if count == 0:
            pdf.image('Dein Metal Portfolio.png', 15, 140, 100)
        else:
            pdf.image('Dein Metal Portfolio.png', pdf_width-115, 140, 100)
        count += 1
    if os.path.exists("Dein Crypto Portfolio.png"):
        if count == 0:
            pdf.image('Dein Crypto Portfolio.png', 15, 140, 100)
        else:
            pdf.image('Dein Crypto Portfolio.png', pdf_width-115, 140, 100)
        count += 1
    if os.path.exists("Dein Stock Portfolio.png"):
        if count == 0:
            pdf.image('Dein Stock Portfolio.png', 15, 140, 100)
        else:
            pdf.image('Dein Stock Portfolio.png', pdf_width-115, 140, 100)
        count += 1
elif numberOfCharts == 1:
    if os.path.exists("Dein Fiat Portfolio.png"):
        pdf.image('Dein Fiat Portfolio.png', (pdf_width/2)-75, 140, 150)
    if os.path.exists("Dein Metal Portfolio.png"):
        pdf.image('Dein Metal Portfolio.png', (pdf_width/2)-75, 140, 150)
    if os.path.exists("Dein Crypto Portfolio.png"):
        pdf.image('Dein Crypto Portfolio.png', (pdf_width/2)-75, 140, 150)
    if os.path.exists("Dein Stock Portfolio.png"):
        pdf.image('Dein Stock Portfolio.png', (pdf_width/2)-75, 140, 150)

pdf.ln(140)
pdf.set_font('times', 'I', 12)
pdf.cell(0, 0, disclaimer_deu, ln=True, align="C")
pdf.ln(5)
pdf.set_font('times', '', 10)
pdf.cell(0, 0, disclaimer_eng, ln=True, align="C")
pdf.ln(5)
pdf.set_font('times', '', 10)


################################################################################################
############################# Detailed Transaction Pages #######################################
################################################################################################


def generateFiatTransactionPages(temp_dict_sorted, asset_set, asset_class):

    asset_set = sorted(asset_set, key=lambda k: k)

    for asset in asset_set:
        
        pdf.add_page()
        pdf.set_font('times', 'B', 10)
        pdf.cell(40, 8, f"Details der {asset} {asset_class} Transaktionen:\n", ln=True)
        pdf.set_font('times', '', 10)
        pdf.ln(5)
        col_width = (pdf_width-30)/4
        pdf.set_font('times', 'B', 10)
        th = pdf.font_size+2
        pdf.cell(col_width, th, "Datum", align='C', border=1)
        pdf.cell(col_width, th, "Transaktion", align='C', border=1)
        pdf.cell(col_width, th, "Betrag", align='C', border=1)
        pdf.cell(col_width, th, "Gebühren", align='C', border=1)
        pdf.ln(th)
        pdf.set_font('times', '', 9)
        th = pdf.font_size+2
        for row in temp_dict_sorted:
            if row['Asset'] == asset:
                pdf.cell(col_width, th, str(row["Datum"]), border=1)
                pdf.cell(col_width, th, str(row["Transaktion"]), border=1)
                pdf.cell(col_width, th, str(row["Betrag"]), border=1)
                pdf.cell(col_width, th, str(row["Gebühren"]), border=1)
                pdf.ln(th)

def generateTransactionPages(temp_dict_sorted, asset_set, winloss, asset_class):

    for asset in asset_set:
        hint = False        
        pdf.add_page()
        pdf.set_font('times', 'B', 10)
        pdf.cell(40, 8, f"Details der {asset} {asset_class} Transaktionen:\n", ln=True)
        pdf.set_font('times', '', 10)
        pdf.ln(5)
        col_width = (pdf_width-30)/6
        pdf.set_font('times', 'B', 10)
        th = pdf.font_size+2
        pdf.cell(col_width, th, "Datum", align='C', border=1)
        pdf.cell(col_width, th, "Transaktion", align='C', border=1)
        pdf.cell(col_width, th, "Betrag", align='C', border=1)
        pdf.cell(col_width, th, "Asset Menge", align='C', border=1)
        pdf.cell(col_width, th, "Asset Preis", align='C', border=1)
        pdf.cell(col_width, th, "Gebühren", align='C', border=1)
        pdf.ln(th)
        pdf.set_font('times', '', 9)
        th = pdf.font_size+2
        for row in temp_dict_sorted:
            if row['Asset'] == asset:
                if row["Transaktion"] == 'empfangen':
                    hint = True
                pdf.cell(col_width, th, str(row["Datum"]), border=1)
                pdf.cell(col_width, th, str(row["Transaktion"]), border=1)
                pdf.cell(col_width, th, str(row["Betrag"]), border=1)
                pdf.cell(col_width, th, str(row["Asset Menge"]), border=1)
                pdf.cell(col_width, th, str(row["Asset Preis"]), border=1)
                pdf.cell(col_width, th, str(row["Gebühren"]), border=1)
                pdf.ln(th)
 
        for rows in winloss:
            if rows['Asset'] == asset:
                pdf.ln(th*2)
                pdf.set_font('times', 'B', 10)
                pdf.cell(45, th, f"Gewinn/Verlust: ")
                if float(rows['winLoss']) < 0.0:
                    pdf.set_text_color(225, 0, 0)
                elif float(rows['winLoss']) > 0.0:
                    pdf.set_text_color(0, 225, 0)
                else:
                    pdf.set_text_color(0, 0, 0)
                pdf.cell(100, th,f" {'{:.2f}'.format(float(rows['winLoss']))} EUR", ln=True)
                pdf.set_font('times', '', 10)
                pdf.set_text_color(0, 0, 0)

        if hint == True:
            pdf.set_text_color(225, 0, 0)
            pdf.ln(th)
            pdf.cell(45, th, f"* Durch das Einzahlen des Assets ist eine genaue Berechnung nicht möglich.")
            pdf.set_text_color(0, 0, 0)
            hint = False

temp_metal_in_dict = copy.deepcopy(metal_in_dict)
temp_metal_out_dict = copy.deepcopy(metal_out_dict)
temp_metal_assets = copy.deepcopy(metal_assets)

temp_crypto_in_dict = copy.deepcopy(crypto_in_dict)
temp_crypto_out_dict = copy.deepcopy(crypto_out_dict)
temp_crypto_assets = copy.deepcopy(crypto_assets)

temp_stock_in_dict = copy.deepcopy(stock_in_dict)
temp_stock_out_dict = copy.deepcopy(stock_out_dict)
temp_stock_assets = copy.deepcopy(stock_assets)

steuernCalc.clear()
metal_winloss, temp_metal_steuern, metal_portfolio = calcWinLoss(temp_metal_in_dict, temp_metal_assets, temp_metal_out_dict, 'metal')
metal_steuern = copy.deepcopy(temp_metal_steuern)

steuernCalc.clear()
crypto_winloss, temp_crypto_steuern, crypto_portfolio = calcWinLoss(temp_crypto_in_dict, temp_crypto_assets, temp_crypto_out_dict, 'crypto')
crypto_steuern = copy.deepcopy(temp_crypto_steuern)

steuernCalc.clear()
stock_winloss, temp_stock_steuern, stock_portfolio = calcWinLoss(temp_stock_in_dict, temp_stock_assets, temp_stock_out_dict, 'stock')
stock_steuern = copy.deepcopy(temp_stock_steuern)

generateFiatTransactionPages(temp_fiat_dict, fiat_assets, 'Fiat')
generateTransactionPages(temp_metal_dict, metal_assets, metal_winloss, 'Metal')
generateTransactionPages(temp_crypto_dict, crypto_assets, crypto_winloss, 'Crypto')
generateTransactionPages(temp_stock_dict, stock_assets, stock_winloss, 'Aktien')


################################################################################################
################################## Steuern Deutschland #########################################
################################################################################################


def generateTaxPage(steuern, asset_class):

    pdf.add_page()
    pdf.ln(5)
    pdf.set_font('times', 'B', 10)
    pdf.cell(40, 8,f"Welchen Gewinn muss ich Versteuern:", ln=True)
    pdf.set_font('times', '', 10)
    pdf.ln(3)
    if asset_class == 'stock':
        pdf.cell(0, 0,f"Für Aktien in Deutschland (Jede Veräußerung muss versteuert werden)", ln=True, align='C')
    elif asset_class == 'metal':
        pdf.cell(0, 0,f"Für Edelmetalle in Deutschland (Steuerfrei bei Haltefrist länger als 1 Jahr)", ln=True, align='C')
    elif asset_class == 'crypto':
        pdf.cell(0, 0,f"Für Cryptowährungen in Deutschland (Steuerfrei bei Haltefrist länger als 1 Jahr)", ln=True, align='C')
    pdf.ln(12)
    col_width = (pdf_width-30)/3
    th = pdf.font_size+2
    pdf.set_font('times', 'B', 10)
    pdf.cell(col_width, th, "Asset", align='C', border=1)
    pdf.cell(col_width, th, "relevantes Jahr", align='C', border=1)
    pdf.cell(col_width, th, "Betrag", align='C', border=1)
    pdf.ln(th)
    pdf.set_font('times', '', 9)
    for row in steuern:
        pdf.cell(col_width, th, row["Asset"], border=1)
        pdf.cell(col_width, th, str(row["verkaufs Jahr"]), align='C', border=1)
        if float(row["Betrag"]) < 0.0:
            pdf.set_text_color(225, 0, 0)
        elif float(row["Betrag"]) > 0.0:
            pdf.set_text_color(0, 225, 0)
        pdf.cell(col_width, th, '{:.2f}'.format(row["Betrag"]), align='C', border=1)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(th)

    pdf.cell(45, th, f"* Durch das Einzahlen des Assets ist eine genaue Berechnung nicht möglich.")
    pdf.ln(16)

    temp_year = steuern[0]["verkaufs Jahr"]
    zahlendeSteuern = 0.00
    for row in steuern:
        if temp_year == row["verkaufs Jahr"]:
            zahlendeSteuern += float(row["Betrag"])
        else:
            if temp_year == today.year:
                pdf.cell(45, th, f"In {temp_year} sind bis jetzt Gewinne/Verluste im Wert von {'{:.2f}'.format(zahlendeSteuern)} angefallen.")
                pdf.ln(6)
            else:
                pdf.cell(45, th, f"In {temp_year} sind Gewinne/Verluste im Wert von {'{:.2f}'.format(zahlendeSteuern)} angefallen.")
                pdf.ln(6)
            zahlendeSteuern = float(row["Betrag"])
            temp_year = row["verkaufs Jahr"]

    if zahlendeSteuern != 0.00:
        if temp_year == today.year:
            pdf.cell(45, th, f"In {temp_year} sind bis jetzt Gewinne/Verluste im Wert von {'{:.2f}'.format(zahlendeSteuern)} angefallen.")
            pdf.ln(6)
        else:
            pdf.cell(45, th, f"In {temp_year} sind Gewinne/Verluste im Wert von {'{:.2f}'.format(zahlendeSteuern)} angefallen.")
            pdf.ln(6)

metal_steuern = sorted(metal_steuern, key=lambda k: (k["verkaufs Jahr"], k["Asset"]))
crypto_steuern = sorted(crypto_steuern, key=lambda k: (k["verkaufs Jahr"], k["Asset"]))
stock_steuern = sorted(stock_steuern, key=lambda k: (k["verkaufs Jahr"], k["Asset"]))

if metal_steuern[0]["verkaufs Jahr"] != 1990:
    generateTaxPage(metal_steuern, 'metal')
if crypto_steuern[0]["verkaufs Jahr"] != 1990:
    generateTaxPage(crypto_steuern, 'crypto')
if stock_steuern[0]["verkaufs Jahr"] != 1990:
    generateTaxPage(stock_steuern, 'stock')

def summaryTax(metal, crypto, stock, all_years, fiat):

    for year in all_years:
        pdf.add_page()
        th = pdf.font_size+2
        pdf.ln(5)
        pdf.set_font('times', 'B', 12)
        pdf.cell(40, 8,f"Zusammenfassung Steuern {year}:", ln=True)
        pdf.set_font('times', '', 10)
        pdf.ln(th*3)
        amount = 0.00
        temp_amount = 0.00
        if len(metal) > 0:
            pdf.set_font('times', 'B', 10)
            pdf.cell(0, 0,f"Edelmetalle", ln=True)
            pdf.set_font('times', '', 10)
            pdf.ln(th)
            for row in metal:
                if row["verkaufs Jahr"] == year:
                    pdf.ln(th)
                    pdf.cell(0, 0, f'{row["Asset"]}', ln=True)
                    pdf.cell(0, 0, f'{"                                     {:.2f}".format(row["Betrag"])} {fiat}', align='R', ln=True)
                    temp_amount += float(row["Betrag"])
            amount += temp_amount
            pdf.ln(th)
            pdf.cell(0, 0, f'_____________________________________________________________________________________________________________', ln=True)
            pdf.ln(th)
            pdf.cell(0, 0, f'                                       {"{:.2f}".format(temp_amount)} {fiat}', align='R', ln=True)
            pdf.ln(th*2)
            
        temp_amount = 0.00
        if len(crypto) > 0:
            pdf.set_font('times', 'B', 10)
            pdf.cell(0, 0,f"Cryptowährungen", ln=True)
            pdf.set_font('times', '', 10)
            pdf.ln(th)
            for row in crypto:
                if row["verkaufs Jahr"] == year:
                    pdf.ln(th)
                    pdf.cell(0, 0, f'{row["Asset"]}', ln=True)
                    pdf.cell(0, 0, f'{"                                     {:.2f}".format(row["Betrag"])} {fiat}', align='R', ln=True)
                    temp_amount += float(row["Betrag"])
            amount += temp_amount
            pdf.ln(th)
            pdf.cell(0, 0, f'_____________________________________________________________________________________________________________', ln=True)
            pdf.ln(th)
            pdf.cell(0, 0, f'{"                                       {:.2f}".format(temp_amount)} {fiat}', align='R', ln=True)
            pdf.ln(th*2)
        
        temp_amount = 0.00
        if len(stock) > 0:
            pdf.set_font('times', 'B', 10)
            pdf.cell(0, 0,f"Aktien", ln=True)
            pdf.set_font('times', '', 10)
            pdf.ln(th)
            for row in stock:
                if row["verkaufs Jahr"] == year:
                    pdf.ln(th)
                    pdf.cell(0, 0, f'{row["Asset"]}', ln=True)
                    pdf.cell(0, 0, f'                                       {"{:.2f}".format(row["Betrag"])} {fiat}', align='R', ln=True)
                    temp_amount += float(row["Betrag"])
            amount += temp_amount
            pdf.ln(th)
            pdf.cell(0, 0, f'_____________________________________________________________________________________________________________', ln=True)
            pdf.ln(th)
            pdf.cell(0, 0, f'                                       {"{:.2f}".format(temp_amount)} {fiat}', align='R', ln=True)
            pdf.ln(th*2)

        pdf.ln(th*4)
        pdf.set_font('times', 'B', 11)
        if year == today.year:
            pdf.cell(45, th, f"In {year} sind bis jetzt Gewinne/Verluste im Wert von {'{:.2f}'.format(amount)} {fiat} zu versteuern.")
            pdf.ln(6)
        else:
            pdf.cell(45, th, f"In {year} sind Gewinne/Verluste im Wert von {'{:.2f}'.format(amount)} {fiat} zu versteuern.")
            pdf.ln(6)
        
        pdf.ln(6)
        pdf.set_font('times', '', 9)
        pdf.cell(45, th, f"*gezahlte Gebühren werden derzeit noch nicht mit verrechnet, da die *csv Datei keine Asset Preise für Gebühren zur verfügung stellt.", ln=True)
        


years_tax = []
for row in metal_steuern:
    if row['verkaufs Jahr'] > 1990:
        years_tax.append(row['verkaufs Jahr'])
for row in crypto_steuern:
    if row['verkaufs Jahr'] > 1990:
        years_tax.append(row['verkaufs Jahr'])
for row in stock_steuern:
    if row['verkaufs Jahr'] > 1990:
        years_tax.append(row['verkaufs Jahr'])

years_tax = set(years_tax)

currency = fiat_assets[0]

summaryTax(metal_steuern, crypto_steuern, stock_steuern, years_tax, currency)


################################################################################################
################################## Aktuelles Portfolio #########################################
################################################################################################


def assetsInPortfolio(assets_list, in_dict, asset_class):
    
    #print(assets_list)
    if len(in_dict) > 0:
        pdf.add_page()
        pdf.ln(5)
        pdf.set_font('times', 'B', 10)
        pdf.cell(40, 8,f"Diese Vermögenswerte, der Anlageklasse {asset_class}, sollten in deinem Portfolio sein:", ln=True)
        pdf.set_font('times', '', 10)
        pdf.ln(12)
        col_width = (pdf_width-30)/6
        pdf.set_font('times', 'B', 10)
        th = pdf.font_size+2
        
        pdf.cell(col_width, th, "Datum", align='C', border=1)
        pdf.cell(col_width, th, "Transaktion", align='C', border=1)
        pdf.cell(col_width, th, "Betrag", align='C', border=1)
        pdf.cell(col_width, th, "Asset Menge", align='C', border=1)
        pdf.cell(col_width, th, "Asset Preis", align='C', border=1)
        pdf.cell(col_width, th, "HODL Zeit", align='C', border=1)
        pdf.ln(th)
        pdf.set_font('times', '', 9)
        temp_asset = ''
        temp_Amount = 0.00
        temp_Price = 0.00
        hodl_amount = 0.00
        for row in in_dict:
            diftime = today - datetime.strptime(row["Datum"], '%Y-%m-%d %H:%M:%S')
            if row["Asset"] != temp_asset:
                if temp_Price > 0.00:
                    col_width = (pdf_width-30)
                    if hodl_amount > 0.00:
                        pdf.cell(col_width, th, f"Haltefrist 1 Jahr+: {'{:.6f}'.format(hodl_amount)} {temp_asset}", align="R",  border=1)
                        pdf.ln(th)
                    else:
                        pdf.cell(col_width, th, '',  border=1)
                        pdf.ln(th)
                    pdf.cell(col_width, th, f"Investiert: {'{:.2f}'.format(temp_Price)}", align="R", border=1)
                    pdf.ln(th)
                    pdf.cell(col_width, th, f"Gesamt Menge: {'{:.6f}'.format(temp_Amount)} {temp_asset}", align="R",  border=1)
                    pdf.ln(th)
                    pdf.cell(col_width, th, f"Durchschnitt Preis: {'{:.3f}'.format(temp_Price/temp_Amount)}", align="R", border=1)
                    pdf.ln(th)
                temp_asset = row["Asset"]
                pdf.set_font('times', 'B', 10)
                col_width = (pdf_width-30)
                pdf.cell(col_width, th, row["Asset"], align='C', border=1)
                col_width = (pdf_width-30)/6
                pdf.set_font('times', '', 9)
                temp_Amount = 0.00
                temp_Price = 0.00
                pdf.ln(th)
            
            col_width = (pdf_width-30)/6
            pdf.cell(col_width, th, str(row["Datum"]), border=1)
            pdf.cell(col_width, th, str(row["Transaktion"]), border=1)
            pdf.cell(col_width, th, str(row["Betrag"]), border=1)
            pdf.cell(col_width, th, str(row["Asset Menge"]), border=1)
            pdf.cell(col_width, th, str(row["Asset Preis"]), border=1)
            if float(diftime.days) > 365:
                pdf.set_text_color(0, 255, 0)
                hodl_amount += float(row['Asset Menge'])
            pdf.cell(col_width, th, str(diftime.days), border=1)
            pdf.ln(th)
            pdf.set_text_color(0, 0, 0)
            temp_Amount += float(row["Asset Menge"])
            if row['Betrag'] != '':
                temp_Price += float(row["Betrag"])
        
        col_width = (pdf_width-30)/4
        if temp_Price > 0.00:
            col_width = (pdf_width-30)
            if hodl_amount > 0.00:
                pdf.cell(col_width, th, f"Haltefrist 1 Jahr+: {'{:.6f}'.format(hodl_amount)} {temp_asset}", align="R",  border=1)
                pdf.ln(th)
            else:
                pdf.cell(col_width, th, '',  border=1)
                pdf.ln(th)
            pdf.cell(col_width, th, f"Investiert: {'{:.2f}'.format(temp_Price)}", align="R", border=1)
            pdf.ln(th)
            pdf.cell(col_width, th, f"Gesamt Menge: {'{:.6f}'.format(temp_Amount)} {temp_asset}", align="R",  border=1)
            pdf.ln(th)
            pdf.cell(col_width, th, f"Durchschnitt Preis: {'{:.3f}'.format(temp_Price/temp_Amount)}", align="R", border=1)
            pdf.ln(th)


if len(metal_portfolio) > 0:
    fin_metal_portfolio = []
    temp_metal_list = []
    for row in metal_list:
        temp_metal_list.append(row['Asset'])
    for row in metal_portfolio:
        if row['Asset'] in temp_metal_list:
            fin_metal_portfolio.append(row)
    assetsInPortfolio(metal_list, fin_metal_portfolio, 'Metal')

if len(crypto_portfolio) > 0:
    fin_crypto_portfolio = []
    temp_crypto_list = []
    for row in crypto_list:
        temp_crypto_list.append(row['Asset'])
    for row in crypto_portfolio:
        if row['Asset'] in temp_crypto_list:
            fin_crypto_portfolio.append(row)
    assetsInPortfolio(crypto_list, fin_crypto_portfolio, 'Crypto')

if len(stock_portfolio) > 0:
    fin_stock_portfolio = []
    temp_stock_list = []
    for row in stock_list:
        temp_stock_list.append(row['Asset'])
    for row in stock_portfolio:
        if row['Asset'] in temp_stock_list:
            fin_stock_portfolio.append(row)
    assetsInPortfolio(stock_list, fin_stock_portfolio, 'Aktien')


################################################################################################
##################################### Last PDF Page ############################################
################################################################################################


btc_adress = 'bc1q09w7rac565vr7dtqvc2j6sv9f8fa4mscv9ct0s'
best_adress = '0x34Fc219cDE52D31BE23D6fA83448B2d1903Df4FD'
iota_adress = 'iota1qqffgg8cmwlh3dqss7s2u6fsl83007505j98zjpqjq9je3ca30cfccrs2uy'

btc_code = pyqrcode.create(btc_adress)
btc_code.png('btc1.png', scale=1, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xff])
listOfPNG.append('btc1')
iota_code = pyqrcode.create(iota_adress)
iota_code.png('iota1.png', scale=1, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xff])
listOfPNG.append('iota1')
best_code = pyqrcode.create(best_adress)
best_code.png('best1.png', scale=1, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xff])
listOfPNG.append('best1')

pdf.add_page()
pdf.ln(5)
pdf.cell(40, 8,f"Gefällt dir diese Anwendung, dann würde ich mich über eine Spende freuen.", ln=True)
pdf.set_font('times', '', 10)
pdf.ln(20)
pdf.cell(40, 8, f"Bitcoin:\n", ln=True)
pdf.image('btc1.png', 100, 55, 20)
pdf.ln(20)
pdf.cell(0, 0, f"{btc_adress}\n", ln=True, align = 'C')
pdf.ln(16)
pdf.cell(40, 8, f"IOTA:\n", ln=True)
pdf.image('iota1.png', 100, 100, 20)
pdf.ln(20)
pdf.cell(0, 0, f"{iota_adress}\n", ln=True, align = 'C')
pdf.ln(16)
pdf.cell(40, 8, f"BEST:\n", ln=True)
pdf.image('best1.png', 100, 145, 20)
pdf.ln(20)
pdf.cell(0, 0, f"{best_adress}\n", ln=True, align = 'C')
pdf.ln(20)
pdf.cell(40, 8,f"Vielen Dank.", ln=True)
pdf.ln(20)
pdf.cell(40, 8,f"Das Script zur Erstellung dieses PDF findet Ihr unter:", ln=True)
pdf.ln(5)
pdf.cell(0, 0,f"{gitlink}", link=gitlink, ln=True, align = 'C')
pdf.ln(20)
pdf.cell(40, 8,f"Hier könnt Ihr auch gerne unter \"Issues\" einen \"New Issue\" anlegen um mir Fehler und Verbesserungsvorschläge zukommen zu lassen.", ln=True)
user = os.environ['USER']
pdf.output(f'/Users/{user}/Desktop/BP-Report.pdf')

removeFiles(listOfPNG)