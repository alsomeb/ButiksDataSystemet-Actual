from datetime import datetime
import os

class Produkt:
    def __init__(self, produktid, pris, typ, namn):
        self._produktid = produktid
        self._pris = float(pris)
        self._typ = typ
        self._namn = namn

    def GetProduktId(self):
        return self._produktid

    def GetPrice(self):
        return self._pris

    def GetNamn(self):
        return self._namn
    
    def SetNamn(self, namn:str):
        self._namn = namn


class Kassa():
    def __init__(self):
        self._produkter = [] # Innehåller alla produkter
        self._kvittoRad = [] # String Lista = Skriva ut kvittoraderna för användaren
        self._totalsumma = 0
        self._date = ""

    def SetTotalPriceReceiptZero(self)->int:
        self._totalsumma = 0

    def GetTotalPriceReceipt(self, price:float)->float:
        self._totalsumma = self._totalsumma + price
        return self._totalsumma

    def GetDate(self)->str:
        self._date = datetime.now()
        tid = self._date.strftime("%Y-%m-%d %H:%M:%S")
        return tid
        
    def AddProdukt(self, produkt:Produkt):
        self._produkter.append(produkt)

    def FindProdukt(self, id:str)->bool:
        for i in self._produkter:
            if i.GetProduktId() == id:
                return True
        return None

    def KvittoRadTotal(self, id:str, antal:float):
        for i in self._produkter:
            if i.GetProduktId() == id:
                return i.GetPrice() * antal
        return False

    def GetProduktPris(self, id:str)->float:
        for produkt in self._produkter:
            if produkt.GetProduktId() == id:
                return produkt.GetPrice()

    def GetProduktNamn(self, id:str)->str:
        for produkt in self._produkter:
            if produkt.GetProduktId() == id:
                return produkt.GetNamn()

    def AddToReceipt(self, id:str, antal:str, total:str)->list:
        for p in self._produkter:
            if p.GetProduktId() == id:
                self._kvittoRad.append(f"{p.GetNamn()} {antal} * {p.GetPrice()} = {total}")
                return self._kvittoRad    

    def ShowAllProducts(self)->list:
        produkter = []
        for produkt in self._produkter:
            produkter.append(f"{produkt.GetNamn()}")
        return produkter

    def FindProduktNamn(self, namn:str)->bool:
        for i in self._produkter:
            if i.GetNamn() == namn:
                return True
        return False

    def ChangeProduktNamn(self, namn:str, nyttNamn:str):
        for produkt in self._produkter:
            if produkt.GetNamn() == namn:
                produkt.SetNamn(nyttNamn)


# Andra Funktioner
def getInputBetween(startval: int, endval: int)->int:
    while True:
        try:
            val = int(input("Mata in: "))
            if val >= startval and val <= endval:
                return val
            print(f"Ogiltigt val, mellan {startval} och {endval}, tack")
        except:
            print("Ange ett tal tack!")

def ReadProducts(objekt:Kassa):
    with open("produkter.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            line = line.split(",")
            objekt.AddProdukt(Produkt(line[0], float(line[1]), line[2], line[3].replace("\n","")))

def nyKund(kassasystemet:object):
    lock_time = False # Låser tiden för ett kvitto, sedan släpper tiden för ny kund när LOOP reset
    while True:
        print("\nkommandon:\n<productid> <antal>\nPAY")
        cmd = input("kommando: ").upper()
        cmdsplit = cmd.split(" ")
        if cmd == "PAY":
            print("Skapar kvitto..")
            SaveReceipt(kundvagn_lista, total_price_receipt, tid)
            kundvagn_lista.clear() # Rensar listan för ny användning
            kassasystemet.SetTotalPriceReceiptZero() # Sätter totalen till 0 för ny kund  
            return
        elif len(cmdsplit) == 2 and kassasystemet.FindProdukt(cmdsplit[0]) == True and cmdsplit[1].isnumeric():
            total_per_rad = kassasystemet.KvittoRadTotal(cmdsplit[0], float(cmdsplit[1])) # = total för 1 rad i kvittot
            kundvagn_lista = kassasystemet.AddToReceipt(cmdsplit[0], cmdsplit[1], total_per_rad) # Används för att printa ut på skärmen kassaRader
            total_price_receipt = kassasystemet.GetTotalPriceReceipt(total_per_rad) # = Total per kvitto
            if lock_time == False:
                tid = kassasystemet.GetDate()
                lock_time = True
            PrintShoppingCart(tid, kundvagn_lista, total_price_receipt)
        else:
            print("Ogiltig inmatning!")

def PrintShoppingCart(tid:str, shoppinglista:list, total_price_receipt:float):
        print(f"\nKVITTO: {tid}")
        for rad in shoppinglista:
            print(rad)
        print(f"Total: {total_price_receipt}")

def GetReceiptNumber():
    with open("Kvittonr.txt", "r") as kvittoFil:
        number = kvittoFil.readline()
        newnumber = int(number) + 1
        with open("Kvittonr.txt", "w") as numberfile:
            numberfile.write(str(newnumber))
    return number

def SaveReceipt(kvitto:list, total:float, tid:str):
    kvittonr = GetReceiptNumber()
    date = datetime.now()
    date = date.strftime("%Y%m%d")
    with open(f"RECEIPT_{date}.txt", "a") as receiptFile:
        receiptFile.write(f"KVITTO: {kvittonr} {tid}\n")
        for line in kvitto:
            receiptFile.write(f"{str(line)}\n")
        receiptFile.write(f"Total: {str(total)} KR\n")
        receiptFile.write("\n")

# Funktioner admin
def FileOpen(filename:str)->str:
    with open(filename) as file:
        lines = file.readlines()
        return lines

def listSpecReceipt(date:str)->str:
    for file in os.listdir("."):
        if file.endswith(f"{date}.txt"):
            return file


def findFile(date:str)->bool:
    for file in os.listdir("."):
        if file.endswith(f"{date}.txt"):
            return True
    return False

def receiptAdminSearch(input_str)->str:
    if len(input_str) < 8 or input_str.isnumeric() == False:
        print("Fel datum format, format(yyyymmdd)")
    elif findFile(input_str) == False:
        print("Kvittonr finns ej!")
    else:
        file_located = listSpecReceipt(input_str)
        current_file = FileOpen(f"{file_located}")
        for lines in current_file:
            if lines.startswith("KVITTO:") or lines.startswith("Total:"):
                print(lines)
        fullreceipt = input("Vill du se fullständigt kvitto från alla den dagen? y/n: ").lower()
        if fullreceipt == "y":
            for lines in current_file:
                print(lines)

def printAllProductNames(kassasystemet:object):
    allProducts = kassasystemet.ShowAllProducts()
    for produkt in allProducts:
        print(produkt)

def admin(kassasystemet:object): #Objektet inskickat i funktionen
    while True:
        print()
        print("1. Sök kvitto")
        print("2. Ändra namn produkt")
        print("3. Ändra pris produkt")
        print("4. Lägg till CampaignPrice på produkt")
        print("0. Återgå huvudmeny")

        sel = getInputBetween(0,4)
        if sel == 0:
            return

        if sel == 1:
            input_str = input("\nAnge datum, tex 20211020: ")
            receiptAdminSearch(input_str)
        
        if sel == 2:
            print()
            printAllProductNames(kassasystemet)
            val = input("Ange namn på produkt du vill ändra namn på: ").capitalize()
            if kassasystemet.FindProduktNamn(val) == True:
                nyttNamn = input("Ange nytt namn: ").capitalize()
                if kassasystemet.FindProduktNamn(nyttNamn) == False:
                    with open("Produkter.txt", "r") as produktfil:
                        filedata = produktfil.read()
                        filedata = filedata.replace(val,nyttNamn)
                    with open("Produkter.txt", "w") as produktfil:
                        produktfil.write(filedata)
                    kassasystemet.ChangeProduktNamn(val,nyttNamn) #Så man inte behöver starta om för ändringar live
                else:
                    print("Namnet du angav finns redan")
            else:
                print("Produkt med det namnet finns inte, kontrollera stavning")
        
        if sel == 3:
            pass #ATT GÖRA