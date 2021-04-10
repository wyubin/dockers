# import contact module in __init__.py
from contact2.router import mod as mod_contact
app.register_blueprint(mod_contact, url_prefix=os.path.join('/',app.config['PROJECT_NAME'],'contact'))

# copy conf.json to system config and revise
cp ../python/share_app/contact2/contact.conf.json ./config/contact.json

# copy mail tmpl and revise it
cp -rf ../python/share_app/contact2/mail_html/* static/html/contact_tmpl/
