"""Strategy interface for different respeaker modules."""

from pixel_ring import pixel_ring


class RespeakerStrategy(object):
    """Strategy for Respeaker modules."""

    def __init__(self, bus, pattern) -> None:
        """Initialize."""
        self.pattern = pattern
        self.bus = bus

    def supports_button(self) -> bool:
        """Determines if the user button is supported."""
        return False

    def supports_pattern(self) -> bool:
        """Determines if the strategy supports custom patterns via pixel_ring."""
        return True

    def startup(self):
        """Setup the LED pixel ring."""
        raise NotImplementedError

    def shutdown(self):
        """Shutdown the LED pixel ring."""
        raise NotImplementedError

    def off(self) -> None:
        """Turn off the pixel ring."""
        pixel_ring.off()

    def speak(self) -> None:
        """Show speak interaction."""
        pixel_ring.speak()

    def wakeup(self) -> None:
        """Show wakeup interaction."""
        pixel_ring.listen()

    def think(self) -> None:
        """Show think interaction."""
        pixel_ring.think()

    def button_cb(self) -> None:
        """Callback for button handler."""
        raise NotImplementedError
