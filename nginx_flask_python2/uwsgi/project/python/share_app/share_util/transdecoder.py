#!/usr/bin/env python
import re,os,subprocess,sys
from uuid import uuid4
sys.path.append(os.path.dirname(__file__))
import fasta_mini_han

codes = ['universal','Euplotes','Tetrahymena','Candida','Acetabularia']
class pkg():
	"""predict transcript's amino acid sequences

	:param args: args include
	:type update: True
	"""
	def __init__(self, args={}):
		"add all options var into self"
		self.notes = []
		self.args = {}
		self.args.update(args)
		self.env = {
			'cmd_path':os.path.join(os.path.dirname(__file__),'../../util/transdecoder/')
		}
		# addtion

	def res(self):
		"for module result, save a tmp fasta to execute transdecoder"
		#self.args['tmp'] = self.args['tmp'] or os.path.split(__file__)[0]
		cmd_path = os.path.abspath(self.args.get('cmd_path') or self.env['cmd_path'])
		o_path = os.getcwd()
		os.chdir(self.args['tmp'])
		fn = '%s.fa' % uuid4().hex
		f_log = open(fn+'.log','w')

		# save file
		open(fn,'w').write(self.args['fasta'].read())
		# LongOrfs
		t_srp = [os.path.join(cmd_path,'TransDecoder.LongOrfs'),'-t',fn]
		if self.args.get('code') and (self.args['code'] != 'universal'):
			t_srp.extend(['-G',self.args['code']])
		if self.args.get('sense'):
			t_srp.extend(['-S'])
		os.system(' '.join(t_srp))
		p = subprocess.Popen(t_srp, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		f_log.write(p.stdout.read())
		# Predict
		t_srp = [os.path.join(cmd_path,'TransDecoder.Predict'),'-t',fn]
		if not self.args.get('multi'):
			t_srp.extend(['--single_best_orf'])
		os.system(' '.join(t_srp))
		p = subprocess.Popen(t_srp, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		f_log.write(p.stdout.read())
		f_log.close()
		# parse fasta
		res = []
		re_name = re.compile('(\w+):(\d+)-(\d+)\(([-\+])\)')
		for i in fasta_mini_han.fasta_mini_han(open(fn+'.transdecoder.pep')):
			t_re = re_name.findall(i.name)[0]
			t_rng = map(int,t_re[1:3])
			t_strd = 0 if t_re[3]=='+' else 1
			res.append({'name':t_re[0],'seq':i.seq,'from':t_rng[t_strd],'to':t_rng[t_strd-1]})
		if not res:
			for i in ['','.log']:
				os.rename(fn+i,'err_'+fn+i)
		#	return {'log':open(fn+'.log').read()}
		# remove files
		os.system('rm -rf %s*' % fn)
		os.chdir(o_path)
		return res

	def out(self):
		"for commandline output, default use fasta output"
		res = self.res()
		for i in res:
			t_name = '%s|from|%s|to|%s' % (i['name'],i['from'],i['to'])
			self.args['out'].write(fasta_mini_han.fasta_mini_han.seq_o(t_name,i['seq']).fasta())

		self.args['out'].close()

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description = pkg.__doc__, formatter_class = argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-i','--fasta',help='fasta file input',metavar='fasta', type=argparse.FileType('r'),default=sys.stdin)
	parser.add_argument('-o','--out',help='peptide output file',metavar='out', type=argparse.FileType('w'),default=sys.stdout)
	parser.add_argument('-c','--code',help='select a genetic code in %s, default use "universal".' % ','.join(codes), metavar='code',default='universal',choices=codes)
	parser.add_argument('-m','--multi',help='output multiple amino acid if has', action='store_true', default=False)
	parser.add_argument('-s','--sense',help='only output sense strand', action='store_true', default=False)
	parser.add_argument('-t','--tmp',help='tmp dir for cmd execute', default='./')
	parser.add_argument('-p','--cmd_path',help='transdecoder dir')
	args = parser.parse_args()

	a=pkg(vars(args))
	a.out()
