import paho.mqtt.client as mqtt
import Message_parser as MePa
import json

MQTT_BROKER = '127.0.0.1'

client = mqtt.Client()

TOPIC_SUBSCRIPTION = ["RCU/Commands", "Pi/Commands", "RCU/Pings"]

#publish wrapper for printing purposes
def soar_publish(topic, msg):
    #print("--------------------------")
    #print("MQTT message published:" + msg)
    client.publish(topic, msg)



def handle_pi_command(data_dictionary):
    command = data_dictionary["command"] 
    if command == "HEARTBEAT":
        msg = MePa.send_heartbeat_msg()
    elif command == "NOS1_HOLD":
        TelO.tele_rcu_obj.is_nos1_hold_enable = True
    elif command == "NOS2_HOLD":
        TelO.tele_rcu_obj.is_nos2_hold_enable = True
    elif command == "NOS3_HOLD":
        TelO.tele_sob_obj.is_nos3_hold_enable = True
    elif command == "NOS1_RESET":
        TelO.tele_rcu_obj.is_nos1_hold_enable = False
    elif command == "NOS2_RESET":
        TelO.tele_rcu_obj.is_nos2_hold_enable = False
    elif command == "NOS3_RESET":
        TelO.tele_sob_obj.is_nos3_hold_enable = False
    elif command == "DELETE_TELEM_LOGS":
        TeleLog.ClearLogs()
    else:
        soar_publish("TELE_PI_ERROR", json.dumps({"error": "Invalid Command"}))
        return False




def on_mqtt_message(client, userdata, message):
    print("----------------------------------------------------received message:\n ",str(message.payload.decode("utf-8")))
    data_dictionary = json.loads(message.payload.decode("utf-8"))

    if message.topic == "RCU/Commands":
        MePa.send_command_msg(data_dictionary)
    elif message.topic == "RCU/Pings":
        MePa.send_ping_message(data_dictionary.get("Target"))
    elif message.topic == "Pi/Commands":
        handle_pi_command(data_dictionary)
    else:
        soar_publish("TELE_PI_ERROR", json.dumps({"error": "Unknown Command Topic"}))
        print("unknown topic")
        return False
        
    return True

def init_mqtt():
    client.connect(MQTT_BROKER)

    client.loop_start()
    for topic in TOPIC_SUBSCRIPTION:
        client.subscribe(topic)
    client.on_message=on_mqtt_message

    print("listening to RCU Commands")
