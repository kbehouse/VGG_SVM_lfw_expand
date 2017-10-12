#!/usr/bin/env python

import json
import os

class FaceTool():
    def __init__(self,faceDB_path = 'faceDB'):
        # self.faceDB_path = 'faceDB'
        self.set_faceDB_path(faceDB_path)
       

    def init_face_index(self):
        face_index_path = self.faceDB_path + "/face-index.json"
        self.face_dic = self.read_json(face_index_path)

    def set_faceDB_path(self, p):
        if os.path.isdir(p):
            self.faceDB_path = p
            self.init_face_index()

    def read_json(self,path):
        """Read a JSON file from path, and convert to object of python."""
        try:
            with open(path) as f:
                content = json.load(f)
                return content
        except IOError as e:
            print(e)
            return None


    def write_json(self, path, content):
        """Write object of python to specify JSON file using JSON format."""
        try:
            with open(path, 'w') as f:
                f.write(json.dumps(content, f, indent=4, separators=(',', ': '), sort_keys=True))
            return True
        except IOError as e:
            print(e)
            return False


    def get_face_label(self, ind):
        if ind == -1:
            return "[None Face]"
        return self.face_dic[str(ind)]

    def get_face_index(self, label):
        for i in self.face_dic:
            if self.face_dic[i] == label:
                return  int(i)
   
        return -1
    


if __name__ == '__main__':   
    f = FaceTool()
    print f.get_face_index('gu')

