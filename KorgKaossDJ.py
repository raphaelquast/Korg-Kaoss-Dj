import Live # This allows us (and the Framework methods) to use the Live API on occasion
import time # We will be using time functions for time-stamping our log file outputs

""" All of the Framework files are listed below, but we are only using using some of them in this script (the rest are commented out) """
from _Framework.ButtonElement import ButtonElement # Class representing a button a the controller
from _Framework.ButtonMatrixElement import ButtonMatrixElement # Class representing a 2-dimensional set of buttons
#from _Framework.ButtonSliderElement import ButtonSliderElement # Class representing a set of buttons used as a slider
from _Framework.ChannelStripComponent import ChannelStripComponent # Class attaching to the mixer of a given track
#from _Framework.ChannelTranslationSelector import ChannelTranslationSelector # Class switches modes by translating the given controls' message channel
from _Framework.ClipSlotComponent import ClipSlotComponent # Class representing a ClipSlot within Live
from _Framework.CompoundComponent import CompoundComponent # Base class for classes encompasing other components to form complex components
from _Framework.ControlElement import ControlElement # Base class for all classes representing control elements on a controller
from _Framework.ControlSurface import ControlSurface # Central base class for scripts based on the new Framework
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent # Base class for all classes encapsulating functions in Live
from _Framework.DeviceComponent import DeviceComponent # Class representing a device in Live
#from _Framework.DisplayDataSource import DisplayDataSource # Data object that is fed with a specific string and notifies its observers
from _Framework.EncoderElement import EncoderElement # Class representing a continuous control on the controller
from _Framework.InputControlElement import * # Base class for all classes representing control elements on a controller
#from _Framework.LogicalDisplaySegment import LogicalDisplaySegment # Class representing a specific segment of a display on the controller
from _Framework.MixerComponent import MixerComponent # Class encompassing several channel strips to form a mixer
#from _Framework.ModeSelectorComponent import ModeSelectorComponent # Class for switching between modes, handle several functions with few controls
#from _Framework.NotifyingControlElement import NotifyingControlElement # Class representing control elements that can send values
#from _Framework.PhysicalDisplayElement import PhysicalDisplayElement # Class representing a display on the controller
from _Framework.SceneComponent import SceneComponent # Class representing a scene in Live

#from _Framework.SessionComponent import SessionComponent # Class encompassing several scene to cover a defined section of Live's session

from _Framework.SessionZoomingComponent import SessionZoomingComponent # Class using a matrix of buttons to choose blocks of clips in the session
from _Framework.SliderElement import SliderElement # Class representing a slider on the controller
#from _Framework.TrackEQComponent import TrackEQComponent # Class representing a track's EQ, it attaches to the last EQ device in the track
#from _Framework.TrackFilterComponent import TrackFilterComponent # Class representing a track's filter, attaches to the last filter in the track
from _Framework.Layer import Layer
from _Framework.Resource import PrioritizedResource


from LooperComponent import LooperComponent
from ScrubComponent import ScrubComponent
# import this from _Arturia to get the "set_scene_select_control()" function
from _Arturia.SessionComponent import SessionComponent

#from _Framework.TransportComponent import TransportComponent # Class encapsulating all functions in Live's transport section
from TransportComponent import TransportComponent
from FXComponent import FXComponent

""" Here we define some global variables """
CHANNEL_CENTER = 6
CHANNEL_LEFT = 7
CHANNEL_RIGHT = 8


LEFT_STRIP_ID = 0
RIGHT_STRIP_ID = 1



class KorgKaossDJ(ControlSurface):
    __module__ = __name__
    __doc__ = " Korg Kaoss DJ controller script "

    def __init__(self, c_instance):
        """everything except the '_on_selected_track_changed' override and 'disconnect' runs from here"""
        ControlSurface.__init__(self, c_instance)

        self._selected_track = None
        self._current_clip = None

        with self.component_guard():
            self._create_controls()
            self._setup_transport_control() # Run the transport setup part of the script
            self._setup_loop_control()
            self._setup_scrub_control()
            self._setup_fx_control()
            self._setup_mixer_control() # Setup the mixer object
            self._setup_session_control()  # Setup the session object

    def _create_controls(self):

        # ------ SLIDER
        self._crossfader_slider = SliderElement(MIDI_CC_TYPE, CHANNEL_CENTER, 23)

        self._left_volume_slider = SliderElement(MIDI_CC_TYPE, CHANNEL_LEFT, 24)
        self._right_volume_slider = SliderElement(MIDI_CC_TYPE, CHANNEL_RIGHT, 24)

        self._left_tempo_fader = SliderElement(MIDI_CC_TYPE, CHANNEL_LEFT, 25)
        self._right_tempo_fader = SliderElement(MIDI_CC_TYPE, CHANNEL_RIGHT, 25)

        # ------ BUTTONS
        self._left_play_button = ButtonElement(True, MIDI_NOTE_TYPE, CHANNEL_LEFT, 27)
        self._right_play_button = ButtonElement(True, MIDI_NOTE_TYPE, CHANNEL_RIGHT, 27)

        self._left_prelisten_button = ButtonElement(True, MIDI_NOTE_TYPE, CHANNEL_LEFT, 25)
        self._right_prelisten_button = ButtonElement(True, MIDI_NOTE_TYPE, CHANNEL_RIGHT, 25)

        self._left_fx_button = ButtonElement(True, MIDI_NOTE_TYPE, CHANNEL_LEFT, 24)
        self._right_fx_button = ButtonElement(True, MIDI_NOTE_TYPE, CHANNEL_RIGHT, 24)

        self._left_A_button = ButtonElement(True, MIDI_NOTE_TYPE, CHANNEL_LEFT, 14)
        self._right_B_button = ButtonElement(True, MIDI_NOTE_TYPE, CHANNEL_RIGHT, 14)


        self._left_shift_button = ButtonElement(True, MIDI_NOTE_TYPE, CHANNEL_LEFT, 26, name='Shift_Button', resource_type=PrioritizedResource)
        self._right_shift_button = ButtonElement(True, MIDI_NOTE_TYPE, CHANNEL_RIGHT, 26, name='Shift_Button', resource_type=PrioritizedResource)


        for i in range(3):
            for side, channel in zip(['_left', '_right'],
                                     [CHANNEL_LEFT, CHANNEL_RIGHT]):
                setattr(self, side + '_loop_' + str(i + 1),
                        ButtonElement(True, MIDI_NOTE_TYPE, channel, 15 + i))
                setattr(self, side + '_loop_' + str(i + 1) + '_shift',
                        ButtonElement(True, MIDI_NOTE_TYPE, channel, 40 + i))
                setattr(self, side + '_hotcue_' + str(i + 1),
                        ButtonElement(True, MIDI_NOTE_TYPE, channel, 18 + i))
                setattr(self, side + '_hotcue_' + str(i + 1) + '_shift',
                        ButtonElement(True, MIDI_NOTE_TYPE, channel, 43 + i))

        # ------ ENCODER

        # browser
        self._center_browse_encoder = EncoderElement(MIDI_CC_TYPE, CHANNEL_CENTER, 30,
                                                     Live.MidiMap.MapMode.relative_smooth_two_compliment)
        # gain left
        self._left_gain_encoder = EncoderElement(MIDI_CC_TYPE, CHANNEL_LEFT, 26,
                                                     Live.MidiMap.MapMode.absolute)
        # gain right
        self._right_gain_encoder = EncoderElement(MIDI_CC_TYPE, CHANNEL_RIGHT, 26,
                                                     Live.MidiMap.MapMode.absolute)

        # middle light off -> does not send on-off messages!
        self._left_jogwheel_encoder = EncoderElement(MIDI_CC_TYPE, CHANNEL_LEFT, 14,
                                                     Live.MidiMap.MapMode.relative_smooth_two_compliment)
        self._right_jogwheel_encoder = EncoderElement(MIDI_CC_TYPE, CHANNEL_RIGHT, 14,
                                                      Live.MidiMap.MapMode.relative_smooth_two_compliment)

        self._left_jogwheel_encoder_shift = EncoderElement(MIDI_CC_TYPE, CHANNEL_LEFT, 15,
                                                           Live.MidiMap.MapMode.relative_smooth_two_compliment)
        self._right_jogwheel_encoder_shift = EncoderElement(MIDI_CC_TYPE, CHANNEL_RIGHT, 15,
                                                            Live.MidiMap.MapMode.relative_smooth_two_compliment)

        # middle light on  -> sends on-off message on channel 31!
        self._left_jogwheel_encoder_active = EncoderElement(MIDI_CC_TYPE, CHANNEL_LEFT, 16,
                                                     Live.MidiMap.MapMode.relative_smooth_two_compliment)
        self._left_jogwheel_encoder_active_button = ButtonElement(True, MIDI_NOTE_TYPE, CHANNEL_LEFT, 31)

        self._right_jogwheel_encoder_active = EncoderElement(MIDI_CC_TYPE, CHANNEL_RIGHT, 16,
                                                      Live.MidiMap.MapMode.relative_smooth_two_compliment)
        self._right_jogwheel_encoder_active_button = ButtonElement(True, MIDI_NOTE_TYPE, CHANNEL_RIGHT, 31)


    	# FX touchpad (same for both channels so we need to read only one)
        self._touchpad_x_encoder = EncoderElement(MIDI_CC_TYPE, CHANNEL_LEFT, 12,
                                                  Live.MidiMap.MapMode.absolute)
        self._touchpad_y_encoder = EncoderElement(MIDI_CC_TYPE, CHANNEL_LEFT, 13,
                                                  Live.MidiMap.MapMode.absolute)
        self._touchpad_x_encoder_shift = EncoderElement(MIDI_CC_TYPE, CHANNEL_CENTER, 17,
                                                  Live.MidiMap.MapMode.absolute)
        self._touchpad_y_encoder_shift = EncoderElement(MIDI_CC_TYPE, CHANNEL_CENTER, 18,
                                                  Live.MidiMap.MapMode.absolute)

        # hi-mid-lo encoders
        _device_MSG_IDS = [27, 28, 29]
        self._device_encoders = ButtonMatrixElement(
            rows=[[EncoderElement(MIDI_CC_TYPE, CHANNEL_LEFT, MSG_ID, Live.MidiMap.MapMode.absolute) for MSG_ID in _device_MSG_IDS],
                  [EncoderElement(MIDI_CC_TYPE, CHANNEL_RIGHT, MSG_ID, Live.MidiMap.MapMode.absolute) for MSG_ID in _device_MSG_IDS]
                  ])


    def _setup_loop_control(self):
        # set looping function ality to Loop- and HotCue buttons
        self._looper_left = LooperComponent(self,
                                            assign_track=0, move_increment=4,
                                            increase_factor=(0, 2), decrease_factor=(0, 2),
                                            start_loop_length = 32, quantize_start=4)
        self._looper_right = LooperComponent(self, assign_track=1, move_increment=4,
                                             increase_factor=(0, 2), decrease_factor=(0, 2),
                                             start_loop_length = 32, quantize_start=1)

        self._looper_left_fine = LooperComponent(self, assign_track=0, move_increment=1,
                                                 increase_factor=(1, 1), decrease_factor=(1, 1),
                                                 start_loop_length = 16, quantize_start=1)
        self._looper_right_fine = LooperComponent(self, assign_track=1, move_increment=1,
                                                  increase_factor=(1, 1), decrease_factor=(1, 1),
                                                  start_loop_length = 16, quantize_start=1)


        self._looper_left.set_loop_decrease_button(self._left_loop_1)
        self._looper_left.set_loop_start_button(self._left_loop_2)
        self._looper_left.set_loop_increase_button(self._left_loop_3)
        self._looper_left.set_loop_move_left_button(self._left_loop_1_shift)
        self._looper_left.set_loop_toggle_button(self._left_loop_2_shift)
        self._looper_left.set_loop_move_right_button(self._left_loop_3_shift)

        self._looper_left_fine.set_loop_decrease_button(self._left_hotcue_1)
        self._looper_left_fine.set_loop_start_button(self._left_hotcue_2)
        self._looper_left_fine.set_loop_increase_button(self._left_hotcue_3)
        self._looper_left_fine.set_loop_move_left_button(self._left_hotcue_1_shift)
        self._looper_left_fine.set_loop_toggle_button(self._left_hotcue_2_shift)
        self._looper_left_fine.set_loop_move_right_button(self._left_hotcue_3_shift)


        self._looper_right.set_loop_decrease_button(self._right_loop_1)
        self._looper_right.set_loop_start_button(self._right_loop_2)
        self._looper_right.set_loop_increase_button(self._right_loop_3)
        self._looper_right.set_loop_move_left_button(self._right_loop_1_shift)
        self._looper_right.set_loop_toggle_button(self._right_loop_2_shift)
        self._looper_right.set_loop_move_right_button(self._right_loop_3_shift)

        self._looper_right_fine.set_loop_decrease_button(self._right_hotcue_1)
        self._looper_right_fine.set_loop_start_button(self._right_hotcue_2)
        self._looper_right_fine.set_loop_increase_button(self._right_hotcue_3)
        self._looper_right_fine.set_loop_move_left_button(self._right_hotcue_1_shift)
        self._looper_right_fine.set_loop_toggle_button(self._right_hotcue_2_shift)
        self._looper_right_fine.set_loop_move_right_button(self._right_hotcue_3_shift)


    def _setup_scrub_control(self):
        self._scrub_left = ScrubComponent(self, assign_track=LEFT_STRIP_ID, increment_scrub=1, increment_fine=0.1)
        self._scrub_right = ScrubComponent(self, assign_track=RIGHT_STRIP_ID, increment_scrub=1, increment_fine=0.1)

        self._scrub_left.set_move_position_button(self._left_jogwheel_encoder)
        self._scrub_left.set_move_position_coarse_button(self._left_jogwheel_encoder_shift)
        self._scrub_left.set_scrub_position_button(self._left_jogwheel_encoder_active)
        self._scrub_left.set_scrub_on_off_button(self._left_jogwheel_encoder_active_button)

        self._scrub_right.set_move_position_button(self._right_jogwheel_encoder)
        self._scrub_right.set_move_position_coarse_button(self._right_jogwheel_encoder_shift)
        self._scrub_right.set_scrub_position_button(self._right_jogwheel_encoder_active)
        self._scrub_right.set_scrub_on_off_button(self._right_jogwheel_encoder_active_button)


    def _setup_fx_control(self):
        self._fx_left = FXComponent(self, assign_track=LEFT_STRIP_ID)
        self._fx_left.set_touchpad_x_button(self._touchpad_x_encoder)
        self._fx_left.set_touchpad_y_button(self._touchpad_y_encoder)
        self._fx_left.set_touchpad_x_shift_button(self._touchpad_x_encoder_shift)
        self._fx_left.set_touchpad_y_shift_button(self._touchpad_y_encoder_shift)
        self._fx_left.set_fx_on_off_button(self._left_fx_button)
        self._fx_left.set_gain_encoder_button(self._left_gain_encoder)

        self._fx_right = FXComponent(self, assign_track=RIGHT_STRIP_ID)
        self._fx_right.set_touchpad_x_button(self._touchpad_x_encoder)
        self._fx_right.set_touchpad_y_button(self._touchpad_y_encoder)
        self._fx_right.set_touchpad_x_shift_button(self._touchpad_x_encoder_shift)
        self._fx_right.set_touchpad_y_shift_button(self._touchpad_y_encoder_shift)
        self._fx_right.set_fx_on_off_button(self._right_fx_button)
        self._fx_right.set_gain_encoder_button(self._right_gain_encoder)



    def _setup_transport_control(self):
        """set up the sliders"""

        self._transport = TransportComponent(self,
                                             name=u'Transport',
                                             is_enabled=False)

        #set tempo-fader
        self._transport.set_tempo_control(self._left_tempo_fader,
                                          fine_control=self._right_tempo_fader) #(control, fine_control)

        self._transport.set_enabled(True)


    def _setup_mixer_control(self):
        self._mixer = MixerComponent(num_tracks=2, num_returns=0, name=u'Mixer',
                                     is_enabled=False)

        self._mixer.set_crossfader_control(self._crossfader_slider)

        # set volume sliders
        self._mixer.channel_strip(LEFT_STRIP_ID).set_volume_control(self._left_volume_slider)
        self._mixer.channel_strip(RIGHT_STRIP_ID).set_volume_control(self._right_volume_slider)

        # set prelisten buttons
        self._mixer.channel_strip(LEFT_STRIP_ID).set_solo_button(self._left_prelisten_button)
        self._mixer.channel_strip(RIGHT_STRIP_ID).set_solo_button(self._right_prelisten_button)

        # use fx buttons to select a track
        self._mixer.channel_strip(LEFT_STRIP_ID).set_select_button(self._left_A_button)
        self._mixer.channel_strip(RIGHT_STRIP_ID).set_select_button(self._right_B_button)



        self._mixer.set_enabled(True)


    def _setup_session_control(self):
        self._session = SessionComponent(num_tracks=2, num_scenes=1, name=u'Session',
                                         is_enabled=False)

        # set horizontal scene selector (this is why we import SessionComponent from _Arturia!)
        self._session.set_scene_select_control(self._center_browse_encoder)

        # set launch-buttons for scene
        self._session.selected_scene().clip_slot(0).set_launch_button(self._left_play_button)
        self._session.selected_scene().clip_slot(1).set_launch_button(self._right_play_button)

        # hightlite the current selection
        self.set_highlighting_session_component(self._session)
        self._session.set_enabled(True)


        # ----------- add functionality to turn playing-light on-off
        def update_lights(track, button):
            playing_clip_idx = track.playing_slot_index
            if playing_clip_idx >= 0:
                button.turn_on()
            else:
                button.turn_off()

        def update_playlight_left():
            track = self.song().tracks[LEFT_STRIP_ID]
            update_lights(track, self._left_play_button)
        def update_playlight_right():
            track = self.song().tracks[RIGHT_STRIP_ID]
            update_lights(track, self._right_play_button)

        self.song().tracks[LEFT_STRIP_ID].add_playing_slot_index_listener(update_playlight_left)
        self.song().tracks[RIGHT_STRIP_ID].add_playing_slot_index_listener(update_playlight_right)
        # override the selected scene change behaviour of the playing light
        self.song().view.add_selected_scene_listener(update_playlight_left)
        self.song().view.add_selected_scene_listener(update_playlight_right)
        # ---------

