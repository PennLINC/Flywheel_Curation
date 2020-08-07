### This heuristic organizes AGGY (808689) data on Flywheel
###
### Ellyn Butler
### August 14, 2019 - September 6, 2019

import os

# create a key
def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

def ReplaceSubject(subj_label):
    return subj_label.lstrip('0')

t1w = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_T1w')
asl = create_key('sub-{subject}/{session}/perf/sub-{subject}_{session}_asl')
asl_moco = create_key('sub-{subject}/{session}/perf/sub-{subject}_{session}_acq-moco_asl')
m0scan = create_key('sub-{subject}/{session}/perf/sub-{subject}_{session}_m0scan')
m0scan_moco = create_key('sub-{subject}/{session}/perf/sub-{subject}_{session}_acq-moco_m0scan')
#t1w_moco = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-moco_run-{item:02d}_T1w')

def gather_session_indeces():

    # use flywheel to gather a dict of all session session_labels
    # with their corresponding index by time, within the subject

    # query subjects
    import flywheel

    fw = flywheel.Client()

    cs = fw.projects.find_first('label="{}"'.format("AGGY_808689"))
    cs_sessions = cs.sessions()
    cs_subjects = [fw.get(x.parents.subject) for x in cs_sessions]
    #cs_subject_labs = [int(x.label) for x in cs_subjects]

    # initialise dict
    sess_dict = {}

    for x in range(len(cs_subjects)):
        # get a list of their sessions
        sess_list = cs_subjects[x].sessions()

        if sess_list:
            # sort that list by timestamp
            sess_list = sorted(sess_list, key=lambda x: x.label) #Not sure this works

            # loop through the sessions and assign the session label an index
            for i, y in enumerate(sess_list):
                sess_dict[y.label] = "AGGY" + str(i + 1)

    return sess_dict

sessions = gather_session_indeces()

def ReplaceSession(ses_label):
    return str(sessions[ses_label])



def infotodict(seqinfo):
    # create the heuristic
    info = {t1w: [], asl: [], asl_moco: [], m0scan: [], m0scan_moco: []}

    for s in seqinfo:
        protocol = s.protocol_name.lower()
        # t1
        if 'mprage' in protocol and 'nav' not in protocol and 'moco' not in protocol and 'ref' not in protocol:
            info[t1w].append(s.series_id)
        elif 'asl' in protocol and s.is_derived == False and s.is_motion_corrected == True:
            info[asl_moco].append(s.series_id)
        elif 'asl' in protocol and s.is_derived == False and s.is_motion_corrected == False:
            info[asl].append(s.series_id)
        elif 'M0' in protocol and s.is_derived == False and s.is_motion_corrected == False:
            info[m0scan].append(s.series_id)
        elif 'M0' in protocol and s.is_derived == False and s.is_motion_corrected == True:
            info[m0scan_moco].append(s.series_id)


    return info
