"""Support for ReSpeaker Core v2"""
import os
import time

from evdev import InputDevice
from mycroft import Message
from pixel_ring import pixel_ring

from respeaker.corev2 import mraa
from respeaker.strategy import RespeakerStrategy
from mycroft.util.log import LOG


class CoreV2(RespeakerStrategy):
    """Strategy for respeaker core v2."""

    def __init__(self, bus, pattern) -> None:
        """Init."""
        super().__init__(bus, pattern)
        self.power = mraa.Gpio(12)

        self.user_key = None
        try:
            self.user_key = InputDevice("/dev/input/event0")
        except Exception as e:
            LOG.debug("exception while reading InputDevice: {}".format(e))

    def supports_button(self) -> bool:
        """Supports button."""
        return True

    def startup(self):
        """Startup of the LED pixel ring."""
        LOG.debug("[CoreV2] Start LED pixel ring.")
        if os.geteuid() != 0:
            time.sleep(1)
        self.power.dir(mraa.DIR_OUT)
        self.power.write(0)

        pixel_ring.set_brightness(20)
        if self.supports_pattern():
            pixel_ring.change_pattern(self.pattern)
        pixel_ring.wakeup()
        pixel_ring.off()

    def shutdown(self):
        """Shutdown LED pixel ring."""
        LOG.debug("[CoreV2] Stop LED pixel ring.")
        pixel_ring.off()
        self.power.write(1)

    def button_cb(self) -> None:
        """Implement user button logic."""
        if not self.user_key:
            return

        longpress_threshold = 2
        respeaker_userkey_code = 194

        if respeaker_userkey_code in self.user_key.active_keys():
            pressed_time = time.time()
            while respeaker_userkey_code in self.user_key.active_keys():
                time.sleep(0.2)
            pressed_time = time.time() - pressed_time
            if pressed_time < longpress_threshold:
                self.bus.emit(Message("mycroft.mic.listen"))
            else:
                self.bus.emit(Message("mycroft.stop"))
