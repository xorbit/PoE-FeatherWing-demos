import board
import busio
import digitalio
import adafruit_requests as requests
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket

print("Wiznet5k WebClient Test")

TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"
JSON_URL = "http://api.coindesk.com/v1/bpi/currentprice/USD.json"

# W5500 connections
cs = digitalio.DigitalInOut(board.D10)
spi_bus = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Read the MAC from the 24AA02E48 chip
mac = bytearray((0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED))
i2c = busio.I2C(board.SCL, board.SDA)
while not i2c.try_lock():
    pass
i2c.writeto(0x50, bytearray((0xFA,)), stop=False)
i2c.readfrom_into(0x50, mac, start=0, end=6)
i2c.unlock()

# Initialize ethernet interface with DHCP and the MAC we have from the 24AA02E48
eth = WIZNET5K(spi_bus, cs, mac=mac)

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
