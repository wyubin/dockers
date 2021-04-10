#!/usr/bin/env python
import xml.etree.ElementTree as ET
import json,re,sys

class parser():
	"""parse MS-GFplus XML output to a reliable json object including prot2len, pep2prot_ranges and pep2scan_scores,
	for compatible with commandline script, args is argparse input

	:param dict args: arguments from argparse(including input_xml,out_json).
	"""
	def __init__(self, args={}):
		"only point args to self.args"
		self.args = args

	def parse(self,xml_file_o):
		"""return info dict of parse result, use xpath to find specific node for info parse

		:param file xml_file_o: file object of xml
		:return: dict of prot2len, prot2pep_ranges(start will -1 for eazy count) and pep2scan_scores.
		:rtype: dict
		"""
		t_root = ET.parse(xml_file_o).getroot()
		# setup namespace
		re_pre = re.findall('{(.+)}',t_root.tag)
		ns = {} if not re_pre else {'n':re_pre[0]}

		prot2len, protid2ac, prot2pep_ranges, pep2scan_scores={},{},{},{}
		# DBSequence
		for i in t_root.iterfind('./n:SequenceCollection/n:DBSequence',ns):
			prot2len[i.attrib['accession']]=int(i.attrib['length'])
			protid2ac[i.attrib['id']]=i.attrib['accession']
			prot2pep_ranges[i.attrib['accession']] = []

		# PeptideEvidence
		for i in t_root.iterfind('./n:SequenceCollection/n:PeptideEvidence',ns):
			n_pep = i.attrib['peptide_ref']
			if n_pep not in pep2scan_scores:
				pep2scan_scores[n_pep] = []

			prot2pep_ranges[protid2ac[i.attrib['dBSequence_ref']]].append([n_pep,int(i.attrib['start'])-1,int(i.attrib['end'])])
			# pep2prot_ranges[n_pep].append([protid2ac[i.attrib['dBSequence_ref']],int(i.attrib['start']),int(i.attrib['end'])])

		# SpectrumIdentificationList
		for i in t_root.iterfind('./n:DataCollection/n:AnalysisData/n:SpectrumIdentificationList/n:SpectrumIdentificationResult',ns):
			ind_scan = int(re.findall('\d+$',i.attrib['id'])[0])
			for j in i.iterfind('n:SpectrumIdentificationItem',ns):
				n_pep = j.attrib['peptide_ref']
				score = float(j.findall("n:cvParam[@name='MS-GF:SpecEValue']",ns)[0].attrib['value'])
				pep2scan_scores[n_pep].append([ind_scan,score])

		return {'prot2len':prot2len,'prot2pep_ranges':prot2pep_ranges,'pep2scan_scores':pep2scan_scores}

	def main(self):
		"based on argparse input to process data for commandline user"
		res = self.parse(self.args['input_xml'])
		json.dump(res,self.args['out_json'], separators=(',', ':'))

if __name__ == '__main__':
	import argparse
	argparser = argparse.ArgumentParser(description = parser.__doc__, formatter_class = argparse.ArgumentDefaultsHelpFormatter)
	argparser.add_argument('input_xml', nargs='?', help='xml output file from MS-GFplus', metavar='input_xml',type=argparse.FileType('r'),default=sys.stdin)
	argparser.add_argument('-o','--out_json',help='output json file',metavar='out_json',type=argparse.FileType('w'),default=sys.stdout)
	args = argparser.parse_args()

	a=parser(vars(args))
	a.main()
