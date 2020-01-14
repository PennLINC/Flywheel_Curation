import flywheel
import datetime
import time
import pytz

print("Loading flywheel data")
fw = flywheel.Client()
proj = fw.lookup('bbl/ALPRAZ_805556')
sessions = proj.sessions()
sessions = [fw.get(x.id) for x in sessions]
# %%
def get_latest_fmriprep(session):

    if session.analyses:

        timezone = pytz.timezone("UTC")
        init_date = datetime.datetime(2018, 1, 1)
        latest_date = timezone.localize(init_date)

        latest_run = None

        for i in session.analyses:
            gear_name = i.gear_info['name']
            state = i.job.state
            date = i.created
            if 'fmriprep' in gear_name and date > latest_date and state =='complete':
                latest_date = date
                latest_run = i

        if latest_run is not None:
            fmriprep_out = [x for x in latest_run.files if 'fmriprep' in x.name][0]
            fmriprep_out
            return(fmriprep_out)

        else:
            return None

    else:
        return None
# %%
def acquisition_t1(acq):

    t1_to_return = None
    is_t1 = False

    acq = fw.get(acq.id)
    filelist = [x for x in acq.files if x.type in ["nifti", "dicom"]]

    for f in filelist:

        if f.type == "nifti":
            if 'BIDS' in f.info:
                if 'T1w' in f.info['BIDS']['Modality']:

                    t1_to_return = f
                    is_t1 = True

    if is_t1:
        return t1_to_return
# %%

def get_task_file(sess):

    # get the taskfile attachment

    return None

print("Gathering input files for each session")
t1s = {}
fmripreps = {}
taskfiles = {}

for num, ses in enumerate(sessions):
    print(str(num), " of ", len(sessions))

    # t1
    t1_list = [acquisition_t1(a) for a in ses.acquisitions()]
    t1_list = [i for i in t1_list if i]
    t1s[ses.label] = t1_list[0]

    #fmriprep
    fmripreps[ses.label] = get_latest_fmriprep(ses)

    #task attachment
    taskfiles[ses.label] = get_task_file(ses)

# %%
xcp = fw.lookup('gears/xcpengine-fw')
# %%
designFile = [x for x in proj.files if x.name == "task_alpraz_acompcor.dsn"][0] # DESIGN FILE IS LOCATED HERE
designFile = proj.get_file(designFile.name)

xcp_runs = {}

exclude = [] # this list is empty

for num, ses in enumerate(sessions):


    if ses.label not in exclude:

        fmriprep = fmripreps[ses.label]
        t1 = t1s[ses.label]
        taskfile = taskfiles[ses.label]

        if all([fmriprep, t1]):
            print(ses.label, " has all required inputs")
            myconfig = {
                'analysis_type': 'xcp',
                'task_name': ''
            }

            myinputs = {
                'fmriprepdir': fmriprep,
                'designfile': designFile,
                'img': t1,
                'taskfile': taskfile
            }

            print("running XCP engine")
            #run = xcp.run(analysis_label="XCP_task_{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())), destination=ses, inputs=myinputs, config=myconfig) # UNCOMMENT

            #xcp_runs[ses.label] = run.id #UNCOMMENT

        else:
            print(ses.label, " incomplete inputs")
            xcp_runs[ses.label] = None

print(xcp_runs)
