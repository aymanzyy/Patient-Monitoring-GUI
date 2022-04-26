import logging
import numpy as np
import matplotlib.pyplot as plt
import neurokit2 as nk
from scipy.signal import butter, lfilter
import json
np.set_printoptions(threshold=np.inf)


def import_data(in_file_path):
    """Reads in data from a given csv file

    csvfile contains ecg information including
    time and voltage. You will need to change the path of
    of the file you will be using in the ecg_driver().

    :param in_file_path: name of csv file in your folder

    :returns: one np.array containing all information in the file
    """

    in_file = open(in_file_path, "r")
    ecg_data = np.genfromtxt(in_file_path, delimiter=',')

    in_file.close()
    return ecg_data


def log_if_nan(ecg_data):
    """logs and error if there is an invalid entry

    If either value in a time, voltage pair is missing, contains a
    non-numeric string, or is NaN, the program should recognize
    that it is missing and log an error and deletes that row

    :param ecg_data: np.array of data from csv file

    :returns fixed_data: np.array of data without skipped entries
    """
    rows_to_delete = np.ones((len(ecg_data[:, 1])), dtype=bool)
    for count, item in enumerate(ecg_data):
        if np.isnan(item[0]) or np.isnan(item[1]):
            logging.error("Invalid input on line {}".format(count))
            rows_to_delete[count] = False
    fixed_data = delete_rows(ecg_data, rows_to_delete)
    return fixed_data


def log_if_voltage(ecg_data, filename):
    """logs and error if there is an invalid voltage

    If the file contains a voltage reading outside the normal range
    of +/- 300 mv, add a warning entry to the log file indicating
    the name of the test file and that voltages exceeded the normal
    range. This should only be done once per file (in other words,
    do not log every single voltage excursion). Analysis of the
    data should still be done as normal.

    :param ecg_data: np.array of data from csv file

    :returns: nothing
    """
    stop = False
    for count, item in enumerate(ecg_data):
        if abs(item[1]) > 300 and stop is False:
            logging.warning("A input voltage exceeds +/- 300mV in "
                            "file {}".format(filename))
            stop = True


def delete_rows(ecg_data, delete_mask):
    """Deletes rows with errors from the logging function

    This will delete any rows that are indicated by the boolean
    array mask passed in. A true value will keep the row and a
    false value will delete the row.

    :param ecg_data: np.array of data from csv file
    :param delete_mask: np.array bools mask of what to delete.

    :returns: all data after deleting the desired rows
    """
    return ecg_data[delete_mask]


def high_filter_ecg(ecg_data, sampling_freq):
    """Filters out signal noise below 1 Hz

    This function filters our noise below 1Hz for a cleaner
    ECG data.

    :param ecg_data: np.array of data from csv file
    :param sampling_freq: int of sampling frequency of ecg data

    :returns: np.array of filtered data
    """
    lowcut = 1
    nyq = 0.5 * sampling_freq
    low = lowcut / nyq
    order = 5
    analog = False
    btype = 'highpass'
    b, a = butter(order, low, btype, analog)
    filtered_data = lfilter(b, a, ecg_data)
    return filtered_data


def low_filter_ecg(ecg_data, sampling_freq):
    """Filters out signal noise above 50 Hz

    This function filters our noise above 50Hz for a cleaner
    ECG data.

    :param ecg_data: np.array of data from csv file
    :param sampling_freq: int of sampling frequency of ecg data

    :returns: np.array of filtered data
    """
    highcut = 50
    nyq = 0.5 * sampling_freq
    high = highcut / nyq
    order = 6
    analog = False
    btype = 'lowpass'
    b, a = butter(order, high, btype, analog)
    filtered_data = lfilter(b, a, ecg_data)
    return filtered_data


def find_peaks(ecg_data):
    """This function finds the peak from raw ECG data

    This function first calls our filters to clean the data. I then
    uses the ecg_peaks() function from neurokit2 to find the peaks.

    :param ecg_data: np.array of data from csv file

    :returns: an array of the peak index locations
    """
    sampling_freq = 1 / (ecg_data[1, 0] - ecg_data[0, 0])
    # print(sampling_freq)
    filtered_data = low_filter_ecg(ecg_data[:, 1], sampling_freq)
    filtered_data - high_filter_ecg(filtered_data, sampling_freq)
    clean_data = nk.ecg_clean(filtered_data,
                              sampling_rate=sampling_freq, method="biosppy")
    _, rpeaks = nk.ecg_peaks(clean_data, sampling_rate=sampling_freq)
    peak_array = rpeaks['ECG_R_Peaks']
    avg_peak = np.average(clean_data[peak_array])

    # force first peak to be counted
    between1and2 = (peak_array[1]-peak_array[0])/2
    check_threshold = round(peak_array[0] - between1and2)
    if check_threshold <= 0:
        # nk.events_plot(peak_array, clean_data)
        # plt.show()
        return peak_array
    if np.max(clean_data[:check_threshold]) > avg_peak/2:
        peak_array = np.insert(peak_array, 0,
                               np.argmax(clean_data[:check_threshold]))
    # nk.events_plot(peak_array, clean_data)
    # plt.show()
    return peak_array


def get_min_max(ecg_data):
    """Identifies the min and max of an array of voltages

    this function finds the min and max voltage of the whole data
    set before modification.

    :param ecg_data: np.array of voltage data from csv file

    :returns: tuple of the min_ecg and max_ecg
    """
    max_ecg = np.max(ecg_data)
    min_ecg = np.min(ecg_data)

    return min_ecg, max_ecg


def get_heartrate(time_data, peak_array):
    """Calculates the heartrate of input ecg data

    This function calculates the heartrate by dividing the
    number of peaks minus 1 by the time between the very first
    and last peaks

    :param time_data: np.array of time data from csv file
    :param peak_array: List of indexes where peaks occur

    :returns: float of the heartrate
    """
    number_of_peaks = len(peak_array)
    index_start = peak_array[0]
    index_end = peak_array[-1]
    time_elapsed = time_data[index_end] - time_data[index_start]
    heartrate = (number_of_peaks-1)*60/time_elapsed
    return heartrate


def get_beats(time_data, peak_array):
    """returns the times where beats occur in ecg data

    This function pulls which times the heartbeats occur
    in the original ECG data.

    :param time_data: np.array of time data from csv file
    :param peak_array: List of indexes where peaks occur

    :returns: list of beat times
    """
    beats = time_data[peak_array]
    return beats


def make_dictionary(duration, min, max, num_beats, heartrate, beats):
    """Takes all ecg information and puts it into a dictionary

    This function takes all of the information about an ecg
    and outputs a dictionary called metrics

    :param duration: last time data point in ecg_data
    :param min: minimum voltage value
    :param max: maximum voltage value
    :param num_beats: number of total beats
    :param heartrate: heartrate in bpm of ecg
    :param beats: minimum voltage value

    :returns: dictionary of ecg information
    """
    metrics = {"duration": duration,
               "voltage_extremes": (min, max),
               "num_beats": num_beats,
               "mean_hr_bpm": heartrate,
               "beats": list(beats)}
    return metrics


def make_filename(filename):
    """Takes input filename and makes the correct
    json file output name

    output file named "filename.json" where filename
    is replaced by the name of the input data set
    Example: testdata_1.json.

    :param filename: string with input filename ending in ".csv"

    :returns: string containing json filename
    """
    filename = filename.replace(".csv", ".json")
    return filename


def output_json(ecg_dict, filename):
    """Takes dictionaty with a scg information and puts it
    in an output json file.

    output file named "filename.json" where filename
    is replaced by the name of the input data set
    Example: testdata_1.json.

    :param ecg_dict: dictionary for a single ecg
    """
    out_file = open(filename, 'w')
    json.dump(ecg_dict, out_file)
    out_file.close()


def plot_trace(ecg_data, peaks, path):
    time = ecg_data[:, 0]
    voltage = ecg_data[:, 1]
    temp = path.split('/')[-1]
    final_file_name = temp.split('.')[0] + ".png"
    plt.plot(time, voltage)
    plt.plot(time[peaks], voltage[peaks], "o")
    plt.savefig('default_images/' + final_file_name,
                bbox_inches='tight', facecolor='red')
    plt.close()
    return 'default_images/' + final_file_name


def ecg_driver():
    logging.basicConfig(filename="ecg_log.log", filemode="w",
                        level=logging.INFO)
    logging.info("Starting analysis of new ECG Trace")

    path = "test_data\\"
    filename = "test_data2.csv"
    in_file_path = path + filename
    ecg_data = import_data(in_file_path)
    ecg_data = log_if_nan(ecg_data)
    log_if_voltage(ecg_data, filename)

    logging.info("Finding peak locations...")
    peak_array = find_peaks(ecg_data)
    logging.info("Finding min and max voltage...")
    min, max = get_min_max(ecg_data[:, 1])
    logging.info("Finding heartrate voltage...")
    heartrate = get_heartrate(ecg_data[:, 0], peak_array)
    logging.info("Finding beat time locations...")
    beats = get_beats(ecg_data[:, 0], peak_array)
    logging.info("Assigning Duration time...")
    logging.info("Assigning Number of Beats")
    logging.info("Loading dictionary...")
    metrics = make_dictionary(ecg_data[-1, 0], min, max,
                              len(peak_array), heartrate, beats)
    json_filename = make_filename(filename)
    output_json(metrics, json_filename)


if __name__ == "__main__":
    ecg_driver()
