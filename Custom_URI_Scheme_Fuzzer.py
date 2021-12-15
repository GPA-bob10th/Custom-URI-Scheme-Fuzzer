import pykd
import threading
import os
import time
import ctypes
import itertools
import pathlib
import hashlib

class Fuzzer(pykd.eventHandler):
    def __init__(self):
        threading.Thread(target=self.testURI).start()
        while(1):
            self.createProc()
            pykd.deinitialize()
        
    def testURI(self):
        time.sleep(12)
        for i in range(len(result1)):
            self.uri = result1[i][0] +"/" + result1[i][1]
            if(self.ex):
                print("Waiting...")
                while(1):
                    if(not self.ex):
                        print("Restart...")
                        time.sleep(12)
                        break
            print("steam://" + self.uri)
            os.system(r"start steam://{}".format(self.uri))
            time.sleep(2)
        for i in range(len(result2)):
            self.uri = result2[i][0] +"/" + result2[i][1] +"/"+ result2[i][2]
            if(self.ex):
                print("Waiting...")
                while(1):
                    if(not self.ex):
                        print("Restart...")
                        time.sleep(12)
                        break
            print("steam://" + self.uri)
            os.system(r"start steam://{}".format(self.uri))
            time.sleep(2)

    def createProc(self):
        pykd.initialize()
        pykd.eventHandler.__init__(self)
        self.proc = pykd.startProcess(r"C:\Program Files (x86)\Steam\steam.exe -- steam://open/console")
        self.pid = pykd.getProcessSystemID(self.proc)
        self.ex = False
        pykd.dbgCommand('sxi asrt')
        pykd.dbgCommand('bp crashhandler+0x7e59')
        pykd.go()

    def terminateProc(self):
        print("KILL " + str(self.pid))
        handle = ctypes.windll.kernel32.OpenProcess(0x0001, False, self.pid)
        ctypes.windll.kernel32.TerminateProcess(handle, 0)
        ctypes.windll.kernel32.CloseHandle(handle)

    def onException(self, ex):
        log = ''
        if ex.exceptionCode == 0xc0000005:
            self.ex = True
            name = hashlib.md5(str(time.time()).encode()).hexdigest()
            log += self.uri + "    "+ hex(ex.exceptionCode) + '\n'
            log += pykd.dbgCommand('r') + '\n'
            log += pykd.dbgCommand('dd esp') + '\n'
            log += pykd.dbgCommand('k')
            pathlib.Path('logs\\{}.txt'.format(name)).write_text(log)
            self.terminateProc()
    
    def onBreakpoint(self):
        self.ex = True
        self.terminateProc()

for i in range(1,5):
    file_path = r"C:\Users\d3o3d\Desktop\BoB10_MyProject\Fuzzer\test_list"+ str(i) + ".txt"
    with open(file_path) as f:
        globals()['list{}'.format(i)] = f.read().splitlines()

result1 = list(itertools.product(*[list1,list2]))
result2 = list(itertools.product(*[list1,list2,list3]))
result3 = list(itertools.product(*[list1,list2,list3,list4]))


print('Start')
fuzzer = Fuzzer()
print('End')