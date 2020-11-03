"""Support for respeaker array v2.0."""
from pixel_ring import pixel_ring

from ..strategy import RespeakerStrategy
from mycroft.util.log import LOG


class RespeakerArrayV2(RespeakerStrategy):
    """Strategy for respeaker array v2.0."""

    def __init__(self, bus, pattern) -> None:
        """Init."""
        super().__init__(bus, pattern)

    def supports_pattern(self) -> bool:
        """Initialise pattern support."""
        return False

    def startup(self):
        """Startup of the LED pixel ring."""
        LOG.debug("[RespeakerArrayV2] Start LED pixel ring.")
        pixel_ring.set_brightness(10)
        pixel_ring.wakeup()

    def shutdown(self):
        """Shutdown LED pixel ring."""
        LOG.debug("[RespeakerArrayV2] Stop LED pixel ring.")
        pixel_ring.off()
