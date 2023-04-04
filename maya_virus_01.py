import os


file_list =[
"D:\tmp\wip\incrementalSave\ep002_Seq007_shot090_Layout__v002.ma\ep002_Seq007_shot090_Layout__v002.0002.ma",
"D:\tmp\wip\incrementalSave\ep002_Seq007_shot090_Layout__v002.ma\ep002_Seq007_shot090_Layout__v002.0003.ma",
"D:\tmp\wip\incrementalSave\ep002_Seq007_shot090_Layout__v002.ma\ep002_Seq007_shot090_Layout__v002.0004.ma",
"D:\tmp\wip\incrementalSave\ep002_Seq007_shot090_Layout__v002.ma\ep002_Seq007_shot090_Layout__v002.0005.ma",
"D:\tmp\wip\incrementalSave\ep002_Seq007_shot090_Layout__v002.ma\ep002_Seq007_shot090_Layout__v002.0001.ma"
]

print (file_list)

file_list_maya = [file for file in file_list if file.endswith(".mb") or file.endswith(".ma")]

print ("file_list_py: {}".format(file_list_maya))