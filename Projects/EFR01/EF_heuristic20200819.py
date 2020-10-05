import os


def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


# create key
t1w = create_key(
    'sub-{subject}/ses-{session}/anat/sub-{subject}_ses-{session}_T1w')
t2w = create_key(
    'sub-{subject}/ses-{session}/anat/sub-{subject}_ses-{session}_T2w')
fracback=create_key(
   'sub-{subject}/{session}/func/sub-{subject}_{session}_task-fracback_acq-singleband_bold')
asl=create_key(
   'sub-{subject}/{session}/perf/sub-{subject}_{session}_asl')
m0=create_key(
   'sub-{subject}/{session}/perf/sub-{subject}_{session}_m0')
mean_perf=create_key(
   'sub-{subject}/{session}/perf/sub-{subject}_{session}_mean-perfusion')
#qsm_mag_1= create_key(
    #'sub-{subject}/ses-{session}/swi/sub-{subject}_ses-{session}_part-mag_echo-1_rec-norm_GRE')
#qsm_mag_2= create_key(
    #'sub-{subject}/ses-{session}/swi/sub-{subject}_ses-{session}_part-mag_echo-2_rec-norm_GRE')
#qsm_mag_3= create_key(
    #'sub-{subject}/ses-{session}/swi/sub-{subject}_ses-{session}_part-mag_echo-3_rec-norm_GRE')
#qsm_mag_4= create_key(
    #'sub-{subject}/ses-{session}/swi/sub-{subject}_ses-{session}_part-mag_echo-4_rec-norm_GRE')
#qsm_phase_1= create_key(
    #'sub-{subject}/ses-{session}/swi/sub-{subject}_ses-{session}_part-phase_echo-1_GRE')
#qsm_phase_2= create_key(
    #'sub-{subject}/ses-{session}/swi/sub-{subject}_ses-{session}_part-phase_echo-2_GRE')
#qsm_phase_3= create_key(
    #'sub-{subject}/ses-{session}/swi/sub-{subject}_ses-{session}_part-phase_echo-3_GRE')
#qsm_phase_4= create_key(
    #'sub-{subject}/ses-{session}/swi/sub-{subject}_ses-{session}_part-phase_echo-4_GRE')
fmap_pa_diff = create_key(
    'sub-{subject}/ses-{session}/fmap/sub-{subject}_ses-{session}_acq-dMRIdistmap_dir-PA_epi')
fmap_ap_diff = create_key(
    'sub-{subject}/ses-{session}/fmap/sub-{subject}_ses-{session}_acq-dMRIdistmap_dir-AP_epi')
fmap_pa_bold = create_key(
    'sub-{subject}/ses-{session}/fmap/sub-{subject}_ses-{session}_acq-fMRIdistmap_dir-PA_epi')
fmap_ap_bold = create_key(
    'sub-{subject}/ses-{session}/fmap/sub-{subject}_ses-{session}_acq-fMRIdistmap_dir-AP_epi')
dwi = create_key(
   'sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-multiband_dwi')

#Resting state bold scans acquired before March 22, 2019 have 2 nifti acquisitions that stem from 1 dicom, and are noted here as "old runs"
#Bold scnas acquired after March 22, 2019 have two dicoms and 2 nifits, representing 2 Bold runs
# the runs with multiple niftis in 1 acquisition

ABCD_rest = create_key('sub-{subject}/ses-{session}/func/sub-{subject}_ses-{session}_task-restbold_run-{item}_bold')
# the new runs that have to be curated in separate acquisitions
func_rest_run_1 = create_key('sub-{subject}/ses-{session}/func/sub-{subject}_ses-{session}_task-restbold_run-1_bold')
func_rest_run_2 = create_key('sub-{subject}/ses-{session}/func/sub-{subject}_ses-{session}_task-restbold_run-2_bold')

#Sequences we don't want to BIDS-ifiy
'''
anat-scout
localizer_32ch
ABCD_T1w_MPR_vNav_setter
anat_acq-vnavsetter_T2w
anat_acq-vnavsetter_T1w
ABCD_T2w_SPC_vNav_setter
anat_acq-vnavsetter-BodyCoil_T1w
'''

#T1 sequences acquired before March 22, 2019 are named 'ABCD_T1w_MPR_vNav' and those after  are  named 'anat_T1w'
#T2 sequences acquired before March 22, 2019 are named 'ABCD_T2W_SPC_vNav' and those after  are  named 'anat_T2w'
#DTI sequences acquierd before March 22, 2019 are named 'ABCD_dMRI' and those after are named 'dwi_acq-multishell'
#Fmap sequences acquired before March 22, 2019 are named 'ABCD_fMRI_DistortionMap_PA' and those after are named 'fmap_acq-dMRIdistmap_dir-PA_epi' (or AP)

def infotodict(seqinfo):

    last_run=len(seqinfo)

    info = {t1w: [], t2w: [], ABCD_rest: [], func_rest_run_1: [], func_rest_run_2: [], fracback: [],
             dwi: [], asl: [], m0: [], mean_perf: [], #qsm_mag_1: [], qsm_mag_2: [], qsm_mag_3: [],
            #qsm_mag_4: [], qsm_phase_1: [], qsm_phase_2: [], qsm_phase_3: [], qsm_phase_4: [],
            fmap_pa_diff: [], fmap_ap_diff: [], fmap_ap_bold: [], fmap_pa_bold:[]}

    def append_series(key, s):
        #    if len(info[key]) == 0:
        info[key].append(s.series_id)
    #    else:
    #        info[key] = [s.series_id]
    for s in seqinfo:
        protocol=s.protocol_name.lower()
        series_description=s.series_description.lower()
    #anat scans
        if "anat_t1w" in protocol and "vnav" not in series_description:
            append_series(t1w, s)
        elif "abcd_t1w_mpr_vnav" in protocol and "setter" not in series_description:
            append_series(t1w, s)
        elif "anat_t2w" in protocol and "vnav" not in series_description and "NORM" in  s.image_type:
            append_series(t2w, s)
        elif "abcd_t2w_spc_vnav" in protocol and "setter" not in series_description:
            append_series(t2w, s)
    #func scans
        elif "fracnoback" in protocol:
            append_series(fracback, s)
        elif "frac-no-back" in protocol:
            append_series(fracback, s)
        elif "rest" in protocol:
        #rest_run for rerpoin
            if "abcd_fmri" in protocol:
                info[ABCD_rest].append(s.series_id)
        # it wasn't reproin so it goes into the other rest runs; we use the run number to pick which one
            elif "01" in protocol:
                info[func_rest_run_1].append(s.series_id)
            else:
                info[func_rest_run_2].append(s.series_id)
    #perf scans
        elif s.series_description.endswith("_ASL"):
            append_series(asl, s)
        elif s.series_description.endswith("_M0"):
            append_series(m0, s)
        elif s.series_description.endswith("_MeanPerf"):
            append_series(mean_perf, s)
    #swi scans
        #elif "qsm" in protocol and not s.is_derived and "NORM" in s.image_type:
            #if s.dcm_dir_name.endswith('e1.nii.gz'):
                #append_series(qsm_mag_1, s)
            #elif s.dcm_dir_name.endswith('e2.nii.gz'):
                #append_series(qsm_mag_2, s)
            #elif s.dcm_dir_name.endswith('e3.nii.gz'):
                #append_series(qsm_mag_3, s)
            #else:
                #append_series(qsm_mag_4, s)
        #elif "qsm" in protocol and not s.is_derived  and "NORM" not in s.image_type:
            #if s.dcm_dir_name.endswith('e1_ph.nii.gz'):
                #append_series(qsm_phase_1, s)
            #elif s.dcm_dir_name.endswith('e2_ph.nii.gz'):
                #append_series(qsm_phase_2, s)
            #elif s.dcm_dir_name.endswith('e3_ph.nii.gz'):
                #append_series(qsm_phase_3, s)
            #else:
                #append_series(qsm_phase_4, s)
    #fmap scans (pre and post name change)
        elif "distortionmap_pa" in protocol and "DIFFUSION" in s.image_type:
            append_series(fmap_pa_diff, s)
        elif "distortionmap_ap" in protocol and "DIFFUSION" in s.image_type:
            append_series(fmap_ap_diff, s)
        elif s.series_description.endswith("dir-PA_epi") and "DIFFUSION" in s.image_type:
            append_series(fmap_pa_diff, s)
        elif s.series_description.endswith("dir-AP_epi") and "DIFFUSION" in s.image_type:
            append_series(fmap_ap_diff, s)
        elif "distortionmap_pa" in protocol and "DIFFUSION" not in s.image_type:
            append_series(fmap_pa_bold, s)
        elif "distortionmap_ap" in protocol and "DIFFUSION" not in s.image_type:
            append_series(fmap_ap_bold, s)
        elif s.series_description.endswith("dir-PA_epi") and "DIFFUSION" not in s.image_type:
            append_series(fmap_pa_bold, s)
        elif s.series_description.endswith("dir-AP_epi") and "DIFFUSION" not in s.image_type:
            append_series(fmap_ap_bold, s)

    #dwi scans (pre and post name change)
        elif "dwi_acq-multishell" in protocol and not s.is_derived:
            append_series(dwi, s)
        elif "abcd_dmri" in protocol and "distortionmap" not in series_description:
            append_series(dwi, s)
        else:
            print("Series not recognized!: ", s.protocol_name, s.dcm_dir_name)


    return info

#intendedfor's
IntendedFor = {
    fmap_pa_diff: [
        '{session}/dwi/sub-{subject}_{session}_acq-multiband_dwi.nii.gz'
#correct
    ],
    fmap_ap_diff: [
        '{session}/dwi/sub-{subject}_{session}_acq-multiband_dwi.nii.gz'
    ],
    fmap_ap_bold: [
        '{session}/func/sub-{subject}_{session}_task-restbold_run-1_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-restbold_run-2_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-fracback_acq-singleband_bold.nii.gz'
    ],
    fmap_pa_bold: [
        '{session}/func/sub-{subject}_{session}_task-restbold_run-1_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-restbold_run-2_bold.nii.gz',
        '{session}/func/sub-{subject}_{session}_task-fracback_acq-singleband_bold.nii.gz'
    ]
}

#ASLmetadata:
MetadataExtras = {
    asl: {
        "PulseSequenceType": "3D",
        "PulseSequenceDetails" : "WIP" ,
        "LabelingType": "PCASL",
        "LabelingDuration": 1.500,
        "PostLabelingDelay": 1.500,
        "BackgroundSuppression": "Yes",
        "M0":"perf/sub-xx_m0scan.nii.gz",
        "LabelingSlabLocation":"X",
        "LabelingOrientation":"",
        "LabelingDistance":2,
        "AverageLabelingGradient": 34,
        "SliceSelectiveLabelingGradient":45,
        "AverageB1LabelingPulses": 0,
        "LabelingSlabThickness":2,
        "AcquisitionDuration":123,
        "InterPulseSpacing":4,
        "PCASLType":"balanced",
        "PASLType": "",
        "LookLocker":"True",
        "LabelingEfficiency":0.85,
        "BolusCutOffFlag":"False",
        "BolusCutOffTimingSequence":"False",
        "BolusCutOffDelayTime":0,
        "BolusCutOffTechnique":"False"
    }
}

def AttachToSession():

    NUM_VOLUMES=40
    data = ['label', 'control'] * NUM_VOLUMES
    data = '\n'.join(data)
    data = 'volume_type\n' + data # the data is now a string; perfect!

    output_file = {

      'name': '{subject}_{session}_aslcontext.tsv',
      'data': data,
      'type': 'text/tab-separated-values'
    }

    return output_file
