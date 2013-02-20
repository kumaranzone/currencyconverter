#!/usr/bin/env python
""" Program for converting currencies based on bank of canada data in the csv format"""
import sys
import urllib2
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os

""" Class for converting currencies"""

class CurrencyConverter(QDialog):
    def __init__(self,parent=None):
        super(CurrencyConverter,self).__init__(parent)
        date = self.getdata()
        rates = sorted(self.rates.keys())
        dateLabel = QLabel(date)
        self.fromCombobox = QComboBox()
        self.fromCombobox.addItems(rates)
        self.fromSpinbox = QDoubleSpinBox()
        self.toCombobox = QComboBox()
        self.toLabel = QLabel("1.00")
        self.fromCombobox.addItems(rates)
        self.fromSpinbox.setRange(0.01,10000000.00)
        self.fromSpinbox.setValue(1.00)
        self.toCombobox.addItems(rates)
        
        grid = QGridLayout()
        grid.addWidget(dateLabel,0,0)
        grid.addWidget(self.fromCombobox,1,0)
        grid.addWidget(self.fromSpinbox,1,1)
        grid.addWidget(self.toCombobox,2,0)
        grid.addWidget(self.toLabel,2,1)
        self.connect(self.fromCombobox, SIGNAL("currentIndexChanged(int)"),self.UpdateUi)
        self.connect(self.toCombobox, SIGNAL("currentIndexChanged(int)"),self.UpdateUi)
        self.connect(self.fromSpinbox, SIGNAL("valueChanged(double)"),self.UpdateUi)
        self.setWindowTitle("Currency")
        self.setLayout(grid)
        
        
    def UpdateUi(self):
        to = unicode(self.toCombobox.currentText())
        from_ = unicode(self.fromCombobox.currentText())
        amount= (self.rates[from_]/self.rates[to]) * \
        self.fromSpinbox.value()
        self.toLabel.setText("%0.2f" % amount)
        
    def getdata(self):
        self.rates = {}
        try:
            date = "Unknown"
            dir = os.getcwd()
            #fh = open(dir +"/pythonexamples/fx-seven-day.csv")
            fh = urllib2.urlopen("http://www.bankofcanada.ca/en/markets/csv/exchange_eng.csv")
           
            for line in fh:
                if not line or line.startswith(("#","Closing")):
                    continue
                fields = line.split(",")
                if line.startswith("Date"):
                    date = fields[-1]
                else:
                    try:
                        value = float(fields[-1])
                        self.rates[unicode(fields[0])]= value
                    except ValueError:
                        pass
            return "Exchange rates date:" + date
        except Exception,e:
            return "Failed to Download : \n%s" % e
        
app = QApplication(sys.argv)
currencyconverter = CurrencyConverter()
currencyconverter.show()
app.exec_()
                
        
        
        
        
    
