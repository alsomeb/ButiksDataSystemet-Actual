from klasser_funktioner import Kassa, getInputBetween, ReadProducts, nyKund, admin

kassasystem = Kassa()
ReadProducts(kassasystem)

while True:
    print("\nKASSA")
    print("1. Ny kund")
    print("2. Adminverktyg")
    print("0. Avsluta")
    sel = getInputBetween(0,2)
    if sel == 0:
        print("Avslutar Kassasystemet..")
        break
    if sel == 1:
       nyKund(kassasystem)
    if sel == 2:
        admin(kassasystem)