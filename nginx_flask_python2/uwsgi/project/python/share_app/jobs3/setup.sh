# copy job conf and revise
cp ../python/share_app/jobs3/jobs.tmpl.json config/jobs.json
# hard link daemon to project folder
ln -sf ../python/share_app/jobs3/daemon.py jobs_daemon.py
# lint job clean script
ln -sf ../python/share_app/jobs3/job_clean.py jobs_clean.py
#[from src] copy job_types into project util folder and revise __init__.py and add job type like blast.py
#cp -r ../python/share_app/jobs/job_types util/

# make jobs static dir
mkdir jobs
chown -R wyubin:www-data jobs
chmod -R 775 jobs
