import socket
from machine import Pin
from time import sleep
import dht 

## Get sensor readings ##

sensor = dht.DHT22(Pin(15))
sensor.measure()
temp = sensor.temperature()
hum = sensor.humidity()
temp_f = temp * (9/5) + 32.0

#### Send sensor data ####
    
host = <YOUR SERVER> ## <-- UPDATE - myserver.com ##
port = <PORT> ## <-- UPDATE ## - 80/443/3306 or any other
postDataHere = <PATH TO DB FOR SENSOR DATA>  ## <-- UPDATE - \mysensorDB.php ##
key = <API KEY FOR AUTH> ## <-- UPDATE - 9834hkgh89t79ohgn ##
sensorModel = "DHT22"
location = "Lab0024"
hum = hum
temp_f = temp_f
baseline = "None"

headers = """\
POST {sensor_url_path} HTTP/1.1\r
Content-Type: {content_type}\r
Content-Length: {content_length}\r
Host: {host}\r
Connection: close\r
\r\n"""


body = "api_key={key}&sensor={sensorModel}&location={location}&value1={sensor1}&value2={sensor2}&value3={sensor3}"

body_bytes = body.format(
    key=key,
    sensorModel=sensorModel,
    location=location,
    sensor1=hum,
    sensor2=temp_f,
    sensor3=baseline
    ).encode('UTF-8')

header_bytes = headers.format(
    sensor_url_path=postDataHere,
    content_type="application/x-www-form-urlencoded",
    content_length=len(body_bytes),
    host=str(host) + ":" + str(port)
    ).encode('UTF-8')

payload = header_bytes + body_bytes

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(payload)
    sleep(900)
