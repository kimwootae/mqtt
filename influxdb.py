import argparse
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

def on_connect(client, userdata, rc):
    print("Conneted with result code" + str(rc))
    client.subscribe("192.168.1.177")

def on_message(client, userdata, msg):
    print str(msg.payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.8", 1883, 60)
#client.subscribe(("/data",0))

client.subscribe(("/temperature",0))
client.subscribe(("/humidity",0))
temp = client.subscribe(("/temperature",0))
humi = client.subscribe(("/humudity",0))

body = [
    {
        "measurement":"temp_humi",
        "tags" : {
            "host": "server01",
            "region": "testroom",
        },
        "fields": {
            "temp": "{}".format(temp), "humi": "{}".format(humi)
        }
    }
]

db = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')
db.create_database('example')
db.write_points(body)
result = db.query('select value from temp_himi;')
print("Result: {0}".format(result))

client.loop_forever()
db.loop_forever()
