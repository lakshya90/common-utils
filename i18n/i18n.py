import json
import sys
from collections import OrderedDict
from pprint import pprint
from google.cloud import translate
from optparse import OptionParser

def construct_usage():
	parser = OptionParser(usage="%prog -l <Space separated target Google language code(s)> [-i <json input file to be translated>]", version="%prog 1.0")
	parser.add_option("-i","--input", action="store", default="en_IN.json", dest="input_file", help="Enter your existing json input file path to be translated")

	parser.add_option("-l","--language", action="store_true", default="kn", dest="language", help="Enter the Google language code(s) of the target translation language(s) separated by spaces")

	return parser

def check_arguments(parser):

	(options,args) = parser.parse_args()

	if len(args) < 1 :
        	print ("\nWrong number of arguments.\n")
		parser.print_help()
		sys.exit()

	return options, args

def list_languages():
	translate_client = translate.Client()
        results = translate_client.get_languages()
	return results
		
 
def translate_text(options, args, parser):
	input_file = options.input_file
	target_file = args
	
	accepted_target_languages = [i['language'].encode('ascii') for i in list_languages()]	

	for i in target_file:
		if i not in accepted_target_languages:
			print '\n The entered language code is not supported by the program.\n'
			sys.exit()

	try:
		json_data = open(input_file)
		print json_data
	
	except IOError:
		print '\nThe json file you entered does not exist.\n' 
		parser.print_help()
		sys.exit()
	
	data = json.load(json_data, object_pairs_hook=OrderedDict)
	json_data.close()
	
	translate_client = translate.Client()
	for i in target_file:
		filename = 'languages/' + str(i)+'_'+'IN'.upper()+'.json'	
		print filename
		with open(filename,'w') as f:	
			f.write('{')
			for k,v in data.items():
				translation = translate_client.translate(v, target_language=str(i))
				f.writelines(u'"{}": "{}",\n'.format(k,translation['translatedText']).encode('utf-8'))

			f.write('}')
			f.close()


if __name__ == "__main__":
	parser = construct_usage()
	options, args = check_arguments(parser)
	translate_text(options, args, parser)
