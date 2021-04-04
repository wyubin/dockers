#!/usr/bin/env python

import sys
import os

scriptDir = os.path.split(os.path.realpath(__file__))[0]
## make vassal
dirUwsgi = os.path.join(scriptDir,'../uwsgi')
dirVassql = os.path.join(dirUwsgi,'vassal')
if not os.path.exists(dirVassql):
  os.makedirs(dirVassql)
## make ini
dirProject = os.path.join(dirUwsgi,'project')
pathSklIni = os.path.abspath(os.path.join(dirProject,'python_app.skl.ini'))
for fileTmp in os.listdir(dirProject):
  pathTmp = os.path.join(dirProject,fileTmp)
  if os.path.isdir(pathTmp):
    pathTrg = os.path.abspath(os.path.join(dirVassql,'%s.ini' % fileTmp))
    os.symlink(pathSklIni,pathTrg)
    sys.stderr.write('[INFO] Make ini for Project "%s"\n' % fileTmp)


sys.stderr.write('[INFO] Setup complete!\n')