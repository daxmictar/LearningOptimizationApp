"""
Attention API for collecting attention data and handling its state

Priority Order for API calls:
-----------------------------
setup_attention > start_attention > end_attention > fill_attention_data > clear_attention_data

setup_attention is required to begin the process. Clear attention data also clears the emotions object,
which requires another call to setup_attention.

"""

import math, asyncio

from dataclasses import dataclass

from em_st_artifacts.utils.support_classes import RawChannelsArray, RawChannels, MindData, RawSpectVals, SpectralDataPercents

from em_st_artifacts.emotional_math import EmotionalMath

from em_st_artifacts.utils.lib_settings import MathLibSetting, ArtifactDetectSetting, ShortArtifactDetectSetting, \
    MentalAndSpectralSetting

from tools.logging import logger

from tools.session import session_rating_append


"""
Code simulation Section
"""

paid_attention: float = 0.00
attention_valid: bool = False


def set_paid_attention(new_attention_val: float, log=False):
    global paid_attention, attention_valid

    logger.debug(f"New attention value: {new_attention_val}") if log else None

    paid_attention = new_attention_val

    session_rating_append(new_attention_val)

    attention_valid = True


def get_paid_attention(log=False):
    global paid_attention, attention_valid

    if attention_valid != True:
        logger.log("set_attention_paid was not used") if log else None
        return 0

    """ 
        Will update based on user interaction with a button on the JS side.
    """
    if log:
        debug_msg = ""
        match (paid_attention):
            case 0.0: 
                debug_msg = "User paid no attention"
            case 1.0:
                debug_msg = "User paid little attention"
            case 2.0:
                debug_msg = "User paid some attention"
            case 3.0:
                debug_msg = "User paid moderate attention"
            case 4.0:
                debug_msg = "User paid significant attention"
            case 5.0:
                debug_msg = "User paid full attention"
            case _:
                debug_msg = "Bad value"

        logger.debug(debug_msg) 

    return paid_attention


def reset_attention_paid(log=False):
    global paid_attention, attention_valid

    paid_attention = 0.0
    attention_valid = False


# calibration settings for EmotionalMath object from sample.py
CALIBRATION_LENGTH = 8
NWINS_SKIP_AFTER_ARTIFACT = 10
MATH_LIB_SETTING = MathLibSetting(sampling_rate=250,
                         process_win_freq=25,
                         fft_window=1000,
                         n_first_sec_skipped=4,
                         bipolar_mode=True,
                         channels_number=4,
                         channel_for_analysis=3)

ARTIFACT_DETECT_SETTING = ArtifactDetectSetting(hanning_win_spectrum=True, num_wins_for_quality_avg=125)
SHORT_ARTIFACT_DETECT_SETTING = ShortArtifactDetectSetting(ampl_art_extremum_border=25)
MENTAL_AND_SPECTRAL_SETTING = MentalAndSpectralSetting()

# global vars for storing data
attention_handler: EmotionalMath = None
attention_data: list[RawChannels] = []

# trying this with async
# Goal: set a flag that maintains the attention data collection loop
# it will stop when the post to 'end_attention' is called.
attention_capture_conc = asyncio.Event()

attention_capture: bool = False

# API Return Messages
ATTENTION_CREATED = "Created Attention"
ATTENTION_STARTED = "Started Attention"
ATTENTION_CLEARED = "Cleared Attention"
ATTENTION_ENDED   = "Ended Attention"
ATTENTION_FILLED  = "Filled Attention"

ATTENTION_STARTED_ERROR = "Attempted function without setup ERROR"
ATTENTION_CLEARED_ERROR = "Attempted stop during data collection ERROR"

# State confirmation messages
__ATTENTION_READY = "Attention object is READY"
__ATTENTION_NOT_READY = "Attention object is NOT READY"
__ATTENTION_STOPPING = "Data collection STOPPED"
__ATTENTION_DATA_COLLECTED = "Data collection FINISHED"
__ATTENTION_DATA_FILLED = "Data collection sucessfully FILLED"

__ATTENTION_DATA_NONE = "No attention data GENERATED"
__ATTENTION_RESET_ERROR = "Attempted to clear during data collection ERROR"


def setup_emotions(log=False):
    """
        Updates the global attention_handler to a new EmotionalMath object with presets.
    """
    global attention_handler

    emotions = EmotionalMath(MATH_LIB_SETTING, 
                             ARTIFACT_DETECT_SETTING,
                             SHORT_ARTIFACT_DETECT_SETTING,
                             MENTAL_AND_SPECTRAL_SETTING)

    emotions.set_calibration_length(CALIBRATION_LENGTH)
    emotions.set_mental_estimation_mode(False)
    emotions.set_skip_wins_after_artifact(NWINS_SKIP_AFTER_ARTIFACT)
    emotions.set_zero_spect_waves(True, 0, 1, 1, 1, 0)
    emotions.set_spect_normalization_by_bands_width(True)

    logger.debug(__ATTENTION_READY) if log else None

    attention_handler = emotions


async def start_attention_capture_conc(log=False):
    """
        Starts the attention capture through an async process. 
        Will continue until the stop_attention_capture function is called.
    """
    global attention_data

    # async flag is FALSE if the loop is running
    while not end_capturing_conc:
        attention_data.append(RawChannels(3, 1))

    if log:
        logger.debug(__ATTENTION_DATA_COLLECTED)


def start_attention_capture(log=False):
    """
        Starts the attention capture process.
        Will continue until the stop_attention_capture function is called.
    """
    global attention_data, attention_capture

    # async flag is FALSE if the loop is running
    while attention_capture == True:
        attention_data.append(RawChannels(3, 1))

    logger.debug(__ATTENTION_DATA_COLLECTED) if log else None


def end_capturing_conc() -> bool:
    """
        Returns the state of the async flag.
        If True, then it has been SET and the capture loop should STOP.
    """
    global attention_capture_conc

    return attention_capture_conc.is_set()


def stop_attention_capture_conc(log=False):
    """ 
        Stops the data collection for the attention_data list by setting
        the async flag to TRUE.
    """
    global attention_capture

    # set the async flag to TRUE
    attention_capture.set()

    if log: 
        logger.debug(__ATTENTION_STOPPING)


def stop_attention_capture(log=False):
    """ 
        Stops the data collection for the attention_data list by setting
        the the flag to FALSE.
    """
    global attention_capture

    attention_capture = False

    logger.debug(__ATTENTION_STOPPING) if log else None


def reset_attention_data_conc(log=False) -> bool:
    """ 
        Concurrent Version 

        Reset the attention_data list to an empty list. All Data
        collected from the previous video will be lost. Will not work if
        data collection is occurring (attention_capture is set to True).

        :return:
            True if the list was reset.
    """
    global attention_handler, attention_data, attention_capture

    # can't reset if in the middle of capturing data
    if not end_capturing_conc():
        if log:
            logger.debug(__ATTENTION_RESET_ERROR)
        return False

    # reset all global vars
    attention_handler = None
    attention_data = []
    attention_capture.clear()

    return True


def reset_attention_data(log=False) -> bool:
    """ 
        Reset the attention_data list to an empty list. All Data
        collected from the previous video will be lost. Will not work if
        data collection is occurring (attention_capture is set to True).

        :return:
            True if the list was reset.
    """
    global attention_handler, attention_data, attention_capture

    # can't reset if in the middle of capturing data
    if attention_capture == True:
        logger.debug(__ATTENTION_RESET_ERROR) if log else None
        return False

    # reset all global vars
    attention_handler = None
    attention_data = []
    attention_capture = False

    return True
 

def is_emotion_object_ready():
    global attention_handler

    return attention_handler == None


def process_emotional_states(log=False) -> MindData | None:
    """
        :return:
            MindData object with percentage values of brain states.
    """
    global attention_handler, attention_data

    if attention_handler == None:
        logger.debug(ATTENTION_STARTED_ERROR) if log else None
        return None

    if len(attention_data) == 0:
        logger.debug(__ATTENTION_DATA_NONE) if log else None
        return None

    # may need to processes this in intermittent API calls for efficiency
    if attention_handler is isinstance(EmotionalMath):
        logger.debug("Pushing Data") if log else None
        attention_handler.push_data(attention_data)
        logger.debug("Processing Data") if log else None
        attention_handler.process_data_arr()

        if attention_handler.is_both_sides_artifacted():
            logger.debug("Both sides are artifacted")

        logger.debug(__ATTENTION_DATA_FILLED) if log else None

    return get_mind_data()


def get_mind_data(log=False) -> MindData:
    global attention_handler

    if attention_handler == None:
        logger.debug(__ATTENTION_NOT_READY) if log else None
        return None

    mind_data = attention_handler.read_average_mental_data(1)

    if log:
        logger.debug("Mind Data: {} {} {} {}".format(mind_data.rel_attention,
                                                     mind_data.rel_relaxation,
                                                     mind_data.inst_attention,
                                                     mind_data.inst_relaxation))

    return mind_data


def get_mind_data_list(log=False) -> list[MindData]:
    global attention_handler

    if attention_handler is None:
        return None

    mind_data_list = attention_handler.read_mental_data_arr()

    if log:
        for i in range(attention_handler.read_mental_data_arr_size()):
            print("{}: {} {} {} {}".format(i, mind_data_list[i].rel_attention,
                                              mind_data_list[i].rel_relaxation,
                                              mind_data_list[i].inst_attention,
                                              mind_data_list[i].inst_relaxation))

    return mind_data_list


def get_raw_spectral_values(log=False) -> RawSpectVals:
    global attention_handler

    if attention_handler is None:
        return None

    raw_spect_vals = attention_handler.read_raw_spectral_vals()

    if log:
        print("Raw Spect Vals: {} {}".format(raw_spect_vals.alpha, raw_spect_vals.beta))

    return raw_spect_vals


def get_raw_spectral_values_list(log=False) -> list[SpectralDataPercents]: 
    global attention_handler

    if attention_handler is None:
        return None

    percents = attention_handler.read_spectral_data_percents_arr()

    if log:
        for i in range(attention_handler.read_spectral_data_percents_arr_size()):
            print("{}: {} {} {} {} {}".format(i, percents[i].alpha,
                                                 percents[i].beta,
                                                 percents[i].gamma,
                                                 percents[i].delta,
                                                 percents[i].theta))

    return percents

