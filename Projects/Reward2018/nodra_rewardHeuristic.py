import os

# create a key
def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

# Create Keys

# T1 scans
t1w = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_T1w')
t1w_nav = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-nav_T1w')
t1w_sag = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-sag_T1w')

# Field maps
b0_phase = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_phasediff')
b0_mag = create_key('sub-{subject}/{session}/fmap/sub-{subject}_{session}_magnitude{item}')

# fmri scans
rest_sb = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-singleband_bold')
rest_mb = create_key(
    'sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_acq-multiband_bold')

card_01 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-card_run-01_bold')
card_02 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-card_run-02_bold')

itc_01 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-itc_run-01_bold')
itc_02 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-itc_run-02_bold')

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
    info = {t1w: [], t1w_nav: [], t1w_sag: [], card_01: [], card_02: [], itc_01: [], itc_02: [], 
            b0_mag: [], b0_phase: [], rest_sb: [], rest_mb: []
            }
    for s in seqinfo:
        protocol = s.protocol_name.lower()
        seriesDescription = s.series_description.lower()
        # t1
        if ("mprage" in protocol): 
            if ("MPRAGE_TI1110_ipat2_moco3" in s.series_description):
                info[t1w].append(s.series_id)
            elif ("MPRAGE_NAVprotocol" in s.series_description):
                info[t1w_nav].append(s.series_id)
            elif ("sag_mpr" in seriesDescription) or ("mpr_sag" in seriesDescription) or ("sag" in seriesDescription) or ("mpr_collection" in seriesDescription):
                info[t1w_sag].append(s.series_id)

        # b0 maps
        elif ("b0map" in protocol) and ("P" in s.image_type):
            info [b0_phase].append(s.series_id)   
        elif ("b0map" in protocol) and ("M" in s.image_type):
            info[b0_mag].append(s.series_id)
        # tasks
        elif "carda0" in protocol:
            info[card_01].append(s.series_id)
        elif "cardb0" in protocol:
            info[card_02].append(s.series_id)
        elif "itc1" in protocol:
            info[itc_01].append(s.series_id)
        elif "itc2" in protocol:
            info[itc_02].append(s.series_id)

        # resting-state
        elif ("bold" in protocol) and (("MB" in s.image_type) or ("mb" in s.series_description)):
            info[rest_mb].append(s.series_id)
        elif "bold" in protocol:
            info[rest_sb].append(s.series_id)
    return info

IntendedFor = {
    b0_mag: [
        '{session}/func/sub-{subject}_{session}_task-rest_acq-singleband_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-rest_acq-multiband_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-card_run-01_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-card_run-02_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-itc_run-01_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-itc_run-02_bold.nii.gz'],

    b0_phase: [
        '{session}/func/sub-{subject}_{session}_task-rest_acq-singleband_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-rest_acq-multiband_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-card_run-01_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-card_run-02_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-itc_run-01_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-itc_run-02_bold.nii.gz']
}

MetadataExtras = {
    b0_phase: {
        "EchoTime1": 0.00406,
        "EchoTime2": 0.00652
    },

    itc_01: {
        "TaskName": 'itc'
    },

    itc_02: {
        "TaskName": 'itc'
    },

    card_01: {
        "TaskName": 'card'
    },

    card_02: {
        "TaskName": 'card'
    },

    rest_sb: {
        "TaskName": 'rest'
    },

    rest_mb: {
        "TaskName": 'rest'
    }    
}
