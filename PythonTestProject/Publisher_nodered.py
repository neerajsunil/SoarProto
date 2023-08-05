#Publisher_nodered.py

import os
import time
import json
import paho.mqtt.client as mqtt
import ControlMessage_pb2 as ProtoCtl
import CommandMessage_pb2 as ProtoCmd
import TelemetryMessage_pb2 as ProtoTele
import CoreProto_pb2 as Core
import TelemetryLogger as TeleLog

class TELE_DMB:
	def tele_gps(self, lat_minutes, lat_degrees, long_minutes, long_degrees, antenna_alt, antenna_unit, geoid_altitude, geoid_unit, total_altitude, total_unit, time):
	    return {
	        "lat": str(lat_minutes) + "." + str(lat_degrees),
	        "lon": str(long_minutes) + "." + str(long_degrees),
		"ant_altitude": str(antenna_alt),
		"ant_unit": str(antenna_unit),
		"geoid_altitude": str(geoid_altitude),
		"geoid_unit": str(geoid_unit),
	        "total_altitude": str(total_altitude),
		"total_unit": str(total_unit),
		"time": str(time),
		"name": "Ouroboros",
		"icon": "rocket",
		"color": "#000"
	    }
	
	def tele_baro(self, baro_pressure, baro_temp):
		return {
			"baro_pressure": str(baro_pressure),
			"baro_temp": str(baro_temp)
		}
	
	def tele_imu(self, accel, gyro, mag):
	    return {
		    "accel": accel,
			"gyro": gyro,
			"mag": mag
	    }
	
	def tele_battery(self, power_src, bat_volt):
	    return {
	        "power_src": str(power_src),
	        "bat_volt": str(bat_volt)
	    }
	
	def tele_flash(self, sector_address, logging_rate):
		return {
			"sector_address": str(sector_address),
			"logging_rate": str(logging_rate)
		}

	def tele_pressure(self, upper_pv_pressure):
	    return {
	        "upper_pv_pressure": str(upper_pv_pressure)
	    }

class TELE_PBB:
	def tele_pressure(self, ib_pressure, lower_pv_pressure):
		return {
			"ib_pressure": str(ib_pressure),
			"lower_pv_pressure": str(lower_pv_pressure)
		}
	
	def tele_temp(self, ib_temperature, pv_temperature):
	    return {
	        "ib_temperature": str(ib_temperature),
	        "pv_temperature": str(pv_temperature)
	    }
	
	def tele_gpio_status(self, vent_open, drain_open):
	    return {
		"vent_open": vent_open,
		"drain_open": drain_open
	    }
	
	def tele_mevstate(self, mev_open):
		return {
			"mev_open": mev_open
		}

class TELE_RCU:
	def __init__(self):
		self.is_nos1_hold_enable = False
		self.is_nos2_hold_enable = False
		self.nos1_hold_mass = 0
		self.nos2_hold_mass = 0

		self.nos1_tare = False
		self.nos2_tare = False
		self.nos1_calibrate = False
		self.nos2_calibrate = False
		self.nos1_calibration_value = 0
		self.nos2_calibration_value = 0
		self.nos1_offset_file = "rcu_nos1_offset.txt"
		self.nos2_offset_file = "rcu_nos2_offset.txt"
		self.nos1_slope_file = "rcu_nos1_slope.txt"
		self.nos2_slope_file = "rcu_nos2_slope.txt"
		self.nos1_decimals_file = "rcu_nos1_decimals.txt"
		self.nos2_decimals_file = "rcu_nos2_decimals.txt"

		self.nos1_offset = TeleLog.LoadCellLogReader(self.nos1_offset_file, 0)
		self.nos2_offset = TeleLog.LoadCellLogReader(self.nos2_offset_file, 0)
		self.nos1_slope = TeleLog.LoadCellLogReader(self.nos1_slope_file, 1)
		self.nos2_slope = TeleLog.LoadCellLogReader(self.nos2_slope_file, 1)
		self.nos1_decimals = int(TeleLog.LoadCellLogReader(self.nos1_decimals_file, 0))
		self.nos2_decimals = int(TeleLog.LoadCellLogReader(self.nos2_decimals_file, 0))

	def tele_pressure(self, pt1_pressure, pt2_pressure, pt3_pressure, pt4_pressure):
		return {
		"pt1_pressure": str(pt1_pressure),
		"pt2_pressure": str(pt2_pressure),
		"pt3_pressure": str(pt3_pressure),
		"pt4_pressure": str(pt4_pressure)
		}

	def tele_temp(self, tc1_temp, tc2_temp):
	    return {
	        "tc1_temp": str(tc1_temp),
	        "tc2_temp": str(tc2_temp)
	    }

	def tele_nos_load_cell(self, nos1_value, nos2_value):
		if self.nos1_tare:
			self.nos1_offset = nos1_value
			print("NOS1_TARE:" + str(self.nos1_offset))
			TeleLog.LoadCellLogger(self.nos1_offset_file, self.nos1_offset)
			self.nos1_tare = False
		if self.nos2_tare:
			self.nos2_offset = nos2_value
			print("NOS2_TARE:" + str(self.nos2_offset))
			TeleLog.LoadCellLogger(self.nos2_offset_file, self.nos2_offset)
			self.nos2_tare = False
		if self.nos1_calibrate:
			self.nos1_slope = (nos1_value - self.nos1_offset) / self.nos1_calibration_value
			print("NOS1_CAL:" + str(self.nos1_slope))
			TeleLog.LoadCellLogger(self.nos1_slope_file, self.nos1_slope)
			self.nos1_decimals = len(str(self.nos1_calibration_value).split(".")[1])
			TeleLog.LoadCellLogger(self.nos1_decimals_file, self.nos1_decimals)
			print("NOS1_DEC:" + str(self.nos1_decimals))
			self.nos1_calibrate = False
		if self.nos2_calibrate:
			self.nos2_slope = (nos2_value - self.nos2_offset) / self.nos2_calibration_value
			print("NOS2_CAL:" + str(self.nos2_slope))
			TeleLog.LoadCellLogger(self.nos2_slope_file, self.nos2_slope)
			self.nos2_decimals = len(str(self.nos2_calibration_value).split(".")[1])
			TeleLog.LoadCellLogger(self.nos2_decimals_file, self.nos2_decimals)
			print("NOS2_DEC:" + str(self.nos2_decimals))
			self.nos2_calibrate = False

		nos1_mass = round((nos1_value - self.nos1_offset) / self.nos1_slope, self.nos1_decimals)
		nos2_mass = round((nos2_value - self.nos2_offset) / self.nos2_slope, self.nos2_decimals)


		nos1_hold_str = "0"
		nos2_hold_str = "0"

		if self.is_nos1_hold_enable is False:
			# keep null string but update nos mass
			self.nos1_hold_mass = nos1_mass
		else:
			# replace output string with last held mass
			nos1_hold_str = str(self.nos1_hold_mass)
			nos1_mass -= self.nos1_hold_mass

		if self.is_nos2_hold_enable is False:
			self.nos2_hold_mass = nos2_mass
		else:
			nos2_hold_str = str(self.nos2_hold_mass)
			nos2_mass -= self.nos2_hold_mass

		return {
	        "nos1_mass": str(nos1_mass),
	        "nos2_mass": str(nos2_mass),
			"nos1_hold": nos1_hold_str,
			"nos2_hold": nos2_hold_str
		    }

	def tele_relay_status(self, ac1_open, ac2_open, pbv1_open, pbv2_open, pbv3_open, sol1_open, sol2_open, sol3_open, sol4_open, sol5_open, sol6_open, sol7_open, sol8a_open, sol8b_open):
	    return {
	        "ac_shed_open": ac1_open,
	        "pbv1_open": pbv1_open,
	        "pbv2_open": pbv2_open,
	        "pbv3_open": pbv3_open,
	        "sol1_open": sol1_open,
	        "sol2_open": sol2_open,
			"sol3_open": sol3_open,
			"sol4_open": sol4_open,
			"sol5_open": sol5_open,
			"sol6_open": sol6_open,
			"sol7_open": sol7_open,
			"sol8a_open": sol8a_open,
			"sol8b_open": sol8b_open
	    }

	def tele_padbox_status(self, cont1, cont2, box1_on, box2_on):
		return {
			"cont1": cont1,
			"cont2": cont2,
			"box1_on": box1_on,
			"box2_on": box2_on
		}

class TELE_SOB:
	def __init__ (self):
		self.is_nos3_hold_enable = False
		self.nos3_hold_mass = 0

		self.nos3_tare = False
		self.nos3_calibrate = False
		self.nos3_calibration_value = 0
		self.nos3_offset_file = "rcu_nos3_offset.txt"
		self.nos3_slope_file = "rcu_nos3_slope.txt"
		self.nos3_decimals_file = "rcu_nos3_decimals.txt"

		self.nos3_offset = TeleLog.LoadCellLogReader(self.nos3_offset_file, 0)
		self.nos3_slope = TeleLog.LoadCellLogReader(self.nos3_slope_file, 1)
		self.nos3_decimals = int(TeleLog.LoadCellLogReader(self.nos3_decimals_file, 0))

	def tele_lr_load_cell(self, rocket_value):
		if self.nos3_tare:
			self.nos3_offset = rocket_value
			print("NOS3_TARE:" + str(self.nos3_offset))
			TeleLog.LoadCellLogger(self.nos3_offset_file, self.nos3_offset)
			self.nos3_tare = False
		if self.nos3_calibrate:
			self.nos3_slope = (rocket_value - self.nos3_offset) / self.nos3_calibration_value
			print("NOS3_CAL:" + str(self.nos3_slope))
			TeleLog.LoadCellLogger(self.nos3_slope_file, self.nos3_slope)
			self.nos3_decimals = len(str(self.nos3_calibration_value).split(".")[1])
			TeleLog.LoadCellLogger(self.nos3_decimals_file, self.nos3_decimals)
			print("NOS3_DEC:" + str(self.nos3_decimals))
			self.nos3_calibrate = False
		print("rocket_mass add values: " + str(rocket_value))
		rocket_mass = round((rocket_value - self.nos3_offset) / self.nos3_slope, self.nos3_decimals)

		nos3_hold_str = "0"

		if self.is_nos3_hold_enable is False:
			self.nos3_hold_mass = rocket_mass
		else:
			nos3_hold_str = str(self.nos3_hold_mass)
			rocket_mass -= self.nos3_hold_mass
			print(nos3_hold_str)

		return {
		"rocket_mass": str(rocket_mass),
		"rocket_hold": nos3_hold_str
		}
	def tele_temp(self, tc1_temp, tc2_temp):
		return {
		"tc1_temp": str(tc1_temp),
		"tc2_temp": str(tc2_temp)
		}
	def tele_irtemp(self, ambient_temp, object_temp):
		return {
		"ambient_temp": str(ambient_temp),
		"object_temp": str(object_temp)
		}

	
#DMB Telemetry
tele_dmb_obj = TELE_DMB()

#PBB Telemetry
tele_pbb_obj = TELE_PBB()

#RCU Telemetry
tele_rcu_obj = TELE_RCU()

#SOB Telemetry
tele_sob_obj = TELE_SOB()
