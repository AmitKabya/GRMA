import json
from collections import defaultdict
from grma.donorsgraph.build_donors_graph import BuildMatchingGraph
from grma.match import Graph, find_matches
import csv
import os
import shutil
from grim import grim


def load_patients_data(patients_file):
    """
        Load patient data from a file.

        Args:
            patients_file (str): Path to the patients data file.

        Returns:
            list: List of lines containing patient data.
        """
    with open(patients_file, 'r') as file:
        lines = file.readlines()
    return lines

def preprocess_patient_data(lines):
    """
        Preprocess patient data and group by patient ID.

        Args:
            lines (list): List of lines containing patient data.

        Returns:
            tuple: A tuple containing:
                - dict: Dictionary mapping patient IDs to their data.
                - dict: Dictionary mapping old patient IDs to new ones.
        """
    patient_data = defaultdict(list)
    new_patient_ids = {}
    patient_counter = 1

    for line in lines:
        parts = line.strip().split(',')
        old_patient_id = parts[0].split(':')[0]
        if old_patient_id not in new_patient_ids:
            new_patient_ids[old_patient_id] = patient_counter
            patient_counter += 1
        new_patient_id = new_patient_ids[old_patient_id]
        new_line = line.replace(old_patient_id, f'{new_patient_id:04d}')
        patient_data[new_patient_id].append(new_line)

    return patient_data, new_patient_ids

def create_patient_files(patient_data):
    """
        Create patient files from grouped patient data.

        Args:
            patient_data (dict): Dictionary mapping patient IDs to their data.
        """
    base_directory = './patients_dir_temp'
    os.makedirs(base_directory, exist_ok=True)

    for patient_id, data in patient_data.items():
        filename = f'patient_{patient_id}.txt'
        filepath = os.path.join(base_directory, filename)

        counter = 1
        while os.path.exists(filepath):
            filename = f'patient_{patient_id}_{counter}.txt'
            filepath = os.path.join(base_directory, filename)
            counter += 1

        with open(filepath, 'w') as file:
            file.writelines(data)


def process_and_save_results(patients_dir, donors_graph, dict_patients, cutof=100, threshold=0.1, result_dir='./result_dir'):
    """
        Process patient files for matching and save results.

        Args:
            patients_dir (str): Path to the directory containing patient files.
            donors_graph (Graph): Donors graph for matching.
            cutof (int, optional): Cutoff parameter for matching. Default is 100.
            threshold (float, optional): Threshold parameter for matching. Default is 0.1.
            result_dir (str, optional): Directory where result files will be saved. Default is './result_dir'.
        """
    if not os.path.exists(result_dir):
    	os.mkdir(result_dir)

    for filename in os.listdir(patients_dir):
        if filename.endswith(".txt"):
            patient_file_path = os.path.join(patients_dir, filename)

            matching_results = find_matches(patient_file_path, donors_graph, cutof=cutof, threshold=threshold)

            for patient, df in matching_results.items():
                original_id = dict_patients[patient]
                result_filename = os.path.join(result_dir, f"{original_id}.csv")
                df["Patient_ID"] = [original_id] * len(df["Patient_ID"])
                with open(result_filename, 'w', newline='') as result_file:
                    writer = csv.writer(result_file)
                    writer.writerow(df.columns)
                    writer.writerows(df.values)

def GetResultPatients(config_grim_file, path_donors_graph, dir_result, cutof=50, threshold=0.1, build_grim_graph=True):
    """
        Process patient data, perform matching, and save results.

        Args:
            config_grim_file (str): Path to the grim configuration.
            path_donors_graph (str): Path to the donors graph pickle file.
            dir_result (str): Directory where result files will be saved.
            cutof (int, optional): Cutoff parameter for matching. Default is 100.
            threshold (float, optional): Threshold parameter for matching. Default is 0.1.
        """
    donors_graph = Graph.from_pickle(path_donors_graph)
    with open(config_grim_file) as f:
        json_conf = json.load(f)
    output_dir = json_conf.get("imuptation_out_path", "output")
    patients_file =   output_dir + "/" + json_conf.get("imputation_out_umug_freq_filename")
    run_grim(config_grim_file,build_grim_graph)
    # add code that use imputation for patients file.
    # after_imputation_patients_file = imputation(patients_file) , and after that change the patients_file to after_imputation_patients_file
    lines = load_patients_data(patients_file)
    patient_data, new_patient_ids = preprocess_patient_data(lines)
    create_patient_files(patient_data)
    dict_patients = {v: k for k, v in new_patient_ids.items()}
    process_and_save_results('./patients_dir_temp', donors_graph,dict_patients, cutof=cutof, threshold=threshold, result_dir=dir_result)

    try:
        shutil.rmtree('./patients_dir_temp')
    except OSError as e:
        print(f"Error: {e}")

    try:
        shutil.rmtree('./output')
    except OSError as e:
        print(f"Error: {e}")

    print("****************************************************************************************************")
    print(f"Matching resault path: {dir_result} ")

def preprocess_donors_data(donors_file):
    """
       Preprocess donor data from a given file and organize it into separate files for each donor.

       Args:
       donors_file (str): The path to the input data file containing donor information.

       Returns:
       None
       """
    # Create a directory called "data" if it doesn't exist
    if not os.path.exists('data'):
        os.mkdir('data')
    # Define a dictionary to store data for each contributor
    donor_data = {}

    # Read the data from the file
    with open(donors_file, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            donor_id = parts[0]

            # Create a file for the contributor if it doesn't exist
            if donor_id not in donor_data:
                donor_data[donor_id] = []

            # Append the data to the contributor's list
            donor_data[donor_id].append(line)

    donors_directory = os.path.join('data', 'donors_dir')
    if not os.path.exists(donors_directory):
        os.mkdir(donors_directory)

    # Create a separate file for each contributor
    for donor_id, data_lines in donor_data.items():
        file_name = os.path.join(donors_directory, f'donor_{donor_id}.txt')
        with open(file_name, 'w') as output_file:
            output_file.writelines(data_lines)



def BuildDonorsGraph(directory_path, result_dir):
    """
        Build a donors graph and save it to a specified result directory.

        Args:
        donors_file (str): The path to the input data file containing donor information.
        result_dir (str): The directory where the result should be saved.

        Returns:
        None
    """

    # Build the matching graph
    build_matching = BuildMatchingGraph(directory_path)

    # Save the matching graph to the result directory
    if not os.path.exists(result_dir):
    	os.mkdir(result_dir)
    build_matching.to_pickle(os.path.join(result_dir, "donors_graph.pkl"))

    try:
        shutil.rmtree(directory_path)
    except OSError as e:
        print(f"Error: {e}")

def run_grim(grim_config_path, build_grim_graph=True):
    """
    Run three parts of GRIM (Graphical Representation of Immunogenetic Data for MHC): gram, grim, and post-gram.

    Args:
    grim_config_path (str): Path to the GRIM configuration file.
    build_grim_graph (bool): Flag indicating whether to build the frequencies graph for GRIM.
                            Set to True for the first run, and False for subsequent runs.

    Returns:
    None
    """

    if build_grim_graph:
        # Build the frequencies graph for GRIM
        grim.graph_freqs(conf_file=grim_config_path)

    # Run the imputation part of GRIM
    grim.impute(conf_file=grim_config_path)








