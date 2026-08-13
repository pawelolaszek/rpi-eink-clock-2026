# *****************************************************************************
# * | File        :   epd2in7_V2.py
# * | Author      :   Waveshare team
# * | Function    :   2.7inch e-paper V2 driver
# * | Date        :   2022-09-17
# *****************************************************************************
# MIT License (Waveshare). Import path adapted for this project.
# *****************************************************************************

import logging
import epdconfig

EPD_WIDTH = 176
EPD_HEIGHT = 264

GRAY1 = 0xff
GRAY2 = 0xC0
GRAY3 = 0x80
GRAY4 = 0x00

BUSY_TIMEOUT_MS = 10000


class EPD:
    def __init__(self):
        self.reset_pin = epdconfig.RST_PIN
        self.dc_pin = epdconfig.DC_PIN
        self.busy_pin = epdconfig.BUSY_PIN
        self.cs_pin = epdconfig.CS_PIN
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self.GRAY1 = GRAY1
        self.GRAY2 = GRAY2
        self.GRAY3 = GRAY3
        self.GRAY4 = GRAY4

    def reset(self):
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(200)
        epdconfig.digital_write(self.reset_pin, 0)
        epdconfig.delay_ms(2)
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(200)

    def send_command(self, command):
        epdconfig.digital_write(self.dc_pin, 0)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte([command])
        epdconfig.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        epdconfig.digital_write(self.dc_pin, 1)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte([data])
        epdconfig.digital_write(self.cs_pin, 1)

    def ReadBusy(self):
        logging.debug("e-Paper busy")
        waited = 0
        # V2 / SSD1680: HIGH = busy, LOW = idle
        while epdconfig.digital_read(self.busy_pin) == 1:
            epdconfig.delay_ms(20)
            waited += 20
            if waited >= BUSY_TIMEOUT_MS:
                raise RuntimeError(
                    "e-paper stuck busy (BUSY stayed HIGH). "
                    "Reseat the HAT, confirm SPI is on, or try EPD_PANEL=v1 "
                    "if this is an original (non-V2) 2.7 inch panel."
                )
        logging.debug("e-Paper busy release")

    def TurnOnDisplay(self):
        self.send_command(0x22)
        self.send_data(0xF7)
        self.send_command(0x20)
        self.ReadBusy()

    def init(self):
        if epdconfig.module_init() != 0:
            return -1

        self.reset()
        self.ReadBusy()

        self.send_command(0x12)  # SWRESET
        self.ReadBusy()

        self.send_command(0x45)  # RAM Y start/end
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x07)
        self.send_data(0x01)

        self.send_command(0x4F)  # RAM Y counter
        self.send_data(0x00)
        self.send_data(0x00)

        self.send_command(0x11)  # data entry mode
        self.send_data(0x03)
        return 0

    def getbuffer(self, image):
        buf = [0xFF] * (int(self.width / 8) * self.height)
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()
        if imwidth == self.width and imheight == self.height:
            for y in range(imheight):
                for x in range(imwidth):
                    if pixels[x, y] == 0:
                        buf[int((x + y * self.width) / 8)] &= ~(0x80 >> (x % 8))
        elif imwidth == self.height and imheight == self.width:
            for y in range(imheight):
                for x in range(imwidth):
                    newx = y
                    newy = self.height - x - 1
                    if pixels[x, y] == 0:
                        buf[int((newx + newy * self.width) / 8)] &= ~(0x80 >> (y % 8))
        return buf

    def display(self, image):
        width = self.width // 8
        height = self.height
        self.send_command(0x24)
        for j in range(height):
            for i in range(width):
                self.send_data(image[i + j * width])
        self.TurnOnDisplay()

    def sleep(self):
        self.send_command(0x10)
        self.send_data(0x01)
        epdconfig.delay_ms(2000)
        epdconfig.module_exit()
