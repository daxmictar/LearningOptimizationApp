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
attention_data: List[RawChannels] = []

# trying this with async
# Goal: set a flag that maintains the attention data collection loop
# it will stop when the post to 'end_attention' is called.
attention_capture = asyncio.Event()

# API Return Messages

ATTENTION_CREATED = "Created Attention"
ATTENTION_STARTED = "Started Attention"
ATTENTION_CLEARED = "Cleared Attention"
ATTENTION_ENDED   = "Ended Attention"
ATTENTION_FILLED  = "Filled Attention"

ATTENTION_STARTED_ERROR = "Started Attention Error"

# State confirmation messages
__ATTENTION_READY = "Attention object is READY"
__ATTENTION_NOT_READY = "Attention object is NOT READY"
__ATTENTION_STOPPING = "Async loop for data collection STOPPED"
__ATTENTION_DATA_COLLECTED = "Async loop for data collection FINISHED"
__ATTENTION_RESET_ERROR = "Async loop stopped during data collection ERROR"


async def start_attention_capture(log=False):
    """
        Starts the attention capture through an async process. 
        Will continue until the stop_attention_capture function is called.
    """
    global attention_data

    # async flag is FALSE if the loop is running
    while not end_capturing:
        attention_data.append(RawChannels(3, 1))

    if log:
        logger.log(__ATTENTION_DATA_COLLECTED)


def end_capturing() -> bool:
    """
        Returns the state of the async flag.
        If True, then it has been SET and the capture loop should STOP.
    """
    global attention_capture

    return attention_capture.is_set()


def stop_attention_capture(log=False):
    """ 
        Stops the data collection for the attention_data list by setting
        the async flag to TRUE.
    """
    global attention_capture

    # set the async flag to TRUE
    attention_capture.set()

    if log: 
        logger.log(__ATTENTION_STOPPING)


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
    if not end_capturing():
        if log:
            log.logger(__ATTENTION_RESET_ERROR)
        return False

    # reset all global vars
    attention_handler = None
    attention_data = []
    attention_capture.clear()

    return True


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

    attention_handler = emotions
    

def is_emotion_object_ready():
    global attention_handler

    return attention_handler == None


def process_emotional_states() -> MindData:
    """
        :return:
            MindData object with percentage values of brain states.
    """
    global attention_handler, attention_data

    if len(attention_data) == 0:
        logger.debug("No data present to parse emotional states")
        return

    # may need to processes this in intermittent API calls for efficiency
    if attention_handler != None and isinstance(EmotionalMath):
        attention_handler.push_data(raw_data)
        attention_handler.process_data_arr()

        if attention_handler.is_both_sides_artifacted():
            logger.debug("Both sides are artifacted")

    return get_mind_data()


def get_mind_data(log=False) -> MindData:
    global attention_handler

    mind_data = attention_handler.read_average_mental_data(1)
    if log:
        logger.debug("Mind Data: {} {} {} {}".format(mind_data.rel_attention,
                                                     mind_data.rel_relaxation,
                                                     mind_data.inst_attention,
                                                     mind_data.inst_relaxation))

    return mind_data


def get_mind_data_list(log=False) -> List[MindData]:
    global attention_handler

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

    raw_spect_vals = emotions.read_raw_spectral_vals()
    if log:
        print("Raw Spect Vals: {} {}".format(raw_spect_vals.alpha, raw_spect_vals.beta))

    return raw_spect_vals


def get_raw_spectral_values_list(log=False) -> List[SpectralDataPercents]: 
    global attention_handler

    percents = attention_handler.read_spectral_data_percents_arr()

    if log:
        for i in range(attention_handler.read_spectral_data_percents_arr_size()):
            print("{}: {} {} {} {} {}".format(i, percents[i].alpha,
                                                 percents[i].beta,
                                                 percents[i].gamma,
                                                 percents[i].delta,
                                                 percents[i].theta))

    return percents

