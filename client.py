import sys
import termios
import contextlib
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import subprocess

 
MQTT_SERVER = "192.168.43.127"
MQTT_PATH = "client_server_communication"
MQTT_PATH_BACK = "server_client_communication"
 
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH_BACK)

def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload))
    # temp = str(msg.payload)
    # print(msg.payload.decode())
    temp = str(msg.payload.decode())
    # print(temp)
    subprocess.call(["./catsay", temp])

@contextlib.contextmanager
def raw_mode(file):
    old_attrs = termios.tcgetattr(file.fileno())
    new_attrs = old_attrs[:]
    new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
    try:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
        yield
    finally:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)


def main():
    print('exit with ^C or ^D')
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_SERVER, 1883, 60)
    with raw_mode(sys.stdin):
        try:
            while True:
                ch = sys.stdin.read(1)
                if not ch or ch == chr(4):
                    break
                print(ch)
                # print('%02x' % ord(ch),)
                if (ch == 'w'):
                    # print("wykrylem w")
                    publish.single(MQTT_PATH, "up", hostname=MQTT_SERVER)
                elif (ch == 's'):
                    #handle
                    # print("wykrylem s")
                    publish.single(MQTT_PATH, "down", hostname=MQTT_SERVER)

                elif (ch == 'a'):
                    # print("wykrylem a")
                    publish.single(MQTT_PATH, "left", hostname=MQTT_SERVER)
                    #handle
                elif (ch == 'd'):
                    # print("wykrylem d")
                    publish.single(MQTT_PATH, "right", hostname=MQTT_SERVER)
                    #handle

                client.loop()
        except(KeyboardInterrupt, EOFError):
            pass


if __name__ == '__main__':
    main()