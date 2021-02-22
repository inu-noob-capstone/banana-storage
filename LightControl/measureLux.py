#!/usr/bin/python
#---------------------------------------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#           bh1750.py
# Read data from a BH1750 digital light sensor.
#
# Author : Matt Hawkins
# Date   : 26/06/2018
#
# For more information please visit :
# https://www.raspberrypi-spy.co.uk/?s=bh1750
#
#---------------------------------------------------------------------
from smbus2 import SMBus
import time
import threading
import CustomException
import LightSetting

class MeasureLux(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.deamon =True
    self.stop_threads = False
    self.lux = 0
    
    # Define some constants from the datasheet
    self.DEVICE     = 0x23 # Default device I2C address

    self.POWER_DOWN = 0x00 # No active state
    self.POWER_ON   = 0x01 # Power on
    self.RESET      = 0x07 # Reset data register value

    # Start measurement at 4lx resolution. Time typically 16ms.
    self.CONTINUOUS_LOW_RES_MODE = 0x13
    # Start measurement at 1lx resolution. Time typically 120ms
    self.CONTINUOUS_HIGH_RES_MODE_1 = 0x10
    # Start measurement at 0.5lx resolution. Time typically 120ms
    self.CONTINUOUS_HIGH_RES_MODE_2 = 0x11
    # Start measurement at 1lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    self.ONE_TIME_HIGH_RES_MODE_1 = 0x20
    # Start measurement at 0.5lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    self.ONE_TIME_HIGH_RES_MODE_2 = 0x21
    # Start measurement at 1lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    self.ONE_TIME_LOW_RES_MODE = 0x23

    #bus = smbus.SMBus(0) # Rev 1 Pi uses 0
    #self.bus = SMBus(1)  # Rev 2 Pi uses 1

  def convertToNumber(self,data):
    # Simple function to convert 2 bytes of data
    # into a decimal number. Optional parameter 'decimals'
    # will round to specified number of decimal places.
    # result=(data[1] + (256 * data[0])) / 1.2. window influence 고려하여 0.4 나누기로 수정
    result=(data[1] + (256 * data[0])) / 0.51
    return (result)

  def readLight(self):
    # Read data from I2C interface
    self.bus = SMBus(1)  # Rev 2 Pi uses 1
    addr=self.DEVICE
    data = self.bus.read_i2c_block_data(addr,self.ONE_TIME_HIGH_RES_MODE_1,2)
    return self.convertToNumber(data)

  def measureLux(self, LightSetting.LightSetting):
      while True:
        self.lux = self.readLight()
        print("Light Level : " + format(self.lux,'.2f') + " lx")
        time.sleep(0.5)
        if self.stop_threads:
          raise CustomException.MeasureLuxTerminate
          break

  def MeasureLuxTerminate(self):
    raise CustomException.MeasureLuxTerminate
      
if __name__=="__main__":
  m = MeasureLux()
  t = threading.Thread(target = m.measureLux, daemon = True)
  t.daemon = True
  m.stop_threads = False
  t.start()
  m.stop_threads = True  
