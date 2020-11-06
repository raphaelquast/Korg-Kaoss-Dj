from functools import partial


class BaseComponent(object):
    '''base class for track-based assignments

    any provided buttonname will get a setter and listener assigned as follows:
        self.<BUTTONNAME>_button               # the button element
        self.<BUTTONNAME>_listener             # if defined, this listener will be assigned to the button as a value-listener
        self.set_<BUTTONNAME>_button           # a setter-function to set the button

    '''
    __module__ = __name__

    def __init__(self, parent, buttonnames=[], assign_track=0):
        self._parent = parent
        self._assign_track = assign_track

        self._track = self._parent.song().tracks[self._assign_track]

        self._buttonnames = buttonnames

        # define setter functions "set_button()" for all required buttons
        #  and assign the listeners "button_listener(value)" accordingly
        for name in self._buttonnames:
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

        listener_func = getattr(self, listener, None)
        assigned_button = getattr(self, name, None)

        # only if button is not yet assigned
        if assigned_button != button:
            if listener_func != None:
                if listener != None and button != None:
                    # remove existing listener
                    button.remove_value_listener(listener_func)
                    button.add_value_listener(listener_func)
                    # set the button
                    setattr(self, name, button)
            else:
                # just set the button
                setattr(self, name, button)


    def get_current_clip(self):
        playing_clip_idx = self._track.playing_slot_index
        if playing_clip_idx < 0:
            return self.get_selected_clip()
        else:
            return self.get_playing_clip()


    def get_selected_clip(self):
        '''find the currently selected clip'''
        clip_slot = self._parent.song().view.selected_scene.clip_slots[self._assign_track]

        if clip_slot != None:
            if clip_slot.has_clip:
                _current_clip = clip_slot.clip
            else:
                _current_clip = None
        else:
            _current_clip = None

        return _current_clip


    def get_playing_clip(self):
        '''find the currently playing clip of the assigned track-number,
        if none is playing, fall back to selected clip'''
        playing_clip_idx = self._track.playing_slot_index

        playing_clip = self._track.clip_slots[playing_clip_idx].clip

        return playing_clip

