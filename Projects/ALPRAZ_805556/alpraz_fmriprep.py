# %% markdown
# # Setup
# %%
# Import packages
import pandas as pd
import flywheel
fw = flywheel.Client()

# Setup project
# SET A VARIABLE FOR YOUR PROJECT
alpralzProj=fw.projects.find_first('label="ALPRAZ_805556"') #
# SET A VARIABLE FOR YOUR SESSIONS
alprazSes=alpralzProj.sessions() # Alpraz sessions

fmriprep = fw.lookup('gears/fmriprep-hpc')
fmriprep

# A DATETIME FOR THE LABELS
import datetime
now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")

# Freesurfer license
### USE THE FILE I SEND YOU HERE
with open("license.txt") as f:
    freesurfer_lic = f.read()

# Configurations

# LIST FOR TRACKING
analysis_ids = []
fails = []

#OPTIONS FROM THE FMRIPREP CONFIG WINDOW
syn_config = {
    'FREESURFER_LICENSE': freesurfer_lic,
    "ignore": "fieldmaps",
    "cifti_output": True
}

# # Run Gears

# LOOP THROUGH EACH SESSION
# FOR EACH, RUN FMRIPREP

for ses in alprazSes:

    # Get the subject of the session
    subject=fw.get(ses.parents.subject)

    # get the subject ID
    subid=subject.label
    subproject=ses.label # save the subproject name

    # RUN IN A TRY-EXCEPT BLOCK
    try:
        inputs = {

            "freesurfer_license": alpralzProj.files[0],

        }
        _id = fmriprep.run(analysis_label='fmriprep_SDK_{}_{}'.format(ses.label, now), config=syn_config, inputs=inputs, destination=ses)
        analysis_ids.append(_id)
    except Exception as e:
        print(e)
        fails.append(ses)

print("Successful runs:")
print(analysis_ids)
print("Total: ", str(len(analysis_ids)))

print("Failes runs:")
print(fails)
print("Total: ", str(len(fails)))
