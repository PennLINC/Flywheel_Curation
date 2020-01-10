import os

# create a key


def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

# create the dictionary evaluate the heuristics


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where
    allowed template fields - follow python string module:
    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    # Create Keys
    t1w = create_key(
        'sub-{subject}/{session}/anat/sub-{subject}_{session}_T1w')

    # ASL - not doing this for now
    # pcasl = create_key('sub-{subject}/asl/sub-{subject}_pcasl')

    # Field maps
    # DistCorMap = create_key('sub-{subject}/fmap/sub-{subject}_phasediff')
    # b0_mag = create_key('sub-{subject}/fmap/sub-{subject}_magnitude')

    # fmri scans
    emotion_id = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_{session}_task-emotionid_bold')
    emotion_rec1 = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_{session}_task-emotionrec_bold')
#    emotion_rec2 = create_key(
#        'sub-{subject}/{session}/func/sub-{subject}_{session}_task-emotionrec_run-2_bold')

    # create the heuristic
    info = {t1w: [], emotion_id: [], emotion_rec1: []}

    def get_both_series(key1, key2, s):
        if len(info[key1]) == 0:
            info[key1].append(s.series_id)
        else:
            info[key2].append(s.series_id)

    for s in seqinfo:

        protocol = s.protocol_name.lower()
        series_description = s.series_description.lower()

        image_type = s.image_type
        # print("dico" in [x.lower() for x in image_type])

        if "mprage" in protocol and "mprage" in series_description:
            if "dico" not in [x.lower() for x in image_type]:
                info[t1w].append(s.series_id)

        elif "bbl1_az_id_210" in protocol and "dico" not in series_description:
            if "dico" not in [x.lower() for x in image_type]:
                info[emotion_id].append(s.series_id)

        elif "bbl1_az_rec_210" in protocol and "dico" not in series_description:
            if "dico" not in [x.lower() for x in image_type] and s.dim3 > 2:
                info[emotion_rec1].append(s.series_id)

    if(len(list(info.values())) != 3):
        print("############# ERROR!!! Files not complete!!! ##########")

    else:
        print("Session files complete")

    return info
