import socket
import dht # sensor 
from machine import Pin
from time import sleep

sensor = dht.DHT22(Pin(16))

#### Send sensor data ####
while True:
    print("Measuring.")
    retry = 0
    while retry < 3:
        try:
            sensor.measure()
            temp = sensor.temperature()
            hum = sensor.humidity()
            temp_f = temp * (9/5) + 32.0
            break
        except:
            retry = retry + 1
    if retry < 3:
        print(temp_f)
        print(hum)
        host = "127.zerodotzero.one"
        port = 80
        postDataHere = "/post_sensor_data.php"
        key = "tPmAT5Ab3j7F9"
        sensorModel = "DHT22"
        location = "Lab0024"
        humidity = hum
        tempInF = temp_f
        baseline = "0.0"

        headers = "POST {sensor_url_path} HTTP/1.1\r\nContent-Type: {content_type}\r\nContent-Length: {content_length}\r\nHost: {host}\r\nConnection: close\r\n\r\n"

        body = "api_key={key}&sensor={sensorModel}&location={location}&value1={sensor1}&value2={sensor2}&value3={sensor3}"

        body_bytes = body.format(key=key,sensorModel=sensorModel,location=location,sensor1=humidity,sensor2=tempInF,sensor3=baseline).encode('UTF-8')
        header_bytes = headers.format(sensor_url_path=postDataHere,content_type="application/x-www-form-urlencoded",content_length=len(body_bytes),host=str(host) +":"+str(port)).encode('UTF-8')
        payload = header_bytes + body_bytes
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.sendall(payload)
        print(payload)
        sleep(5)
