'''
Heuristic to curate the 22Q_812481 project.
Katja Zoner
Updated: 04/16/2021
'''

import os

##################### Create keys for each acquisition type ####################

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

# Structural scans
t1w = create_key(
    'sub-{subject}/{session}/anat/sub-{subject}_{session}_T1w')

# fMRI scans
rest_bold_124 = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-singleband_bold')
demo = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-idemo_bold')
#jolo = create_key(
#    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-jolo_bold')

# Diffusion weighted scans
dwi_run1 = create_key(
    'sub-{subject}/{session}/dwi/sub-{subject}_{session}_run-01_dwi')
dwi_run2 = create_key(
    'sub-{subject}/{session}/dwi/sub-{subject}_{session}_run-02_dwi')

# Field maps
b0_mag = create_key(
    'sub-{subject}/{session}/fmap/sub-{subject}_{session}_magnitude{item}')
b0_phase = create_key(
    'sub-{subject}/{session}/fmap/sub-{subject}_{session}_phase{item}')
b0_phasediff = create_key(
    'sub-{subject}/{session}/fmap/sub-{subject}_{session}_phasediff')

# ASL scans
asl = create_key(
    'sub-{subject}/{session}/perf/sub-{subject}_{session}_acq-se_asl')

############################ Define heuristic rules ############################

def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where
    allowed template fields - follow python string module:
    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    #last_run = len(seqinfo)

    # Info dictionary to map series_id's to correct create_key key
    info = {t1w: [],
            rest_bold_124: [],  demo: [], #jolo: [],
            dwi_run1: [], dwi_run2: [],
            b0_mag: [], b0_phase: [], b0_phasediff: [],
            asl: []
            }

    def get_latest_series(key, s):
        info[key].append(s.series_id)

    for s in seqinfo:
        protocol = s.protocol_name.lower()

        # Structural scans
        if "mprage" in protocol and "nav" not in protocol and "MOSAIC" not in s.image_type:
            get_latest_series(t1w, s)

        # fmRI scans
        elif "idemo" in protocol:
            get_latest_series(demo, s)
        elif "restbold" in protocol:
            get_latest_series(rest_bold_124, s)
        #elif "jolo" in protocol:
        #    get_latest_series(jolo, s)

        ## TODO: Is this correct?
        # Fieldmap scans
        elif "b0map" in protocol and "M" in s.image_type:
            get_latest_series(b0_mag, s)
        elif "b0map" in protocol and "P" in s.image_type:
            if "v3" in protocol:
                info[b0_phase].append(s.series_id)
                get_latest_series(b0_phase, s)

            else:
                info[b0_phasediff].append(s.series_id)
                get_latest_series(b0_phasediff, s)

        # dwi
        elif "dti" in protocol and not s.is_derived:
            if "35" in protocol:
                get_latest_series(dwi_run1, s)
            elif "36" in protocol:
                get_latest_series(dwi_run2, s)

        # ASL scans
        elif "pcasl" in protocol and "MOCO" not in s.image_type:
            get_latest_series(asl, s)

        else:
            print("Series not recognized!: ", s.protocol_name, s.dcm_dir_name)

    return info

################## Hardcode required params in MetadataExtras ##################
MetadataExtras = {    
    b0_phasediff: {
        "EchoTime1": 0.00471,
        "EchoTime2": 0.00717
    },
    # ASL params hardcoded from PNC_CS ASL metadata
    asl: {
        #"AcquisitionDuration": 123,
        "ArterialSpinLabelingType": "PCASL", # required
        #"AverageB1LabelingPulses": 0,
        #"AverageLabelingGradient": 34,
        "BackgroundSuppression": False, # required
        "InterPulseSpacing": 4,
        "LabelingDistance": 2,
        "LabelingDuration": 1.2, # required 
        "LabelingEfficiency": 0.72,
        "LabelingSlabLocation": "X", # correct
        "LabelingType": "PCASL", #?? unsure
        #"LookLocker": True,
        "M0Type": "Absent", # required 
        "PCASLType": "balanced",
        "PostLabelingDelay": 1.517, # required
        #"PulseDuration": 1.5088,
        #"PulseSequenceDetails": "WIP",
        "PulseSequenceType": "2D",
        "RepetitionTimePreparation": 0, # required
        "SliceSelectiveLabelingGradient": 45 #not that important,  but correct
        #"VascularCrushingVenc": 2
    }
}

## TODO: Is this correct?
IntendedFor = {
    b0_phase: [
        '{session}/func/sub-{subject}_{session}_task-rest_acq-singleband_bold.nii.gz',
        #'{session}/func/sub-{subject}_{session}_task-jolo_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-idemo_bold.nii.gz',
        '{session}/dwi/sub-{subject}_{session}_run-01_dwi.nii.gz',
        '{session}/dwi/sub-{subject}_{session}_run-02_dwi.nii.gz',
        '{session}/perf/sub-{subject}_{session}_acq-se_asl.nii.gz'
    ],
    b0_phasediff: [
        '{session}/func/sub-{subject}_{session}_task-rest_acq-singleband_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-idemo_bold.nii.gz',
        '{session}/dwi/sub-{subject}_{session}_run-01_dwi.nii.gz',
        '{session}/dwi/sub-{subject}_{session}_run-02_dwi.nii.gz',
        '{session}/perf/sub-{subject}_{session}_acq-se_asl.nii.gz'
    ],
    b0_mag: [
        '{session}/func/sub-{subject}_{session}_task-rest_acq-singleband_bold.nii.gz',
        #'{session}/func/sub-{subject}_{session}_task-jolo_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-idemo_bold.nii.gz',
        '{session}/dwi/sub-{subject}_{session}_run-01_dwi.nii.gz',
        '{session}/dwi/sub-{subject}_{session}_run-02_dwi.nii.gz'
        '{session}/perf/sub-{subject}_{session}_acq-se_asl.nii.gz'
    ]
}

def AttachToSession():
    NUM_VOLUMES=40
    data = ['control', 'label'] * NUM_VOLUMES
    data = '\n'.join(data)
    data = 'volume_type\n' + data # the data is now a string; perfect!

    # define asl_context.tsv file
    asl_context = {
        'name': 'sub-{subject}/{session}/perf/sub-{subject}_{session}_acq-se_aslcontext.tsv',
        'data': data,
        'type': 'text/tab-separated-values'
    }

    import pandas as pd 

    df = pd.read_csv("info/task-idemo_events.tsv", sep='\t') 

    # define idemo events.tsv file
    idemo_events = {
        'name': 'sub-{subject}/{session}/func/sub-{subject}_{session}_task-idemo_events.tsv',
        'data': df.to_csv(index=False, sep='\t'),
        'type': 'text/tab-separated-values'
    }

    '''
    # define jolo events.tsv file
    jolo_events = {
        'name': 'sub-{subject}/{session}/func/sub-{subject}_{session}_task-jolo_events.tsv',
        'data': df.to_csv(index=False, sep='\t'),
        'type': 'text/tab-separated-values'
    }
    '''
    return [asl_context, idemo_events]

####################### Rename session and subject labels #######################

# Use flywheel to gather a dictionary of all session session_labels
# with their corresponding index by time, within the subject
def gather_session_indices():

    import flywheel
    fw = flywheel.Client()

    proj = fw.projects.find_first('label="{}"'.format("22Q_812481"))
    subjects = proj.subjects()

    # Initialize session dict
    # Key: existing session label
    # Value: new session label in form <proj_name><session idx>
    session_labels = {}

    for s in range(len(subjects)):

        # Get a list of the subject's sessions
        sessions = subjects[s].sessions()

        if sessions:
            # Sort session list by timestamp
            sessions = sorted(sessions, key=lambda x: x.timestamp)
            # loop through the subject's sessions, assign each session an index
            for i, sess in enumerate(sessions):
                session_labels[sess.label] = "22Q" + str(i + 1)

    return session_labels

session_labels = gather_session_indices()

# Replace session label with <proj_name><session_idx>
def ReplaceSession(ses_label):
    return str(session_labels[ses_label])

def ReplaceSubject(label):
    return label.lstrip("0")
