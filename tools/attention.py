import math

from dataclasses import dataclass

from em_st_artifacts.utils.support_classes import RawChannelsArray, RawChannels, MindData, RawSpectVals, SpectralDataPercents

from em_st_artifacts.emotional_math import EmotionalMath

from em_st_artifacts.utils.lib_settings import MathLibSetting, ArtifactDetectSetting, ShortArtifactDetectSetting, \
    MentalAndSpectralSetting

from tools.logging import logger


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

@dataclass
class BrainDataInfo:
    brain_data: List[MindData]



def setup_emotions() -> EmotionalMath:
    emotions = EmotionalMath(MATH_LIB_SETTING, 
                             ARTIFACT_DETECT_SETTING,
                             SHORT_ARTIFACT_DETECT_SETTING,
                             MENTAL_AND_SPECTRAL_SETTING)

    emotions.set_calibration_length(CALIBRATION_LENGTH)
    emotions.set_mental_estimation_mode(False)
    emotions.set_skip_wins_after_artifact(NWINS_SKIP_AFTER_ARTIFACT)
    emotions.set_zero_spect_waves(True, 0, 1, 1, 1, 0)
    emotions.set_spect_normalization_by_bands_width(True)

    return emotions


def process_emotional_states(emotions: EmotionalMath, raw_data: List[RawChannels]) -> (float, float, float, float):
    """
        Takes an EmotionalMath object and reads the emotional states from the data being processed by it.

        :params:
            emotions: EmotionalMath - The emotion object to be read from

        :return:
            A tuple with values related to the brain data
            0 - Relative Attention Value
            1 - Relative Relaxation Value 
            2 - Instatiate Attention Value
            3 - Instantiate Relaxation Value 
    """
    if len(raw_data) == 0:
        logger.debug("No data present to parse emotional states")
        return

    # may need to processes this in intermittent API calls for efficiency
    emotions.push_data(raw_data)
    emotions.process_data_arr()

    if emotions.is_both_sides_artifacted():
        logger.debug("Both sides are artifacted")

    return emotions

    # this section should just retrieve and output the processed data
 


def get_mind_data(emotions: EmotionalMath, print_data=False) -> MindData:
    mind_data = emotions.read_average_mental_data(1)
    if print_data:
        logger.debug("Mind Data: {} {} {} {}".format(mind_data.rel_attention,
                                                     mind_data.rel_relaxation,
                                                     mind_data.inst_attention,
                                                     mind_data.inst_relaxation))

    return mind_data

def get_mind_data_list(emotions: EmotionalMath, print_data=False) -> List[MindData]:
    mind_data_list = emotions.read_mental_data_arr()
    if print_data:
        for i in range(emotions.read_mental_data_arr_size()):
            print("{}: {} {} {} {}".format(i,
                                            mind_data_list[i].rel_attention,
                                            mind_data_list[i].rel_relaxation,
                                            mind_data_list[i].inst_attention,
                                            mind_data_list[i].inst_relaxation))

    return mind_data_list

def get_raw_spectral_values(emotions: EmotionalMath, print_data=False) -> RawSpectVals:
    raw_spect_vals = emotions.read_raw_spectral_vals()

    if print_data:
        print("Raw Spect Vals: {} {}".format(raw_spect_vals.alpha, raw_spect_vals.beta))

    return raw_spect_vals


def get_raw_spectral_values_list(emotions: EmotionalMath, print_data=False) -> List[SpectralDataPercents]: 
    percents = emotions.read_spectral_data_percents_arr()

    if print_data:
        for i in range(emotions.read_spectral_data_percents_arr_size()):
            print("{}: {} {} {} {} {}".format(i,percents[i].alpha,
                                                percents[i].beta,
                                                percents[i].gamma,
                                                percents[i].delta,
                                                percents[i].theta))

