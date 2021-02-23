### This heuristic organizes SYRP (818621) data on Flywheel
###
### Ellyn Butler
### September 6, 2019 - September 10, 2019
###
### Joelle Jee
### December 14, 2020 -Jan 8, 2021

import os

# create a key
def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

def ReplaceSubject(subj_label):
    return subj_label.lstrip('0')

sub_sess_dir = "sub-{subject}/{session}/"
sub_sess_name = "sub-{subject}_{session}_"

# structural
t1w = create_key(sub_sess_dir + "anat/" + sub_sess_name + "T1w")
t1w_moco = create_key(sub_sess_dir + "anat/" + sub_sess_name + "acq-moco_T1w")
# t1w_moco = create_key(sub_sess_dir + "anat/" + sub_sess_name + "acq-moco_T1w")
t2w = create_key(sub_sess_dir + "anat/" + sub_sess_name + "T2w")

# fmri
rest_bold_742 = create_key(sub_sess_dir + "func/" + sub_sess_name + "task-rest_acq-742_bold")

# fmaps
fmap_ph = create_key(sub_sess_dir + "fmap/" + sub_sess_name + "phasediff")
fmap_mag = create_key(sub_sess_dir + "fmap/" + sub_sess_name + "magnitude{item}")
fmap_topup = create_key(sub_sess_dir + "fmap/" + sub_sess_name + "acq-mstopup_dir-PA_epi")

# dwi
dwi_117 = create_key(sub_sess_dir + "dwi/" + sub_sess_name + "acq-ms117dir_dir-AP_dwi")
dwi_127 = create_key(sub_sess_dir + "dwi/" + sub_sess_name + "acq-ms127dir_dir-AP_dwi")

# qsm 1.5mm
qsm_15mm = create_key(sub_sess_dir + "anat/" + sub_sess_name + "acq-15mmqsme{item}_T2star")
qsm_15mm_ph = create_key(sub_sess_dir + "anat/" + sub_sess_name + "acq-15mmqsmph{item}_T2star")

# qsm 1mm
qsm_1mm = create_key(sub_sess_dir + "anat/" + sub_sess_name + "acq-1mmqsme{item}_T2star")
qsm_1mm_ph = create_key(sub_sess_dir + "anat/" + sub_sess_name + "acq-1mmqsmph{item}_T2star")


def infotodict(seqinfo):
    # create the heuristic
    info = {# structural
            t1w: [], t1w_moco: [], t2w: [],

            # fmri
            rest_bold_742: [],

            # fmaps
            fmap_ph: [], fmap_mag: [], fmap_topup: [],

            #dwi
            dwi_117: [], dwi_127: [],

            # qsm 1.5mm
            qsm_15mm: [], qsm_15mm_ph: [],

            # qsm 1mm
            qsm_1mm: [], qsm_1mm_ph: []

            }

    for s in seqinfo:
        protocol = s.protocol_name.lower()

        # t1
        if "mprage" in protocol and 'nav' not in protocol and 'moco' in protocol and "DERIVED" not in s.image_type:
            if s.TR == 1.85 and s.dim1 == 256 :
                info[t1w_moco].append(s.series_id)
            # disregard T1 images with very small TR value
            else:
                continue
        elif "mpr" in protocol and "nav" not in protocol:
            info[t1w].append(s.series_id)

        # t2
        elif "t2" in protocol and ("spc" in protocol or "space" in protocol):
            # filter out "T2_SAG_FLAIR_SPACE_turbo2_p2"
            if "flair" in protocol:
                continue
            info[t2w].append(s.series_id)

        # fmri
        elif "restbold" in protocol and "742" in protocol:
            info[rest_bold_742].append(s.series_id)

        # fmaps
        elif "topup" in protocol:
            info[fmap_topup].append(s.series_id)

        elif "b0map" in protocol:
            if "P" in s.image_type:
                info[fmap_ph].append(s.series_id)
            else:
                info[fmap_mag].append(s.series_id)

        # dwi
        elif "multishell" in protocol:
            if s.dim3 == 116:
                info[dwi_117].append(s.series_id)
            elif s.dim3 == 126:
                info[dwi_127].append(s.series_id)

        # qsm
        elif "t2star_qsm" in protocol:
            # first filter out the subject that has qsm data with dim3=399
            if s.dim3 == 399:
                continue
            # determine the run no.
            if "P" in s.image_type and "1mm" in protocol:
            	info[qsm_1mm_ph].append(s.series_id)
            elif "1mm" in protocol:
                info[qsm_1mm].append(s.series_id)
            elif "P" in s.image_type and "1.5" in protocol:
                info[qsm_15mm_ph].append(s.series_id)
            elif "1.5" in protocol:
                info[qsm_15mm].append(s.series_id)


    return info


MetadataExtras = {
    fmap_ph: {
        "EchoTime1": 0.00313,
        "EchoTime2": 0.00559
    }
}

IntendedFor = {
    fmap_ph: [
        "{session}/func/" + sub_sess_name + "task-rest_acq-742_bold.nii.gz",
        "{session}/anat/" + sub_sess_name + "acq-moco_T1w.nii.gz",
        "{session}/anat/" + sub_sess_name + "T1w.nii.gz",
        "{session}/anat/" + sub_sess_name + "T2w.nii.gz",
        "{session}/dwi/" + sub_sess_name + "acq-ms117dir_dir-AP_dwi.nii.gz"
    ],

    fmap_mag: [
        "{session}/func/" + sub_sess_name + "task-rest_acq-742_bold.nii.gz",
        "{session}/anat/" + sub_sess_name + "acq-moco_T1w.nii.gz",
        "{session}/anat/" + sub_sess_name + "T1w.nii.gz",
        "{session}/anat/" + sub_sess_name + "T2w.nii.gz",
        "{session}/dwi/" + sub_sess_name + "acq-ms117dir_dir-AP_dwi.nii.gz"
    ],

    fmap_topup: [
        "{session}/dwi/" + sub_sess_name + "acq-ms127dir_dir-AP_dwi.nii.gz"
    ]

}
