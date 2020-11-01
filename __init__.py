# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from mycroft.skills.core import MycroftSkill, intent_handler
from adapt.intent import IntentBuilder

from respeaker import obtain_strategy, RespeakerStrategy


class ReSpeaker(MycroftSkill):

    def __init__(self):
        super(ReSpeaker, self).__init__(name="ReSpeaker")
        self.strategy: RespeakerStrategy = None

    def initialize(self):
        self.log.info("Pixel Ring: Initializing")
        self.strategy = obtain_strategy('echo', self.bus)

        self.strategy.startup()

        self.enable()

    def enable(self):
        self.log.info("Pixel Ring: Enabling")

        self.add_event('recognizer_loop:wakeword',
                       self.handle_listener_wakeup)
        self.add_event('recognizer_loop:record_end',
                       self.handle_listener_off)

        self.add_event('mycroft.skill.handler.start',
                       self.handle_listener_think)
        self.add_event('mycroft.skill.handler.complete',
                       self.handle_listener_off)

        self.add_event('recognizer_loop:audio_output_start',
                       self.handler_listener_speak)
        self.add_event('recognizer_loop:audio_output_end',
                       self.handle_listener_off)

        if self.strategy.supports_button():
            self.schedule_repeating_event(self.strategy.button_cb, None, 0.1,
                                          name='respeaker_button_cb')

        self.strategy.off()

    def disable(self):
        self.log.info("Pixel Ring: Disabling")
        self.remove_event('recognizer_loop:wakeup')
        self.remove_event('recognizer_loop:record_end')
        self.remove_event('recognizer_loop:audio_output_start')
        self.remove_event('recognizer_loop:audio_output_end')
        self.remove_event('mycroft.skill.handler.start')
        self.remove_event('mycroft.skill.handler.complete')

        if self.strategy.supports_button():
            self.cancel_scheduled_event("respeaker_button_cb")

    def shutdown(self):
        self.log.info("Pixel Ring: Shutdown")
        self.strategy.shutdown()

    def handle_listener_wakeup(self, message):
        self.log.info("Pixel Ring: Wakeup")
        self.strategy.wakeup()

    def handle_listener_off(self, message):
        self.log.info("Pixel Ring: Off")
        self.strategy.off()

    def handle_listener_think(self, message):
        self.log.info("Pixel Ring: Think")
        self.strategy.think()

    def handler_listener_speak(self, message):
        self.log.info("Pixel Ring: Speak")
        self.strategy.speak()

    @intent_handler(IntentBuilder("").require("EnablePixelRing"))
    def handle_enable_pixel_ring_intent(self, message):
        self.enable()
        self.speak_dialog("EnablePixelRing")

    @intent_handler(IntentBuilder("").require("DisablePixelRing"))
    def handle_disable_pixel_ring_intent(self, message):
        self.disable()
        self.speak_dialog("DisablePixelRing")


def create_skill():
    return ReSpeaker()
