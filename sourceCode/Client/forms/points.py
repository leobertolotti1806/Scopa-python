from config import *

class PointTable(customtkinter.CTkFrame):
    def __init__(self, parent, pickedCards, enemyPickedCards, points, names, home):
        super().__init__(parent)

        # Configura griglia con più spazio
        self.pickedCards = pickedCards
        self.enemyPickedCards = enemyPickedCards
        self.names = names
        self.calculatePoints(points)

        self.grid_columnconfigure((0, 1, 2), weight=1, uniform="cols")
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        header_label = customtkinter.CTkLabel(self, text=self.points["win"], font=customtkinter.CTkFont(size=20, weight="bold"))

        header_label.grid(row=0, column=0, columnspan=3, pady=(15, 10))

        customtkinter.CTkLabel(self, text=names[0], font=customtkinter.CTkFont(size=16, weight="bold")).grid(row=1, column=0, padx=10, pady=(5, 10))
        customtkinter.CTkLabel(self, text="Resoconto", font=customtkinter.CTkFont(size=16, weight="bold")).grid(row=1, column=1, padx=10, pady=(5, 10))
        customtkinter.CTkLabel(self, text=names[1], font=customtkinter.CTkFont(size=16, weight="bold")).grid(row=1, column=2, padx=10, pady=(5, 10))

        labels = ["Scope", "Sette bello", "Carte", "Denari", "Primiera", "Totale"]
        for i, label in enumerate(labels):
            customtkinter.CTkLabel(self, text=label,
                        font=customtkinter.CTkFont(size=14)).grid(row=i + 2, column=1, pady=10)

        # Punteggi iniziali (0 per tutte le celle)
        self.myLabels = []
        self.enemyLabels = []

        for i in range(6):
            myLbl = customtkinter.CTkLabel(self, font=customtkinter.CTkFont(size=14))
            enemyLbl = customtkinter.CTkLabel(self, font=customtkinter.CTkFont(size=14))
            myLbl.grid(row= i + 2, column=0, padx=10, pady=10)
            enemyLbl.grid(row=i + 2, column=2, padx=10, pady=10)
            self.myLabels.append(myLbl)
            self.enemyLabels.append(enemyLbl)

        self.myLabels[0].configure(text = self.points["Scope1"])
        self.enemyLabels[0].configure(text = self.points["Scope2"])
        
        self.myLabels[1].configure(text = self.points["Sette bello"])
        self.enemyLabels[1].configure(text = "Sì" if self.points["Sette bello"] == "No" else "No")

        self.myLabels[2].configure(text = len(pickedCards) if self.points["Carte"] != "Pari" else "Pari")
        self.enemyLabels[2].configure(text = len(enemyPickedCards) if self.points["Carte"] != "Pari" else "Pari")

        self.myLabels[3].configure(text = self.points["Denari1"])
        self.enemyLabels[3].configure(text = self.points["Denari2"])

        self.myLabels[4].configure(text = self.points["Primiera"])
        self.enemyLabels[4].configure(
            text="Sì" if self.points["Primiera"] == "No" else "No" if self.points["Primiera"] == "Sì" else "Pari"
        )

        self.myLabels[5].configure(text = self.points["Totale1"])
        self.enemyLabels[5].configure(text = self.points["Totale2"])

        # Pulsante in basso (centrato e più grande)
        self.grid_rowconfigure(9, weight=1)
        btnsFrame = customtkinter.CTkFrame(self)
        btnsFrame.grid(row=9, column=0, columnspan=3, pady=(20, 10), sticky="nsew")
        btnsFrame.grid_columnconfigure(0, weight=1)

        # Pulsante Home
        homeBtn = customtkinter.CTkButton(
            btnsFrame,
            text="Home",
            font=customtkinter.CTkFont(size=16, weight="bold"),
            anchor="center",
            height=50,  # Altezza aumentata
            width=150,  # Larghezza aumentata
            command=home,
        )
        homeBtn.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    def calculatePoints(self, points):
        points["Totale1"] = 0
        points["Totale2"] = 0
        points["Carte"] = len(self.pickedCards)
        
        if len(self.pickedCards) > 20:
            points["Totale1"] += 1
        elif len(self.pickedCards) < 20:
            points["Totale2"] += 1
        else:
            points["Carte"] = "Pari"

        self.calculateDenari(points)

        if points["Denari1"] > points["Denari2"]:
            points["Totale1"] += 1
        elif points["Denari1"] < points["Denari2"]:
            points["Totale2"] += 1
        else:
            points["Denari1"] = "Pari"
            points["Denari2"] = "Pari"

        self.calculatePrimiera(points)

        if points["Primiera"] == "Sì":
            points["Totale1"] += 1
        elif points["Primiera"] == "No":
            points["Totale2"] += 1

        points["Totale1"] += points["Scope1"]
        points["Totale2"] += points["Scope2"]

        if points["Sette bello"] == "Sì":
            points["Totale1"] += 1
        else:
            points["Totale2"] += 1

        if points["Totale1"] > points["Totale2"]:
            points["win"] = self.names[0] + " HA VINTO!!!"
        elif points["Totale1"] < points["Totale2"]:
            points["win"] = self.names[1] + " HA VINTO!!!"
        else:
            points["win"] = "Patta!"

        self.points = points

    def count(self, num):
        return sum(1 for carta in self.pickedCards if carta[1:] == str(num))
    
    def calculatePrimiera(self, points):
        points["Primiera"] = "Pari"

        primiera = 2
        i = 0
        val = [7, 6 ,1]

        while primiera == 2 and i < 3:
            primiera = self.count(val[i])

            if primiera > 2:
                points["Primiera"] = "Sì"
            elif primiera < 2:
                points["Primiera"] = "No"
                
            i += 1

    def calculateDenari(self, points):
        points["Denari1"] = 0
        points["Denari2"] = 0

        for c in self.pickedCards:
            if c[0] == "D":
                points["Denari1"] += 1

        for c in self.enemyPickedCards:
            if c[0] == "D":
                points["Denari2"] += 1