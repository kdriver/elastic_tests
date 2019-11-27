import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-f","--file")
parser.add_argument("-i","--index_delete",action="store_true")
parser.add_argument("-d","--docs_delete",action="store_true")
cla = parser.parse_args()
print(cla.index_delete,cla.docs_delete,cla.file)