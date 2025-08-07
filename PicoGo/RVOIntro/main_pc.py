#encoding=utf8
import os
import argparse 
# import g1_hash
import sys
from ftplib import FTP
# import res_encrypt
import sys
from ftplib import FTP
# import wdfpacker
# from hunter_cli import Hunter
# from hunter_cli.open_platform import get_api_token


# PYTHON_PATH = "D:\\mhxy\\engine\\python-2.7.3"
# PYTHON_EXE  = PYTHON_PATH + "\\PCBuild\\python.exe"

DesRoot = "Resources\\"
SrcRoot = ""
FtpPath = ""
PhonePath = ""
target = ""

UploadPatchList = []
CompiledList = []



root = None
# log_handler = None
# def write_log(info):
# 	global log_handler,root
# 	if not log_handler:
# 		if not root:
# 			return
# 		log_handler = open(root + "g1_vs_log.txt","a")
# 	log_handler.write(info)
# 	log_handler.write("\n")
# 	log_handler.flush()

# def finish_log():
# 	if log_handler:
# 		log_handler.close()


def get_hunter(args):
	if args.useHunter2 == "false":
		from hunter_cli import Hunter
		hunter = Hunter(args.token, args.process, devip=args.ip,devid = args.deviceId)
		return hunter
	else:
		from hunter2_cli import Hunter
		hunter = Hunter(args.token, args.process, devip=args.ip,devid = args.deviceId)
		return hunter



# def compile_script():
# 	print("compile script")
# 	cmd = PYTHON_EXE + " -OO " + SrcRoot + "build_single.py " + SrcRoot + " " + DesRoot + " " + target
# 	print(cmd)
# 	os.system(cmd)


# def get_upload_py_patch_list():
# 	global s,UploadPatchList
# 	fn = target.split("\\")
# 	fn = fn[-1]
# 	UploadPatchList.append(fn)
# 	print(UploadPatchList)

# def get_hash(filename):
# 	return "%08x" % wdfpacker.filepathid(filename)


# def upload():
# 	print("upload")
# 	global FtpPath,PhonePath
# 	ftp = FTP()
# 	ftp.connect("g1.nie.netease.com","21")
# 	ftp.login("wlw","g1_ftp")
# 	bufsize = 1024
# 	info = ""
# 	ftp_root = "patch/syn/pctestDemoAndroid/"
# 	for v in UploadPatchList:
# 		fn = DesRoot + "mhimage\\" + v
# 		path = ftp_root + v
# 		print(fn,path)
# 		FtpPath = path[6:]
# 		PhonePath = "pctestDemoAndroid/mhimage/" + v
# 		file_handler = open(fn,"rb")

# 		ftp.storbinary("STOR " + path,file_handler,bufsize)
# 		file_handler.close()
# 	ftp.quit()

def upload_py():
	print("upload")
	global FtpPath,PhonePath
	ftp = FTP()
	ftp.connect("g1.nie.netease.com", 21)
	ftp.login("wlw","g1_ftp")
	bufsize = 1024
	info = ""
	ftp_root = "patch/syn/pc/"
	for v in UploadPatchList:
		fn = v.split("\\")[-1]
		path = ftp_root + fn
		# print(fn,path)
		FtpPath = path[6:]
		# PhonePath = "pctestDemoAndroid/mhimage/" + fn
		PhonePath = "eximage/" + fn
		file_handler = open(v,"rb")

		ftp.storbinary("STOR " + path,file_handler,bufsize)
		file_handler.close()
	ftp.quit()

def syn(args):
	global FtpPath,HashName,PhonePath
	context = ""
	if args.process == "CallMeLeaderJack":
		context = '''do 
					require "out_script.hunter_tool"
					out_script.hunter_tool.download_py_from_ftp_and_update("%s","tmpbase/%s")
			 end'''%(FtpPath,PhonePath)
	else:
		context = '''
import ht_reload
ht_reload.down_py_from_ftp("%s","%s")
'''%(FtpPath,PhonePath)

	print(context)
	hunter = get_hunter(args)
	hunter.script(context)

def parse_file(args):
	fn = args.file.replace("/","\\")
	if fn.startswith("\\"):
		fn = fn[1:]
	
	args.file = fn

	root = args.root

	root = root[0].upper() + root[1:]
	tag = "mhimage"
	idx = fn.find(tag)
	fn = fn[idx + len(tag) + 1:]

	fn = fn.replace(root,"")
	return fn





def synPy(args):
	global target
	fn = parse_file(args)
	# s = fn.split("\\")
	print("syn py")
	# target = "\\".join(s) #mhimage\\mobile\\innerchatwnd.py
	target = args.file #D:\\G1\\remote_mobile\\mhimage\\vscode_syn_test.py
	print("target",target)
	UploadPatchList.append(target)

	upload_py()
	syn(args)


if __name__ == '__main__':
	parser = argparse.ArgumentParser() 
	parser.add_argument('-name', type=str,help='name')
	parser.add_argument('-deviceId', type=str,help='device id')
	parser.add_argument('-ip', type=str,help='device ip')
	parser.add_argument('-process', type=str,help='hunter process')

	parser.add_argument('-token', type=str,help='token')
	parser.add_argument('-cmd', type=str,help='cmd')
	parser.add_argument('-file', type=str,help='cur edit file')
	parser.add_argument('-root', type=str,help='root path')
	parser.add_argument('-pyFile', type=str,help='main.py')
	parser.add_argument('-useHunter2', type=str, default='false',help='use hunter2')
	args = parser.parse_args()
	
	
	func_map = {}
	func_map["synPy"] = synPy

	root = args.root
	
	SrcRoot = root + "mhimage\\"
	DesRoot = root + "Resources\\"
	
	# write_log("start")
	# write_log(str(args))
	if args.cmd in func_map:
		# write_log("func:" + args.cmd)
		func_map[args.cmd](args)
	else:
		# write_log("no func:" + args.cmd)
		pass
	
	# finish_log()

