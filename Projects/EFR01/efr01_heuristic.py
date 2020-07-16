def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes'

# Create Keys
'''
localizer
MPRAGE_TI1100_ipat2
ep2d_se_pcasl_PHC_1200ms
epi_singlerep_advshim
B0map_onesizefitsall_v3
bbl1_frac2back1_231
bbl1_idemo2_210
DTI_2x32_35
DTI_2x32_36
bbl1_restbold1_124

localizer_32ch
ABCD_T1w_MPR_vNav_setter
ABCD_T1w_MPR_vNav
ABCD_fMRI_DistortionMap_PA
ABCD_fMRI_DistortionMap_AP
ABCD_fMRI_motive1
ABCD_fMRI_motive2
ABCD_fMRI_motive3
ABCD_fMRI_rest
ABCD_fMRI_rest
QSM_SWI_1.5mm
'''

#localizer = create_key('sub-{subject}/ses-{session}/anat/sub-{subject}_ses-{session}_T1w')
t1w = create_key('sub-{subject}/ses-{session}/anat/sub-{subject}_ses-{session}_T1w')
pcasl = create_key('sub-{subject}/ses-{session}/func/sub-{subject}_ses-{session}_acq-pCASL_asl')
epi_single = create_key('sub-{subject}/ses-{session}/func/sub-{subject}_ses-{session}_acq-singleRep_bold')
b0map = create_key('sub-{subject}/ses-{session}/fmap/sub-{subject}_ses-{session}_fieldmap')
fracback = create_key('sub-{subject}/ses-{session}/func/sub-{subject}_ses-{session}_task-fractalNback_bold')
emoid = create_key('sub-{subject}/ses-{session}/func/sub-{subject}_ses-{session}_task-EmoID_bold')
dti_35 = create_key('sub-{subject}/ses-{session}/dwi/sub-{subject}_ses-{session}_acq-35vol_dir-AP_dwi')
dti_36 = create_key('sub-{subject}/ses-{session}/dwi/sub-{subject}_ses-{session}_acq-36vol_dir-AP_dwi')
rest = create_key('sub-{subject}/ses-{session}/func/sub-{subject}_ses-{session}_task-restbold_acq-124volume_bold')

#localizer32 = create_key('sub-{subject}/ses-{session}/anat/sub-{subject}_ses-{session}_T1w')
fmap_pa = create_key('sub-{subject}/ses-{session}/fmap/sub-{subject}_ses-{session}_acq-fMRIdistmap_dir-PA_epi')
fmap_ap = create_key('sub-{subject}/ses-{session}/fmap/sub-{subject}_ses-{session}_acq-fMRIdistmap_dir-AP_epi')
motive1 = create_key('sub-{subject}/ses-{session}/func/sub-{subject}_ses-{session}_task-motive1_run-01_bold')
motive2 = create_key('sub-{subject}/ses-{session}/func/sub-{subject}_ses-{session}_task-motive2_run-02_bold')
motive3 = create_key('sub-{subject}/ses-{session}/func/sub-{subject}_ses-{session}_task-motive3_run-03_bold')
abcd_rest1 = create_key('sub-{subject}/ses-{session}/func/sub-{subject}_ses-{session}_task-restbold_run-01_bold')
abcd_rest2 = create_key('sub-{subject}/ses-{session}/func/sub-{subject}_ses-{session}_task-restbold_run-02_bold')
qsm = create_key('sub-{subject}/ses-{session}/swi/sub-{subject}_ses-{session}_GRE')

def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where
    allowed template fields - follow python string module:
    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    # create the heuristic
    info = {t1w: [], pcasl: [], epi_single: [],
            b0map: [], fracback: [], emoid: [],
            dti_35: [], dti_36: [], rest: [],

            fmap_pa: [], fmap_ap: [], motive1: [],
            motive2: [], motive3: [], abcd_rest1: [],
            abcd_rest2: [], qsm: []}

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

        if "anat_T1w" in protocol and "vnav" not in series_description:
                info[t1w].append(s.series_id)

        elif "bbl1_az_id_210" in protocol and "dico" not in series_description:
            if "dico" not in [x.lower() for x in image_type]:
                info[emotion_id].append(s.series_id)

        elif "bbl1_az_rec_210" in protocol and "dico" not in series_description:
            if "dico" not in [x.lower() for x in image_type] and s.dim3 > 2:
                info[emotion_rec1].append(s.series_id)
        else:
            print("Template not found for protocol", protocol)

    return info
