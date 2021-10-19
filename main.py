from klasser_funktioner import Kassa, getInputBetween, ReadProducts, nyKund

kassasystem = Kassa()
ReadProducts(kassasystem)

while True:
    print("\nKASSA")
    print("1. Ny kund")
    print("0. Avsluta")
    sel = getInputBetween(0,1)
    if sel == 0:
        print("Avslutar Kassasystemet..")
        break
    if sel == 1:
       nyKund(kassasystem)
