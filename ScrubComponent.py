from _Framework.ButtonElement import ButtonElement  # added
from _Framework.EncoderElement import EncoderElement  # added

from functools import partial



class ScrubComponent():
    'Handles looping controls'
    __module__ = __name__

    def __init__(self, parent, assign_track=0, increment_scrub=1, increment_fine=.1, increment_coarse=4):
        self._parent = parent
        self._assign_track = assign_track
        self._track = self._parent.song().tracks[self._assign_track]

        self._increment_scrub = increment_scrub
        self._increment_fine = increment_fine
        self._increment_coarse = increment_coarse

        self.scrub_position = 0

        buttonnames = ['_move_position', '_move_position_coarse', '_scrub_position', '_scrub_position_coarse', '_scrub_on_off']

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


    def _move_position_listener(self, value):
        self.move_position(value, self._increment_fine)

    def _move_position_coarse_listener(self, value):
        self.move_position(value, self._increment_coarse)


    def _scrub_on_off_listener(self, value):
        self._scrub_on_off(value)

    def _scrub_position_listener(self, value):
        self._parent.show_message('scrubbing... ' + str(value))
        self._scrub_position(value, self._increment_scrub)


    def _scrub_on_off(self, value):
        current_clip = self.get_current_clip()

        if value == 127:
            self.scrub_position = current_clip.playing_position
            self._parent.show_message('scrub START')
        if value == 0:
            current_clip.stop_scrub()
            self._parent.show_message('scrub STOP')

    def _scrub_position(self, value, increment):
        current_clip = self.get_current_clip()

        if value > 65:
            self.scrub_position -= increment
            current_clip.scrub(self.scrub_position)
        else:
            self.scrub_position += increment
            current_clip.scrub(self.scrub_position)

    def move_position(self, value, increment):
        current_clip = self.get_current_clip()

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
            playing_clip = self._track.clip_slots[playing_clip_idx].clip
        else:
            if track == self._parent.song().view.selected_track:
                playing_clip = self.get_selected_clip()
            else:
                playing_clip = None

        # self._parent.show_message(str(track.name) + '  |||  ' +
        #                           str(self._parent.song().view.selected_track.name) + '  |||   ' +
        #                           str(playing_clip) + '  |||  ' +
        #                           str(track.playing_slot_index) + '  |||  ' +
        #                           str(track == self._parent.song().view.selected_track))

        return playing_clip
