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
    existing_attachments = [f.name for f in existing_attachments if ".zip" in f.name]

    analyses = ses.analyses
    analyses_to_delete = []
    attachments_to_delete = []
    for x in existing_attachments:

        for al in analyses:

            inputs = al.inputs

            if inputs:
                inputs2 = [i.name for i in inputs]

                if x in inputs2:
                    print("Must delete analysis associated with ", x)

                    analyses_to_delete.append(al.id)
                    attachments_to_delete.append(x)

                    #fw.delete_container_analysis(ses.id, al.id)

    if analyses_to_delete:
        for al in set(analyses_to_delete):
            fw.delete_container_analysis(ses.id, al)

    if attachments_to_delete:
        for at in set(attachments_to_delete):
            ses.delete_file(at)
