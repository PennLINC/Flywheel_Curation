import os

# create a key
def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

# Create Keys

# T1 scans
t1w = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_T1w')

# ASL
pcasl = create_key('sub-{subject}/{session}/asl/sub-{subject}_{session}_asl')    
pcasl_moco = create_key('sub-{subject}/{session}/asl/sub-{subject}_{session}_asl_moco')   

# Field maps
b0_phase = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_phase{item}')
b0_mag = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_magnitude{item}')

# fmri scans
rest = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_bold')

face_01 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-face_run-01_bold')
face_02 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-face_run-02_bold')

card_01 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-card_run-01_bold')
card_02 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-card_run-02_bold')

# create the dictionary evaluate the heuristics
def infotodict(seqinfo):

    """Heuristic evaluator for determining which runs belong where
    allowed template fields - follow python string module:
    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    # create the heuristic
    info = {t1w: [], pcasl: [], pcasl_moco: [], face_01: [], face_02: [], card_01: [], card_02: [],
            b0_mag: [], b0_phase: [], rest: []
            }
    for s in seqinfo:
        protocol = s.protocol_name.lower()
        # t1
        if "mprage" in protocol:
            info[t1w].append(s.series_id)
        
        # asl
        elif ("MOCO" in s.image_type) and ("pcasl" in protocol):
            info[pcasl_moco].append(s.series_id)

        elif ("pcasl" in protocol):
            info[pcasl].append(s.series_id)

        # b0 maps
        elif ("b0map" in protocol) and ("P" in s.image_type):
            info [b0_phase].append(s.series_id)   
        elif ("b0map" in protocol) and ("M" in s.image_type):
            info[b0_mag].append(s.series_id)

        # tasks
        elif "facea0" in protocol:
            info[face_01].append(s.series_id)
        elif "faceb0" in protocol:
            info[face_02].append(s.series_id)
        elif "carda0" in protocol:
            info[card_01].append(s.series_id)
        elif "cardb0" in protocol:
            info[card_02].append(s.series_id)

        # resting-state
        elif "bold" in protocol:
            info[rest].append(s.series_id)
    return info

IntendedFor = {
    b0_mag: [
        '{session}/func/sub-{subject}_{session}_task-rest_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-face_run-01_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-face_run-02_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-card_run-01_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-card_run-02_bold.nii.gz'],

    b0_phase: [
        '{session}/func/sub-{subject}_{session}_task-rest_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-face_run-01_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-face_run-02_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-card_run-01_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-card_run-02_bold.nii.gz']
}

MetadataExtras = {
    rest: {
        "TaskName": 'rest'
    },

    card_01: {
        "TaskName": 'card'
    },

    card_02: {
        "TaskName": 'card'
    },

    face_01: {
        "TaskName": 'face'
    },

    face_02: {
        "TaskName": 'face'
    },

    pcasl: {
        'ASLContext': 'Label_Control', 
        'LabelingType': 'PCASL'
    }    
}