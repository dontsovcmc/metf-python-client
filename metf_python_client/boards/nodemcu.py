
# Pin maping
# NodeMCU - ESP8266 GPIO
# https://randomnerdtutorials.com/esp8266-pinout-reference-gpios/

         # IN        #   OUT  #

D0 = 16  # no        # no PWM or i2c support #  HIGH at boot used to wake up from deep sleep
         # interrupt #

D1 = 5   # +        #  +     # often used as SCL (I2C)

D2 = 4   # +        #  +     # often used as  SDA (I2C)

D3 = 0   # pulled   #  +     # connected to FLASH button, boot fails if pulled LOW
         # UP       #

D4 = 2   # pulled   #
         # UP       #  +     #  HIGH at boot,  connected to on-board LED, boot fails if pulled LOW

D5 = 14  # +        #  +     #  SPI (SCLK)

D6 = 12  # +        #  +     #  SPI (MISO)

D7 = 13  # +        #  +     #  SPI (MOSI)

D8 = 15  # pulled   #  +     #  SPI (CS), Boot fails if pulled HIGH
         # to GND   #

D9 = 3   # +        # RX pin #  HIGH at boot

D10 = 1  # TX pin   #  +     #  HIGH at boot. debug output at boot, boot fails if pulled LOW

#A0 = ADC0 # analog input   # -  #
RX = D9
TX = D10

LED_BUILTIN = D4
LED_BUILTIN_AUX = D0


