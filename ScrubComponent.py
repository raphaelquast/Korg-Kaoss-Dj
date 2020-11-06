from BaseComponent import BaseComponent

class ScrubComponent(BaseComponent):
    'Handles song-position controls'
    __module__ = __name__

    def __init__(self, parent, assign_track=0, increment_scrub=1, increment_fine=.1, increment_coarse=4,
                 *args, **kwargs):

        buttonnames = ['_move_position', '_move_position_coarse',
                       '_scrub_position', '_scrub_position_coarse',
                       '_scrub_on_off']

        super(ScrubComponent, self).__init__(parent, buttonnames, assign_track)


        self._increment_scrub = increment_scrub
        self._increment_fine = increment_fine
        self._increment_coarse = increment_coarse

        self.scrub_position = 0


    def _move_position_listener(self, value):
        self.move_position(value, self._increment_fine)

    def _move_position_coarse_listener(self, value):
        self.move_position(value, self._increment_coarse)


    def _scrub_on_off_listener(self, value):
        self._scrub_on_off(value)

    def _scrub_position_listener(self, value):
        self._scrub_position(value, self._increment_scrub)


    def _scrub_on_off(self, value):
        current_clip = self.get_current_clip()
        if current_clip != None:
            if value == 127:
                self.scrub_position = current_clip.playing_position
            if value == 0:
                current_clip.stop_scrub()

    def _scrub_position(self, value, increment):
        current_clip = self.get_current_clip()
        if current_clip != None:
            if current_clip.warping:
                if value > 65:
                    self.scrub_position -= increment
                    current_clip.scrub(self.scrub_position)
                else:
                    self.scrub_position += increment
                    current_clip.scrub(self.scrub_position)
            else:
                self._parent.show_message(str(current_clip.playing_position))
                current_clip.start_marker += 1

    def move_position(self, value, increment):
        current_clip = self.get_current_clip()
        if current_clip != None:
            if current_clip.looping:
                if value > 65:
                    current_clip.position -= increment
                else:
                    current_clip.position += increment
            else:

                if value > 65:
                    current_clip.loop_start -= increment
                else:
                    current_clip.loop_start += increment


    def update_lights(self):
        clip = self.get_playing_clip()

        if clip != None and clip.looping:
            self._loop_start_button.turn_on()
        else:
            self._loop_start_button.turn_off()
