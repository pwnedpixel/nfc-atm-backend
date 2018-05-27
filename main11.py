# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import jsonify
import sys
import time
from threading import Thread
import pymongo
from pymongo import MongoClient

#servo setup
import RPi.GPIO as IO    
                         # calling for time to provide delays in program
IO.setwarnings(False)          # do not show any warnings
IO.setmode (IO.BCM)            # programming the GPIO by BCM pin numbers. (like PIN29 as‘GPIO5’)
IO.setup(19,IO.OUT)             # initialize GPIO19 as an output
s1 = IO.PWM(19,50)      #withdraw servo
withdrawPos = 9.5
neutralPos = 3.5
depositPos = 12.5
import I2C_LCD_driver

mylcd = I2C_LCD_driver.lcd()

#Flask Setup
app = Flask(__name__)

#Welcome screen
mylcd.lcd_clear()
mylcd.lcd_display_string("Welcome to TAP ATM")

def transaction(action, amount, account):
        mylcd.lcd_clear()
        if action =='withdraw':
                mylcd.lcd_display_string('Withdrawing '+amount,1)
                mylcd.lcd_display_string('from '+account,2)
                mylcd.lcd_display_string('Thank you for', 3)
                mylcd.lcd_display_string('using TAP ATM!', 4)
                s1.start(neutralPos)
                time.sleep(1)
                s1.ChangeDutyCycle(withdrawPos)                   # change duty cycle for getting the servo position to 90º
                time.sleep(1)                                      # sleep for 1 second
                s1.ChangeDutyCycle(neutralPos)                  # change duty cycle for getting the servo position to 180º
                time.sleep(1)
                s1.ChangeDutyCycle(0)
                
        elif action == 'deposit':
                mylcd.lcd_display_string('Deposit ' + amount + ' into')
                mylcd.lcd_display_string(account+ ' via',2)
                mylcd.lcd_display_string('the slot. Thank you', 3)
                mylcd.lcd_display_string('for using TAP ATM!',4)
        time.sleep(4)
        mylcd.lcd_clear()
        mylcd.lcd_display_string("Welcome to TAP ATM")

@app.route('/', methods=['POST'])
def index():
        amount = request.get_json()['amount']
        action = request.get_json()['type']
        account = request.get_json()['account']
        thread = Thread(target = transaction, args=(action,amount,account,))
        thread.start()
        return jsonify(responseMessage='success')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
