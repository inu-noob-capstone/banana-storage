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
import LightControl.CustomException as CustomException
import LightControl.LightSetting as LightSetting
import concurrent.futures

class MeasureLux():
  def __init__(self):
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

  def measureLux(self):
        self.lux = int(self.readLight())
        #print("측정된 조도 : " + format(self.lux,'.2f') + " lx")
        #time.sleep(0.5)
        return self.lux
        if self.stop_threads:
          raise CustomException.MeasureLuxTerminate

def work(lightSetting):
  lightSetting.lux = 999

if __name__=="__main__":
  global lightSetting
  lightSetting = LightSetting.LightSetting()
  m = MeasureLux()

  lightSetting.lux = m.measureLux()
  print('lightSetting.lux :', lightSetting.lux)
  work(lightSetting)
  print('lightSetting.lux :', lightSetting.lux)
