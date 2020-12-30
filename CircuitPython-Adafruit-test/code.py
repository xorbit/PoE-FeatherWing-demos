import board
import busio
import digitalio
import adafruit_requests as requests
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket
import neopixel
import time

print("Wiznet5k WebClient Test")

def get_mac(i2c):
    "Read MAC from 24AA02E48 chip and return it"
    mac = bytearray(6)
    while not i2c.try_lock():
        pass
    i2c.writeto(0x50, bytearray((0xFA,)))
    i2c.readfrom_into(0x50, mac, start=0, end=6)
    i2c.unlock()
    return mac

# Status LED
led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led.brightness = 0.3
led[0] = (0, 0, 255)

TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"
JSON_URL = "http://api.coindesk.com/v1/bpi/currentprice/USD.json"

# PoE-FeatherWing connections
cs = digitalio.DigitalInOut(board.D10)
spi_bus = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
i2c = busio.I2C(board.SCL, board.SDA)

# Read the MAC from the 24AA02E48 chip
mac = get_mac(i2c)

# Initialize ethernet interface with DHCP and the MAC we have from the 24AA02E48
eth = WIZNET5K(spi_bus, cs, mac=mac, hostname="PoE-FeatherWing-{}")

# Initialize a requests object with a socket and ethernet interface
requests.set_socket(socket, eth)

print("Chip Version:", eth.chip)
print("MAC Address:", [hex(i) for i in eth.mac_address])
print("My IP address is:", eth.pretty_ip(eth.ip_address))
print(
    "IP lookup adafruit.com: %s" % eth.pretty_ip(eth.get_host_by_name("adafruit.com"))
)

print("Fetching text from", TEXT_URL)
r = requests.get(TEXT_URL)
print("-" * 40)
print(r.text)
print("-" * 40)
r.close()

print()
print("Fetching json from", JSON_URL)
r = requests.get(JSON_URL)
print("-" * 40)
print(r.json())
print("-" * 40)
r.close()

print("Done!")
led[0] = (0, 255, 0)

while True:
  time.sleep(1)

