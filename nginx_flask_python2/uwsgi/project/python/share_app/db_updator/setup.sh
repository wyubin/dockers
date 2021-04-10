# copy config file and revise it
cp ../python/share_app/db_updator/db_updator.tmpl.json config/db_updator.json
# soft link daemon to project folder
ln -fs /home/wyubin/project/python/share_app/db_updator/daemon.py ./daemon_db_updator.py
chmod +x ../python/share_app/db_updator/daemon.py
# copy mod and revise it
# cp ../python/share_app/db_updator/mod.py util/mod_db_updator.py

chown -R wyubin:www-data util
chmod -R 755 util

# make db_updator static dir
mkdir static/doc/db_updator
# copy mail tmpl and revise it
cp -rf ../python/share_app/db_updator/mail_html static/doc/db_updator
# make tmp dir for data process
mkdir static/doc/db_updator/tmp
mkdir static/doc/db_updator/ref
mkdir static/doc/db_updator/old_log

chown -R wyubin:www-data static/doc/db_updator
chmod -R 775 static/doc/db_updator

# sql db settings
cp ../../python_module/file2sql/nhri_enterovirus/sql_conf.json \
	./static/doc/db_updator/
cp ../../python_module/file2sql/nhri_enterovirus/setup_conf.json \
	./static/doc/db_updator/
