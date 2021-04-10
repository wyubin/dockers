# copy config file and revise it
cp ../python/share_app/jobs/jobs.tmpl.json config/jobs.json
# hard link daemon to project folder
ln ../python/share_app/jobs/daemon.py jobs_daemon.py
#[from src] copy job_types into project util folder and revise __init__.py and add job type like blast.py
#cp -r ../python/share_app/jobs/job_types util/
