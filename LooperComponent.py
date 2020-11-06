from _Framework.ButtonElement import ButtonElement  # added
from _Framework.EncoderElement import EncoderElement  # added

from functools import partial
from BaseComponent import BaseComponent


class LooperComponent(BaseComponent):
    'Handles looping controls'
    __module__ = __name__

    def __init__(self, parent, assign_track=0, move_increment=4,
                 increase_factor=(0, 2), decrease_factor=(0, 2),
                 start_loop_length = 32, quantize_start=1):

        buttonnames = ['_loop_toggle', '_loop_start',
                       '_loop_increase', '_loop_decrease',
                       '_loop_move_left', '_loop_move_right']

        super(LooperComponent, self).__init__(parent, buttonnames, assign_track)

        # the initial length of the loop
        self._start_loop_length = start_loop_length
        # the move increment (in beats)
        self._move_increment = move_increment
        # the increase factors   length = A + B * length
        self._increase_A, self._increase_B = increase_factor
        # the decrease factors   length = length/B - A
        self._decrease_A, self._decrease_B = decrease_factor
        # the quantization factor for starting a loop at the current playing position
        self._quantize_start = quantize_start


        # update lights if the playing clip changed
        self._parent.song().tracks[self._assign_track].add_playing_slot_index_listener(self._playing_slot_index_listener)

        # update lights on scene selection change (necessary if track is not playing)
        self._parent.song().view.add_selected_scene_listener(self._selected_scene_listener)


    def _loop_toggle_listener(self, value):
        if value > 0:
            current_clip = self.get_current_clip()
            if current_clip is not None:
                if current_clip.looping == 1:
                    current_clip.looping = 0
                    #self._loop_start_button.turn_off()
                else:
                    current_clip.looping = 1
                    #self._loop_start_button.turn_on()

    def _loop_start_listener(self, value):
        if value > 0:
            current_clip = self.get_current_clip()
            if current_clip is not None:

                # toggle loop in case it has already been running
                if current_clip.looping == 1:
                    current_clip.looping = 0
                    #self._loop_start_button.turn_off()
                else:
                    playing_position = round(current_clip.playing_position / self._quantize_start) * self._quantize_start
                    current_clip.looping = 1
                    # do this in addition to setting start- and end-point to avoid
                    # a bug in case scrobbling is used prior to moving the loop
                    current_clip.position = playing_position

                    current_clip.loop_start = playing_position
                    current_clip.loop_end = playing_position + self._start_loop_length
                    #self._loop_start_button.turn_on()

    def _loop_increase_listener(self, value):
        if value > 0:
            self._resize_loop(A=self._increase_A,
                              B=float(self._increase_B))

    def _loop_decrease_listener(self, value):
        if value > 0:
            self._resize_loop(A=-self._decrease_A,
                              B=1./float(self._decrease_B))

    def _loop_move_left_listener(self, value):
        if value > 0:
            self._move_loop(direction=-1)

    def _loop_move_right_listener(self, value):
        if value > 0:
            self._move_loop(direction=1)

    def _resize_loop(self, A, B):
        current_clip = self.get_current_clip()
        if current_clip is not None:
            was_playing = current_clip.looping

            current_clip.looping = 1

            loop_length = round(current_clip.loop_end -
                                current_clip.loop_start)

            current_clip.loop_end = (current_clip.loop_start +
                                     A + loop_length * B)

            if was_playing == 0:
                current_clip.looping = 0

    def _move_loop(self, direction=1):
        current_clip = self.get_current_clip()
        if current_clip is not None:

            if current_clip.looping:
                current_clip.position = round(current_clip.position +
                                              direction * self._move_increment)
            else:
                # temporarily set looping to 1 to avoid a nasty bug that sets
                # the clip-start and end-position instead of the loop-position
                # in case the loop is disabled
                current_clip.looping = 1
                current_clip.position = round(current_clip.position +
                                              direction * self._move_increment)
                current_clip.looping = 0


    def _playing_slot_index_listener(self):
        clip = self.get_playing_clip()

        self.update_lights()

        # add a playing position listener to have a blinking light
        if clip is not None and not clip.playing_position_has_listener(self._playing_position_listener):
            clip.add_playing_position_listener(self._playing_position_listener)

        # add also a static looping listener to get an indicator even if no track is playing
        if clip is not None and not clip.looping_has_listener(self.update_lights):
            clip.add_looping_listener(self.update_lights)


    def _playing_position_listener(self):
        clip = self.get_playing_clip()

        if clip is not None:
            if (clip.is_playing or clip.is_triggered) and clip.looping:
                if round(clip.playing_position*10%10) > 5:
                    self._loop_start_button.turn_on()
                else:
                    self._loop_start_button.turn_off()
            else:
                self._loop_start_button.turn_off()


    def _selected_scene_listener(self):
        clip = self.get_playing_clip()

        self.update_lights()

        if clip is not None and not clip.looping_has_listener(self.update_lights):
            clip.add_looping_listener(self.update_lights)

        if clip is not None and not clip.playing_position_has_listener(self._playing_position_listener):
            clip.add_playing_position_listener(self._playing_position_listener)


    def update_lights(self):
        clip = self.get_playing_clip()

        if clip is not None and clip.looping:
            self._loop_start_button.turn_on()
        else:
            self._loop_start_button.turn_off()

