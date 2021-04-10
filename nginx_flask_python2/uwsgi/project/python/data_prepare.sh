scp mirai.iis.sinica.edu.tw:/home/wyubin/mayfield_coral/shys/sql_mk/app.db ./
scp mirai.iis.sinica.edu.tw:/home/wyubin/mayfield_coral/shys/sql_mk/taxid2* static/doc/

# json compression
jq -s '.[0]+.[1]+.[2]' blast_setting.json ../../../static/json/blast_arg.json ../../../static/json/blast_form.json -c > blast.min.json
