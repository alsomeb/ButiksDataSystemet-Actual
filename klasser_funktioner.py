from datetime import datetime

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


# Funktioner
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