from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtWidgets import QLabel, QPushButton, QLineEdit, QComboBox
import json
import requests

app = QApplication([])

class combobox(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather report")
        mainlayout = QVBoxLayout(self)
        layout = QHBoxLayout(self)
        mainlayout.addLayout(layout)
        layout1  = QVBoxLayout(self)
        layout.addLayout(layout1)
        self.output_label = QLabel()
        mainlayout.addWidget(self.output_label)
        self.in_combo_country = QComboBox()
        self.in_combo_states = QComboBox()
        self.in_combo_cities = QComboBox()
        Country = ['None', 'India', 'Germany']
        self.in_combo_country.addItems(Country)
        layout1.addWidget(self.in_combo_country)
        self.in_combo_states.addItem('None')
        layout1.addWidget(self.in_combo_states)
        self.in_combo_cities.addItem('None')
        layout1.addWidget(self.in_combo_cities)
        layout2 = QVBoxLayout()
        self.btn = QPushButton('get weather')
        
        layout2.addWidget(self.btn)
        layout.addLayout(layout2)
     
        self.setLayout(layout)
   
        self.in_combo_country.currentTextChanged.connect(self.additems_combo_1)
        self.additems_combo_1()
        self.in_combo_country.currentTextChanged.connect(self.additems_combo_2)
        self.additems_combo_2()
        self.in_combo_states.activated.connect(self.additems_combo_2)
        self.additems_combo_2()
        self.btn.clicked.connect(self.get_weather)
        #self.get_weather()

    def additems_combo_1(self):
        for i in range(0, 3):
            for i in range(self.in_combo_states.count()):
                self.in_combo_states.removeItem(i)
        states = {'India' : ['AndhraPradesh', 'Karnataka', 'Kerala', 'Tamilnadu'], 'Germany' : ['Bavaria', 'Hesse', 'Thuringia', 'Berlin'], 'None':['None']}
        in_country = self.in_combo_country.currentText()
        self.in_combo_states.addItems(states[in_country])

    def additems_combo_2(self):
         for i in range(0, 3):
            for i in range(self.in_combo_cities.count()):
                self.in_combo_cities.removeItem(i)
         cities = {'AndhraPradesh' : ['Anantapur','Vishakpatnam','Kurnool'],'Karnataka' : ['Bengaluru','Gulbarga','Udupi'], 'Kerala': ['Kochi','Thrissur','Kannur'],
              'Tamilnadu':['Chennai','Coimbatore','Madurai'], 'Bavaria':['Munich','Nuremberg','Deggendorf'], 'Hesse': ['Kassel','Frankfurt','Marburg'],
              'Thuringia':['Jena','Erfurt'], 'Berlin':[], 'None':['None']}
         in_states = self.in_combo_states.currentText()
         self.in_combo_cities.addItems(cities[in_states])

    def get_weather(self):
        in_country = self.in_combo_country.currentText()
        in_states = self.in_combo_states.currentText()
        in_city = self.in_combo_cities.currentText()
        response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={in_city},{in_states},{in_country}&limit=5&appid=c19e9ceffe954823d9f32fef61db9426")
        obj = response.json()
        newdata = {}
        for entry in obj:
            name = entry.pop('name') #remove and return the name field to use as a key
            newdata[name] = entry
            lat_1 = newdata[in_city]['lat']
            lon_1= newdata[in_city]['lon']
            add = f'https://api.openweathermap.org/data/2.5/weather?lat={lat_1}&lon={lon_1}&appid=c19e9ceffe954823d9f32fef61db9426'
            temp = requests.get(add).json()
            #print(temp)
            message=[]
            for key, val in temp["main"].items():
                #print(key,val)
                message.append (f'{key} is {val}')
            self.output_label.setText(str(message))

    
window = combobox()
window.show()
app.exec()



    
