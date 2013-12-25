# coding: utf-8
'''简单文件信息查询，Tkinter练习使用'''
from Tkinter import *
import os
import time

# 当前路径
currentDir = os.getcwd()

def refreshInfo(listboxDir_, listboxFile_, currentDir):
	'''使用Listbox，更新目录列表
	1.清空目录,和文件目录
	2.当前目录列表，添加.和..两个目录
	3.使用os.path.isdir()函数判断并添加目录项
	4.添加文件项
	'''
	listboxDir_.delete('0', END)
	listboxDir_.insert('1', '.')
	listboxDir_.insert('2', '..')

	listboxFile_.delete('0', END)
	# listdir展示目录下的文件和文件夹
	# isdir判断是否是文件夹,接收函数是完整路径
	# os.sep 是系统的/或\
	for item in (os.listdir(currentDir)):
		if os.path.isdir(currentDir + os.sep + item):
			listboxDir_.insert(END, item)
		else:
			listboxFile_.insert(END, item)
	listboxFile.selection_set(0)
def changeDir(event):
	'''双击改变目录，所以changeDir有参数
	1.双击.不变，双击..返回上一层目录
	2.更新文件和目录显示
	3.更新文件属性信息
	'''

	global currentDir
	# 获取当前选中的内容
	select = listboxDir.get(listboxDir.curselection()) 
	if select == '.':
		pass
	elif select == '..':
		currentDir = os.path.split(currentDir)[0]
	else:
		currentDir = currentDir + os.sep + select
	
	os.chdir(currentDir)
	refreshInfo(listboxDir, listboxFile, currentDir)
	showFileProperties(event)

def showFileProperties(event):
	'''鼠标点到一个文件时，显示文件基本属性
	1.文件路径
	2.文件大小
	3.文件创建，修改，访问时间
	4.使用os.stat模块
	'''
	try:
		file_name = listboxFile.get(listboxFile.curselection())
		file_path = currentDir + os.sep + file_name
		#print file_path
		state = os.stat(r'%s' %str(file_path))
		file_size = state.st_size / 1024.0
		file_create_time = format_time(state.st_ctime)
		file_modify_time = format_time(state.st_mtime)
		file_ask_time = format_time(state.st_atime)

		file_information = ('\n' + '文件名称: ' + file_name + '\n' + '文件路径:\n' + file_path + '\n' + '文件大小: ' +
					str(file_size) + 'Kb\n' + '创建时间: ' + file_create_time
					+ '\n' + '修改时间: ' + file_modify_time + '\n'
					+ '访问时间: ' + file_ask_time)
	#	print file_information
		file_information_message['text'] = file_information
	except:
		file_information_message['text'] = ''
def format_time(stime):
	return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stime))
# 设置UI, 没有使用类，结构化顺序编写的
def main():
	root = Tk()
	root.title('文件信息查看器')
	# 快捷键退出
	root.bind('<Control-q>', sys.exit)

	global file_information_message
	global listboxDir
	global listboxFile
	Label(root, text = '\n').grid(row = 0, column = 0, columnspan = 3)
	Label(root, text = '文件目录').grid(row = 1, column = 0)
	Label(root, text = '文件列表').grid(row = 1, column = 1)
	Label(root, text = '文件属性').grid(row = 1, column = 2)

	listboxDir = Listbox(root, height = 20)
	listboxFile = Listbox(root, height = 20)

	refreshInfo(listboxDir, listboxFile, currentDir)
	# 按键行为绑定
	listboxDir.bind('<Double-Button-1>', changeDir)
	listboxFile.bind('<Button-1>', showFileProperties)

	listboxDir.grid(row = 2, column = 0)
	listboxFile.grid(row = 2, column = 1)
	
	file_information_message = Message(root)
	showFileProperties(0)
	file_information_message.grid(row = 2, column = 2)
	root.mainloop()
if __name__ == '__main__':
	main()
