# copy spa_tmpl to project static folder
cp -r ../python/static/share_spa_tmpl static/spa_tmpl
# edit config.py and add page in "<page_name>.html" and "<page_name>.js"
# finally, build SPA index.html in static/html/
../../python_module/jinja2static.py static/spa_tmpl static/html
