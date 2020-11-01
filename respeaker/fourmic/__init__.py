"""Support for ReSpeaker 4-Mics Hat."""
from gpiozero import LED
from pixel_ring import pixel_ring

from respeaker.strategy import RespeakerStrategy
from mycroft.util.log import LOG


class Respeaker4Mic(RespeakerStrategy):
    """Strategy for respeaker 4 mic hat."""

    def __init__(self, bus, pattern) -> None:
        """Init."""
        super().__init__(bus, pattern)
        self.power = LED(5)

    def startup(self):
        """Startup of the LED pixel ring."""
        LOG.debug("[Respeaker4Mic] Start LED pixel ring.")
        self.power.on()
        pixel_ring.set_brightness(10)
        pixel_ring.change_pattern(self.pattern)
        pixel_ring.wakeup()

    def shutdown(self):
        """Shutdown LED pixel ring."""
        LOG.debug("[Respeaker4Mic] Stop LED pixel ring.")
        pixel_ring.off()
        self.power.off()
