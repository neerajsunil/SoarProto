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
	        "lat_minutes": str(lat_minutes),
	        "lat_degrees": str(lat_degrees),
	        "long_minutes": str(long_minutes),
	        "long_seconds": str(long_degrees),
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
			"accel_x": str(accel[0]),
			"accel_y": str(accel[1]),
			"accel_z": str(accel[2]),
			"gyro_x": str(gyro[0]),
			"gyro_y": str(gyro[1]),
			"gyro_z": str(gyro[2]),
			"mag_x": str(mag[0]),
			"mag_y": str(mag[1]),
			"mag_z": str(mag[2])
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
	        "mev_open": str(main_engine_valve_open),
			"vent_open": str(vent_open),
			"drain_open": str(drain_open)
	    }

class TELE_RCU:
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
	    return {
	        "nos1_mass": str(nos1_mass),
	        "nos2_mass": str(nos2_mass)
	    }
	
	def tele_relay_status(self, ac1_open, ac2_open, pbv1_open, pbv2_open, pbv3_open, sol1_open, sol2_open, sol3_open, sol4_open, sol5_open, sol6_open, sol7_open, sol8a_open, sol8b_open):
	    return {
	        "ac1_open": str(ac1_open),
	        "ac2_open": str(ac2_open),
	        "pbv1_open": str(pbv1_open),
	        "pbv2_open": str(pbv2_open),
	        "pbv3_open": str(pbv3_open),
	        "sol1_open": str(sol1_open),
	        "sol2_open": str(sol2_open),
			"sol3_open": str(sol3_open),
			"sol4_open": str(sol4_open),
			"sol5_open": str(sol5_open),
			"sol6_open": str(sol6_open),
			"sol7_open": str(sol7_open),
			"sol8a_open": str(sol8a_open),
			"sol8b_open": str(sol8b_open)
	    }

	def tele_padbox_status(self, cont1, cont2):
		return {
			"cont1": str(cont1),
			"cont2": str(cont2)
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