import paho.mqtt.client as mqtt
import paho.mqtt.enums as enums
import time
import random
import json

# Configuración del cliente MQTT
broker = '8f06ff98fc7a47bd959c5a6a1d2ac822.s1.eu.hivemq.cloud'
port = 8883
topic = "test"
client_id = 'python-mqtt'
username = 'admin'
password = 'admiN456'

#funciones callback
def on_connect(client, userdata, flags, rc, args):
    print('CONNACK received with code ' + str(rc))

def on_publish(client, userdata, mid, rc, args): 
    print("mid: " + str(mid))

#funcione leer datos
def get_data():
    simulated_value1 = random.randint(0, 100)
    simulated_value2 = random.randint(0, 1)
    simulated_value3 = random.randint(0, 1)
    return {
        'level': simulated_value1,
        'value1': simulated_value2,
        'value2': simulated_value3
    }


# Crear un cliente MQTT
client = mqtt.Client(client_id="", userdata=None, clean_session=True, protocol=mqtt.MQTTv311, callback_api_version= enums.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_publish = on_publish
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set(username, password)
client.connect(broker, port)

client.loop_start()

# Simular datos de GPIO y publicar
try:
    while True:
        data = get_data()
        data_json = json.dumps(data)
      
        print(f'publish value: {data_json}')
        client.publish(topic, data_json, qos=1)
        time.sleep(3)
except KeyboardInterrupt:
    print("Script detenido manualmente")


client.loop_stop()
client.disconnect()
