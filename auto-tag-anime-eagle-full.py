import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import model
import tag
from iptcinfo3 import IPTCInfo

class addAnimeTags():
    def __init__(self):
        self.model = model.deepdanbooruModel()

    def navigateDir(self, path):
        if os.path.isdir(path): 
            for root, dirs, files in os.walk(path):
                for filename in files:
                    if (filename[len(filename)-13:len(filename)] != 'thumbnail.png' and (filename[len(filename)-4:len(filename)] != 'json')):
                        print(self.addTagsToImage(root + '/' + filename, root))
        else:
            print(self.addTagsToImage(path, root))

    def addTagsToImage(self, path, root):

        if (path[len(path)-13:len(path)] != 'thumbnail.png' and (path[len(path)-4:len(path)] != 'json')):
            status, tags = self.model.classify_image(path)
            if status == 'success':
                if sys.platform == 'win32':   
                        tag.tag_eagle(root, tags)
                        return 'added ' + str(len(tags)) + ' tags to ' + path
            else:
                return 'failed to add tags for ' + path
            
    def add_tags(self, file, tags):
        if sys.platform == "linux" or sys.platform == "darwin":
            tag.osx_writexattrs(file, tags)
        elif sys.platform == 'win32':
            tag.win_addInfo(file, tags)
    
def parseArgs():
    if len(sys.argv) < 2:
        print("no path")
        sys.exit()

    if not os.path.exists(sys.argv[1]):
        print('path does not exist')
        sys.exit()

if __name__ == "__main__":
    parseArgs()
    addAnimeTags = addAnimeTags()
    addAnimeTags.navigateDir(sys.argv[1])
