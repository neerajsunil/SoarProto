#Publisher_nodered.py

import time
import json
import paho.mqtt.client as mqtt
import ControlMessage_pb2 as ProtoCtl
import CommandMessage_pb2 as ProtoCmd
import TelemetryMessage_pb2 as ProtoTele
import CoreProto_pb2 as Core

class TELE_DMB:
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
	
	def tele_pressure(self, upper_pv_pressure):
	    return {
	        "upper_pv_pressure": str(upper_pv_pressure)
	    }
	
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
	
	def tele_battery(self, power_src, bat_volt):
	    return {
	        "power_src": str(power_src),
	        "bat_volt": str(bat_volt)
	    }

	def tele_flash(self, sector_address, logging_rate):
		return {
			"loghz": str(sector_address),
			"logsec": str(logging_rate)
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
	        "mev_open": str(mev_open),
			"vent_open": str(vent_open),
			"drain_open": str(drain_state)
	    }
	
	#def cmd_hb(self):
	#	return {
	#	}

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
			"continuity1_state": str(continuity1_state),
			"continuity2_state": str(continuity2_state)
		}
	
	#def cmd_hb(self):
	#	return {
	#	}

class TELE_SOB:
	def tele_lr_load_cell(self, rocket_lc1):
		return {
		"rocket_lc1": str(rocket_lc1)
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

def on_message(client, userdata, message):
	print("received message: ",str(message.payload.decode("utf-8")))

#DMB Telemetry
tele_dmb_obj = TELE_DMB()
#jsonStr_baro = json.dumps(tele_dmb_obj.tele_baro(18.0, 15.0))
#jsonStr_imu = json.dumps(tele_dmb_obj.tele_imu([25.0,20.0,15.0], [45.0,40.0,35.0], [65.0,60.0,55.0]))
#jsonStr_pressure = json.dumps(tele_dmb_obj.tele_pressure(20.0))
#jsonStr_gps = json.dumps(tele_dmb_obj.tele_gps(20.0, 19.0, 18.0, 17.0, 16.0))
#jsonStr_battery = json.dumps(tele_dmb_obj.tele_battery(0, 15.0))
#jsonStr_flash = json.dumps(tele_dmb_obj.tele_flash(0, 15.0))
#jsonStr_state = json.dumps(tele_dmb_obj.tele_state(0, 0, 18.0, 0, 0, 0, 0, 0))

#PBB Telemetry
tele_pbb_obj = TELE_PBB()
#pbb_jsonStr_pressure = json.dumps(tele_pbb_obj.tele_pressure(25.0, 20.0))
#pbb_jsonStr_temp = json.dumps(tele_pbb_obj.tele_temp(25.0, 20.0))
#pbb_jsonStr_gpio_status = json.dumps(tele_pbb_obj.tele_gpio_status(0, 0))

#RCU Telemetry
tele_rcu_obj = TELE_RCU()
#rcu_jsonStr_pressure = json.dumps(tele_rcu_obj.tele_pressure(25.0, 20.0, 15.0, 10.0))
#rcu_jsonStr_temp = json.dumps(tele_rcu_obj.tele_temp(25.0, 20.0))
#rcu_jsonStr_nos_load_cell = json.dumps(tele_rcu_obj.tele_nos_load_cell(25.0, 20.0))
#rcu_jsonStr_relay_status = json.dumps(tele_rcu_obj.tele_relay_status(0,0,0,0,0,0,0,0,0))

#SOB Telemetry
tele_sob_obj = TELE_SOB()
#sob_jsonStr_lr_load_cell = json.dumps(tele_sob_obj.tele_lr_load_cell(25.0))
#sob_jsonStr_temp = json.dumps(tele_sob_obj.tele_temp(25.0, 20.0))

'''
while True:
	#DMB
	client.publish("TELE_DMB", jsonStr_baro)
	print("Just published json object" + str(jsonStr_baro) + "to TELE_DMB")
	client.publish("TELE_IMU", jsonStr_imu)
	print("Just published json object" + str(jsonStr_imu) + "to TELE_IMU")
	client.publish("TELE_PRESSURE", jsonStr_pressure)
	print("Just published json object" + str(jsonStr_pressure) + "to TELE_PRESSURE")
	client.publish("TELE_GPS", jsonStr_gps)
	print("Just published json object" + str(jsonStr_gps) + "to TELE_GPS")
	client.publish("TELE_BATTERY", jsonStr_battery)
	print("Just published json object" + str(jsonStr_battery) + "to TELE_BATTERY")
	client.publish("TELE_FLASH", jsonStr_flash)
	print("Just published json object" + str(jsonStr_flash) + "to TELE_FLASH")
	client.publish("TELE_STATE", jsonStr_state)
	print("Just published json object" + str(jsonStr_state) + "to TELE_STATE")
	client.publish("MCB_COMMAND", mcb_jsonStr_command)
	print("Just published json object" + str(mcb_jsonStr_command) + "to MCB_COMMAND")
	
	
	time.sleep(1)

	client.loop_start()
	client.subscribe("TELE_TEST")
	client.on_message=on_message
	client.loop_stop()
	
	#client.loop_start()
	#client.subscribe("test")
	#client.on_message=on_message
	#client.loop_stop()
'''