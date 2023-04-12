#Publisher_nodered.py

import time
import json
import paho.mqtt.client as mqtt
import ControlMessage_pb2 as Proto
import CommandMessage_pb2 as ProtoCmd
import CoreProto_pb2 as Core

class TELE_DMB:
	def tele_baro(self, temp, pressure):
		return {
		"temp": str(temp),
		"pressure": str(pressure)
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
	
	def tele_pressure(self, pressure):
	    return {
	        "pressure": str(pressure)
	    }
	
	def tele_gps(self, lat_minutes, lat_seconds, long_minutes, long_seconds, altitude):
	    return {
	        "lat_minutes": str(lat_minutes),
	        "lat_seconds": str(lat_seconds),
	        "long_minutes": str(long_minutes),
	        "long_seconds": str(long_seconds),
	        "altitude": str(altitude)
	    }
	
	def tele_battery(self, power_src, bat_volt):
	    return {
	        "power_src": str(power_src),
	        "bat_volt": str(bat_volt)
	    }
	
	def tele_state(self, state, log_hz, log_sector, data_hz, hb_period, vent_state, drain_state, mev_pwm):
	    return {
	        "state": str(state),
	        "log_hz": str(log_hz),
	        "log_sector": str(log_sector),
	        "data_hz": str(data_hz),
	        "hb_period": str(hb_period),
	        "vent_state": str(vent_state),
	        "drain_state": str(drain_state),
	        "mev_pwm": str(mev_pwm)
	    }

class TELE_PBB:
	def tele_pressure(self, pressure1, pressure2):
		return {
		"pressure1": str(pressure1),
		"pressure2": str(pressure2)
		}
	
	def tele_temp(self, temp1, temp2):
	    return {
	        "temp1": str(temp1),
	        "temp2": str(temp2)
	    }
	
	def tele_gpio_status(self, drain_state, mev_state):
	    return {
	        "drain_state": str(drain_state),
	        "mev_state": str(mev_state)
	    }
	
	#def cmd_hb(self):
	#	return {
	#	}

class TELE_RCU:
	def tele_pressure(self, pressure1, pressure2, pressure3, pressure4):
		return {
		"pressure1": str(pressure1),
		"pressure2": str(pressure2),
		"pressure3": str(pressure3),
		"pressure4": str(pressure4)
		}
	
	def tele_temp(self, temp1, temp2):
	    return {
	        "temp1": str(temp1),
	        "temp2": str(temp2)
	    }
	
	def tele_nos_load_cell(self, nos_lc1, nos_lc2):
	    return {
	        "nos_lc1": str(nos_lc1),
	        "nos_lc2": str(nos_lc2)
	    }
	
	def tele_gpio_status(self, ac1_state, ac2_state, pbv1_state, pbv2_state, pbv3_state, sol1_state, sol2_state, continuity1_state, continuity2_state):
	    return {
	        "ac1_state": str(ac1_state),
	        "ac2_state": str(ac2_state),
	        "pbv1_state": str(pbv1_state),
	        "pbv2_state": str(pbv2_state),
	        "pbv3_state": str(pbv3_state),
	        "sol1_state": str(sol1_state),
	        "sol2_state": str(sol2_state),
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
	
	def tele_temp(self, temp1, temp2):
	    return {
	        "temp1": str(temp1),
	        "temp2": str(temp2)
	    }

	#def cmd_hb(self):
	#	return {
	#	}


MCB_CMD = {
'CMD_RCU_AC_1': 0,
'CMD_RCU_AC_2': 0,
'CMD_RCU_PBV_1': 0,
'CMD_RCU_PBV_2': 0,
'CMD_RCU_PBV_3': 0,
'CMD_RCU_SOL_1': 0,
'CMD_RCU_SOL_2A': 0,
'CMD_RCU_SOL_2B': 0,
'CMD_RCU_SOL_3A': 0,
'CMD_RCU_SOL_3B': 0,
'CMD_PAD_1_LAUNCH': 1,
'CMD_PAD_2_LAUNCH': 1,
'CMD_DMB_MEV': 0,
'CMD_DMB_DRAIN': 0, #all above int
'CMD_DMB_STATE': 'IDLE' #string
}

PROTO_STATE_TO_STRING = {
Core.RS_ABORT : 'RS_ABORT',
Core.RS_ARM : 'RS_ARM',
Core.RS_BURN : 'RS_BURN',
Core.RS_COAST : 'RS_COAST',
Core.RS_DESCENT : 'RS_DESCENT',
Core.RS_FILL : 'RS_FILL',
Core.RS_IGNITION : 'RS_IGNITION',
Core.RS_LAUNCH : 'RS_LAUNCH',
Core.RS_NONE : 'RS_NONE',
Core.RS_PRELAUNCH : 'RS_PRELAUNCH',
Core.RS_RECOVERY : 'RS_RECOVERY'
}

class MCB:
	def cmd_RCU_AC(self, rcu_ac_1, rcu_ac_2):
		MCB_CMD['CMD_RCU_AC_1'] = rcu_ac_1
		MCB_CMD['CMD_RCU_AC_2'] = rcu_ac_2
	
	def cmd_RCU_PBV(self, rcu_pbv_1, rcu_pbv_2, rcu_pbv_3):
		MCB_CMD['CMD_RCU_PBV_1'] = rcu_pbv_1
		MCB_CMD['CMD_RCU_PBV_2'] = rcu_pbv_2
		MCB_CMD['CMD_RCU_PBV_3'] = rcu_pbv_3
	
	def cmd_RCU_SOL(self, rcu_sol_1, rcu_sol_2a, rcu_sol_2b, rcu_sol_3a, rcu_sol_3b):
		MCB_CMD['CMD_RCU_SOL_1'] = rcu_sol_1
		MCB_CMD['CMD_RCU_SOL_2A'] = rcu_sol_2a
		MCB_CMD['CMD_RCU_SOL_2B'] = rcu_sol_2b
		MCB_CMD['CMD_RCU_SOL_3A'] = rcu_sol_3a
		MCB_CMD['CMD_RCU_SOL_3B'] = rcu_sol_3b
	
	def cmd_dmb(self, dmb_mev, dmb_drain, dmb_state):
		MCB_CMD['CMD_DMB_MEV'] = dmb_mev
		MCB_CMD['CMD_DMB_DRAIN'] = dmb_drain
		MCB_CMD['CMD_DMB_STATE'] = dmb_state	

'''

def on_message(client, userdata, message):
	print("received message: ",str(message.payload.decode("utf-8")))

#DMB Telemetry
tele_dmb_obj = TELE_DMB()
jsonStr_baro = json.dumps(tele_dmb_obj.tele_baro(18.0, 15.0))
jsonStr_imu = json.dumps(tele_dmb_obj.tele_imu([25.0,20.0,15.0], [45.0,40.0,35.0], [65.0,60.0,55.0]))
jsonStr_pressure = json.dumps(tele_dmb_obj.tele_pressure(20.0))
jsonStr_gps = json.dumps(tele_dmb_obj.tele_gps(20.0, 19.0, 18.0, 17.0, 16.0))
jsonStr_battery = json.dumps(tele_dmb_obj.tele_battery(0, 15.0))
jsonStr_state = json.dumps(tele_dmb_obj.tele_state(0, 0, 18.0, 0, 0, 0, 0, 0))

#PBB Telemetry
tele_pbb_obj = TELE_PBB()
pbb_jsonStr_pressure = json.dumps(tele_pbb_obj.tele_pressure(25.0, 20.0))
pbb_jsonStr_temp = json.dumps(tele_pbb_obj.tele_temp(25.0, 20.0))
pbb_jsonStr_gpio_status = json.dumps(tele_pbb_obj.tele_gpio_status(0, 0))

#RCU Telemetry
tele_rcu_obj = TELE_RCU()
rcu_jsonStr_pressure = json.dumps(tele_rcu_obj.tele_pressure(25.0, 20.0, 15.0, 10.0))
rcu_jsonStr_temp = json.dumps(tele_rcu_obj.tele_temp(25.0, 20.0))
rcu_jsonStr_nos_load_cell = json.dumps(tele_rcu_obj.tele_nos_load_cell(25.0, 20.0))
rcu_jsonStr_gpio_status = json.dumps(tele_rcu_obj.tele_gpio_status(0,0,0,0,0,0,0,0,0))

#SOB Telemetry
tele_sob_obj = TELE_SOB()
sob_jsonStr_lr_load_cell = json.dumps(tele_sob_obj.tele_lr_load_cell(25.0))
sob_jsonStr_temp = json.dumps(tele_sob_obj.tele_temp(25.0, 20.0))

#MCB Command
com_mcb_obj = MCB()
mcb_jsonStr_command = json.dumps(MCB_CMD)

mqttBroker ="127.0.0.1"

client = mqtt.Client()
client.connect(mqttBroker)

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