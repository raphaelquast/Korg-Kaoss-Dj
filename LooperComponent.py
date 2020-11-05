from _Framework.ButtonElement import ButtonElement  # added
from _Framework.EncoderElement import EncoderElement  # added

from functools import partial



class LooperComponent():
    'Handles looping controls'
    __module__ = __name__

    def __init__(self, parent, assign_track=0, move_increment=4,
                 increase_factor=(0, 2), decrease_factor=(0, 2),
                 start_loop_length = 32):
        self._parent = parent
        self._start_loop_length = start_loop_length

        # track-index to which the controls will be sensitive
        self._assign_track = assign_track
        # the move increment (in beats)
        self._move_increment = move_increment
        # the increase factors   length = A + B * length
        self._increase_A, self._increase_B = increase_factor
        # the decrease factors   length = length/B - A
        self._decrease_A, self._decrease_B = decrease_factor


        buttonnames = ['_loop_toggle', '_loop_start',
                       '_loop_increase', '_loop_decrease',
                       '_loop_move_left', '_loop_move_right']

        # define setter functions "set_button()" for all required buttons
        #  and assign the listeners "button_listener(value)" accordingly
        for name in buttonnames:
            buttonname = name + '_button'
            listener = name + '_listener'
            setter = 'set' + buttonname

            # set all buttons to None
            setattr(self, buttonname, None)
            # define setter functions
            setattr(self, setter,
                    partial(self._set_a_button, name=buttonname,
                            listener=listener))


    def _set_a_button(self, button, name, listener):
        '''
        a generic setter function for the buttons
        '''
        assert ((button is None) or (isinstance(button, ButtonElement)
                                      and button.is_momentary()))
        # only if button is not yet assigned
        if getattr(self, name) != button:
            # remove existing listener
            if listener is not None and getattr(self, name) is not None:
                getattr(self, name
                        ).remove_value_listener(getattr(self, listener))

            # set the button
            setattr(self, name, button)
            if listener is not None and getattr(self, name) is not None:
                getattr(self, name
                        ).add_value_listener(getattr(self, listener))


    def _loop_toggle_listener(self, value):
        if value > 0:
            current_clip = self.get_current_clip()
            if current_clip is not None:
                if current_clip.looping == 1:
                    current_clip.looping = 0
                    self._loop_toggle_button.turn_off()
                else:
                    current_clip.looping = 1
                    self._loop_toggle_button.turn_on()

    def _loop_start_listener(self, value):
        if value > 0:
            current_clip = self.get_current_clip()
            if current_clip is not None:
                playing_position = round(current_clip.playing_position)
                current_clip.looping = 1
                # do this in addition to setting start- and end-point to avoid
                # a bug in case scrobbling is used prior to moving the loop
                current_clip.position = round(playing_position)

                current_clip.loop_start = playing_position
                current_clip.loop_end = playing_position + self._start_loop_length
                self._loop_toggle_button.set_light(1)

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

    def get_current_clip(self):
        if self._assign_track == -1:
            return self.get_selected_clip()
        else:

            return self.get_playing_clip()

    def get_selected_clip(self):
        '''find the currently selected clip'''
        if (self._parent.song().view.highlighted_clip_slot is not None):
            clip_slot = self._parent.song().view.highlighted_clip_slot
            if clip_slot.has_clip:
                _current_clip = clip_slot.clip
            else:
                _current_clip = None
        else:
            _current_clip = None

        return _current_clip

    def get_playing_clip(self):
        '''find the currently playing clip of the assigned track-number'''
        track = self._parent.song().tracks[self._assign_track]
        playing_clip_idx = track.playing_slot_index


        if playing_clip_idx >= 0:
            playing_clip = track.clip_slots[playing_clip_idx].clip
        else:
            if track == self._parent.song().view.selected_track:
                playing_clip = self.get_selected_clip()
            else:
                playing_clip = None

        return playing_clip
