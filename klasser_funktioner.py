from datetime import datetime
import os

class Produkt:
    def __init__(self, produktid, pris, typ, namn, CampaignStartDate, CampaignEndDate):
        self._produktid = produktid
        self._pris = float(pris)
        self._typ = typ
        self._namn = namn
        self._CampaignStartDate = CampaignStartDate
        self._CampaignEndDate = CampaignEndDate

    def GetProduktId(self)->str:
        return self._produktid

    def GetPrice(self)->float: #Används för live prisjustering med kampanj
        if self.isCampaign() == True:
            price = self._pris / 2
        else:
            price = self._pris
        return price

    def GetNonCampPrice(self)->float: #används för org priset i admin menyn
        return self._pris

    def GetNamn(self)->str:
        return self._namn
    
    def SetNamn(self, namn:str):
        self._namn = namn

    def SetPrice(self, price:float):
        self._pris = price

    def getCampaignStartDate(self)->datetime:
        date_time_str = self._CampaignStartDate 
        date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d")
        return date_time_obj

    def getCampaignStartDateSTRING(self)->str:
        return self._CampaignStartDate
    
    def getCampaignEndDateSTRING(self)->str:
        return self._CampaignEndDate

    def getCampaignEndDate(self)->datetime:
        date_time_str = self._CampaignEndDate
        date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d")
        return date_time_obj

    def setCampaignStartDate(self, new:str):
        self._CampaignStartDate = new

    def setCampaignEndDate(self, new:str):
        self._CampaignEndDate = new

    def isCampaign(self)->bool:
        now = datetime.now()
        start = self.getCampaignStartDate()
        end = self.getCampaignEndDate()
        if start <= now <= end: # Kollar ifall now hamnar mellan/= start och end
            return True
        return False
        

class Kassa():
    def __init__(self):
        self._produkter = [] # Innehåller alla produkter
        self._kvittoRad = [] # String Lista = Skriva ut kvittoraderna för användaren
        self._totalsumma = 0
        self._date = "" #funk GetDate hämtar datum

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
        return False

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
    

    def ShowAllProductsPrices(self)->list:
        produkter = []
        for produkt in self._produkter:
            produkter.append(f"ID: {produkt.GetProduktId()}, {produkt.GetNamn()} - Pris: {produkt.GetNonCampPrice()}")
        return produkter

    def ShowAllCampaignDates(self)->list:
        dates = []
        for produkt in self._produkter:
            dates.append(f"ID: {produkt.GetProduktId()} Namn: {produkt.GetNamn()}\nStart: {produkt.getCampaignStartDate()}\nSlut: {produkt.getCampaignEndDate()}\n")
        return dates

    def FindProduktNamn(self, namn:str)->bool:
        for i in self._produkter:
            if i.GetNamn() == namn:
                return True
        return False

    def FindProduktPris(self, id:str)->float:
        for produkt in self._produkter:
            if produkt.GetProduktId() == id:
                return produkt.GetPrice()

    def FindProduktCampStart(self, id:str)->str:
        for produkt in self._produkter:
            if produkt.GetProduktId() == id:
                return produkt.getCampaignStartDateSTRING()

    def FindProduktCampEnd(self, id:str)->str:
        for produkt in self._produkter:
            if produkt.GetProduktId() == id:
                return produkt.getCampaignEndDateSTRING()

    def ChangeProduktPrice(self, id:str, newprice:float):
        for produkt in self._produkter:
            if produkt.GetProduktId() == id:
                produkt.SetPrice(newprice)

    def ChangeProduktNamn(self, namn:str, nyttNamn:str):
        for produkt in self._produkter:
            if produkt.GetNamn() == namn:
                produkt.SetNamn(nyttNamn)

    def ChangeCampStartDate(self, id:str, nytt:str):
        for produkt in self._produkter:
            if produkt.GetProduktId() == id:
                produkt.setCampaignStartDate(nytt)

    def ChangeCampEndDate(self, id:str, nytt:str):
        for produkt in self._produkter:
            if produkt.GetProduktId() == id:
                produkt.setCampaignEndDate(nytt)


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
            objekt.AddProdukt(Produkt(line[0], float(line[1]), line[2], line[3], line[4], line[5].replace("\n","")))

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

def printAllProductPrices(kassasystemet:object):
    allProductsPrices = kassasystemet.ShowAllProductsPrices()
    for produkt in allProductsPrices:
        print(produkt)

def is_number_float(string:str)->bool:
    try:
        float(string)
        return True
    except ValueError:
        return False

def ChangeNameProductMenu(kassasystemet:object):
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
                    kassasystemet.ChangeProduktNamn(val,nyttNamn) #behöver ej starta om för ändringar live i program
                else:
                    print("Namnet du angav finns redan")
            else:
                print("Produkt med det namnet finns inte, kontrollera stavning")

def ShowAllCampDates(kassasystemet:object):
    allCampaignDates = kassasystemet.ShowAllCampaignDates()
    for dates in allCampaignDates:
        print(dates)

def isDate(date_string:str)->bool:
    date_string = date_string
    format = "%Y-%m-%d"
    try:
        datetime.strptime(date_string, format)
        return True
    except ValueError:
        return False

def ChangePriceMenu(kassasystemet:object):
    printAllProductPrices(kassasystemet)
    id = input("Ange id på produkt du vill ändra pris på: ")
    if len(id) != 3 or id.isnumeric() == False:
        print("3 siffror, tack!")
    produktens_current_price = kassasystemet.FindProduktPris(id) #hämtar nuvarande pris fr class
    if kassasystemet.FindProdukt(id) == True:
        nyttPris = input("Ange nytt pris: ")
        if is_number_float(nyttPris) == False: # Egengjord checker
            print("Inga bokstäver tillåtna")
        else:
            with open("produkter.txt", "r") as produktfil:
                new = []
                for rad in produktfil.readlines():
                    if rad.startswith(id):
                        new.append(rad.replace(str(produktens_current_price),nyttPris))
                    else:
                        new.append(rad)
            with open("produkter.txt", "w") as produktfil:
                for rad in new:
                    produktfil.write(rad)
            kassasystemet.ChangeProduktPrice(id,float(nyttPris)) #Upd priset live i programmet även

def ChangeCampDateMenu(kassasystemet:object):
    ShowAllCampDates(kassasystemet)
    id_prod = input("Ange ID på produkt du vill ändra datum för: ").capitalize()
    if len(id_prod) != 3 or id_prod.isnumeric() == False:
        print("3 siffror, tack!")
    produktens_current_start = kassasystemet.FindProduktCampStart(id_prod) #hämtar fr class nuvrande datum
    produktens_current_slut = kassasystemet.FindProduktCampEnd(id_prod)
    if kassasystemet.FindProdukt(id_prod) == True:
        nyttStartDatum = input("Ange Startdatum i format YYYY-MM-DD: ")
        nyttSlutDatum = input("Ange Slutdatum i format YYYY-MM-DD: ")  
        if isDate(nyttStartDatum) == True and isDate(nyttSlutDatum) == True: # Egen checker på date
            with open("produkter.txt", "r") as prodfile:
                newlines = []
                for line in prodfile.readlines(): #Startdatum
                    if line.startswith(id_prod):
                        newlines.append(line.replace(produktens_current_start,nyttStartDatum))
                    else:
                        newlines.append(line)
            with open("produkter.txt", "w") as prodfile:
                for line in newlines:
                    prodfile.write(line)

            with open("produkter.txt", "r") as prodfile: #Slutdatum
                newlines = []
                for line in prodfile.readlines():
                    if line.startswith(id_prod):
                        newlines.append(line.replace(produktens_current_slut,nyttSlutDatum))
                    else:
                        newlines.append(line)
            with open("produkter.txt", "w") as prodfile:
                for line in newlines:
                    prodfile.write(line)
            kassasystemet.ChangeCampStartDate(id_prod, nyttStartDatum) #Updaterar live i programmet
            kassasystemet.ChangeCampEndDate(id_prod, nyttSlutDatum)            
        else:
            print("Fel format, YYYY-MM-DD endast!")



def admin(kassasystemet:object): #Objektet inskickat i funktionen
    while True:
        print()
        print("1. Sök kvitto")
        print("2. Ändra namn produkt")
        print("3. Ändra pris produkt")
        print("4. Ändra Kampanjdatum på produkt")
        print("0. Återgå huvudmeny")

        sel = getInputBetween(0,4)
        if sel == 0:
            return

        if sel == 1:
            input_str = input("\nAnge datum, tex 20211020: ")
            receiptAdminSearch(input_str)
        
        if sel == 2:
            print()
            ChangeNameProductMenu(kassasystemet)
    
        if sel == 3: # Snygga till, kanske en fin funk ?
            print()
            ChangePriceMenu(kassasystemet)

        if sel == 4: #Snygga till
            print()
            ChangeCampDateMenu(kassasystemet)
            # ShowAllCampDates(kassasystemet)
            # id_prod = input("Ange ID på produkt du vill ändra datum för: ").capitalize()
            # if len(id_prod) != 3 or id_prod.isnumeric() == False:
            #     print("3 siffror, tack!")
            # produktens_current_start = kassasystemet.FindProduktCampStart(id_prod) #hämtar fr class nuvrande datum
            # produktens_current_slut = kassasystemet.FindProduktCampEnd(id_prod)
            # if kassasystemet.FindProdukt(id_prod) == True:
            #     nyttStartDatum = input("Ange Startdatum i format YYYY-MM-DD: ")
            #     nyttSlutDatum = input("Ange Slutdatum i format YYYY-MM-DD: ")  
            #     if isDate(nyttStartDatum) == True and isDate(nyttSlutDatum) == True: # Egen checker på date
            #         with open("produkter.txt", "r") as prodfile:
            #             newlines = []
            #             for line in prodfile.readlines(): #Startdatum
            #                 if line.startswith(id_prod):
            #                     newlines.append(line.replace(produktens_current_start,nyttStartDatum))
            #                 else:
            #                     newlines.append(line)
            #         with open("produkter.txt", "w") as prodfile:
            #             for line in newlines:
            #                 prodfile.write(line)

            #         with open("produkter.txt", "r") as prodfile: #Slutdatum
            #             newlines = []
            #             for line in prodfile.readlines():
            #                 if line.startswith(id_prod):
            #                     newlines.append(line.replace(produktens_current_slut,nyttSlutDatum))
            #                 else:
            #                     newlines.append(line)
            #         with open("produkter.txt", "w") as prodfile:
            #             for line in newlines:
            #                 prodfile.write(line)
            #         kassasystemet.ChangeCampStartDate(id_prod, nyttStartDatum) #Updaterar live i programmet
            #         kassasystemet.ChangeCampEndDate(id_prod, nyttSlutDatum)            
            #     else:
            #         print("Fel format, YYYY-MM-DD endast!")
