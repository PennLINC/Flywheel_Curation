import flywheel
import os

print("Loading flywheel data")
fw = flywheel.Client()
proj = fw.lookup('bbl/ALPRAZ_805556')
sessions = proj.sessions()
sessions = [fw.get(x.id) for x in sessions]

current_dir = os.getcwd()
zips = [current_dir + "/Projects/ALPRAZ_805556/data/" +x for x in os.listdir("./Projects/ALPRAZ_805556/data/")]

for ses in sessions:

    existing_attachments = ses.files
    existing_attachments = [f.name for f in existing_attachments]
    print(existing_attachments)
    file_to_upload = [z for z in zips if str(int(ses.label)) in z]

    if file_to_upload:
        print(os.path.basename(file_to_upload[0]))
        print(os.path.exists(file_to_upload[0]))

        if os.path.basename(file_to_upload[0]) in existing_attachments:
            print("File exists! Removing existing...")
            ses.delete_file(os.path.basename(file_to_upload[0]))

        else:
            print("uploading")
            status = ses.upload_file(file_to_upload[0])
            print(status)
    else:
        print("no file for %s" % ses.label)
