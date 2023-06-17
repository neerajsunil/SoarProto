#Publisher_nodered.py

import time
import json
import paho.mqtt.client as mqtt
import ControlMessage_pb2 as ProtoCtl
import CommandMessage_pb2 as ProtoCmd
import TelemetryMessage_pb2 as ProtoTele
import CoreProto_pb2 as Core

class TELE_DMB:
	def tele_gps(self, lat_minutes, lat_degrees, long_minutes, long_degrees, antenna_alt, antenna_unit, geoid_altitude, geoid_unit, total_altitude, total_unit, time):
	    return {
	        "latitude": str(lat_minutes) + "." + str(lat_degrees),
	        "longitude": str(long_minutes) + "." + str(long_degrees),
			"ant_altitude": str(antenna_alt),
			"ant_unit": str(antenna_unit),
			"geoid_altitude": str(geoid_altitude),
			"geoid_unit": str(geoid_unit),
	        "total_altitude": str(total_altitude),
			"total_unit": str(total_unit),
			"time": str(time)
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
	
	def tele_gpio_status(self, main_engine_valve_open, vent_open, drain_open):
	    return {
	        "mev_open": main_engine_valve_open,
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

	def tele_nos_load_cell(self, nos1_mass, nos2_mass):
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
	        "ac1_open": ac1_open,
	        "ac2_open": ac2_open,
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

	def tele_padbox_status(self, cont1, cont2):
		return {
			"cont1": cont1,
			"cont2": cont2
		}

class TELE_SOB:
	def tele_lr_load_cell(self, rocket_mass):
		return {
		"rocket_mass": str(rocket_mass)
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