from ctypes import *
import os
import sys
import ftplib

"""
ftp.cwd(pathname) # 设置FTP当前操作的路径
ftp.dir() # 显示目录下所有目录的信息
ftp.nlst() # 获取目录下的文件
ftp.mkd(pathname) #新建远程目录
ftp.pwd() #返回当前所在位置
ftp.rmd(dirname)  # 删除远程目录
ftp.delete(filename) # 删除远程文件
ftp.rename(fromname,toname) # 将fromname修改为toname
ftp.storbinary('STOR filename.txt',file_handle,bufsize)#上传目标文件
ftp.retbinary('RETR filename.txt',file_handle,bufsize) # 下载ftp文件

ftp.quit() # 发送quit命令给服务器并关闭连接
ftp.close() # 单方面的关闭连接，不应该在ftp.quit()之后 
"""


class myFTP:
    ftp = ftplib.FTP()
    bIsDir = False

    def __init__(self, host, port="21"):
        self.ftp.set_debuglevel(1)
        self.ftp.set_pasv(0)  # 0主动模式，1被动模式
        self.ftp.connect(host, int(port))

    def Login(self, user, password):
        self.ftp.login(user, password)
        print(self.ftp.welcome)

    def DownloadFile(self, LocalFile, RemoteFile):
        print("downloading to ", LocalFile)
        try:
            file_handler = open(LocalFile, "wb")
            self.ftp.retrbinary("RETR {}".format(RemoteFile), file_handler.write)
            file_handler.close()  
        except Exception as e:
            os.remove(LocalFile) # clean up failed runs
            print(LocalFile, RemoteFile, e)
        return

    def UploadFile(self, LocalFile, RemoteFile):
        if os.path.isfile(LocalFile) == False:
            raise "这不是一个合法的文件路径"
        file_handler = open(LocalFile, "rb")
        self.ftp.storbinary("STOR {}".format(RemoteFile), file_handler, blocksize=4096)
        file_handler.close()
        return

    def UpLoadFileTree(self, LocalDir, RemoteDir):
        if os.path.isdir(LocalDir) == False:
            raise "这不是一个合法的文件夹路径"
        LocalNames = os.listdir(LocalDir)
        self.ftp.cwd(RemoteDir)
        for Local in LocalNames:
            src = os.path.join(LocalDir, Local)
            if os.path.isdir(src):
                self.UpLoadFileTree(src, Local)
            else:
                try:
                    self.UploadFile(src, Local)      
                except Exception as e:
                    print(src, Local, e)
                    
        self.ftp.cwd("..")
        return

    def DownLoadFileTree(self, LocalDir, RemoteDir):
        """Recursively download all files under the RemoteDir

        Args:
            LocalDir (str): absolute path to download dir
            RemoteDir (str): relative path on server
        """
        if os.path.isdir(LocalDir) == False:
            os.makedirs(LocalDir)
        self.ftp.cwd(RemoteDir)

        try:
            RemoteNames = self.ftp.nlst()          
            for file in RemoteNames:
                Local = os.path.join(LocalDir, file)
                print("remote file:", file)
                if self.isDir(file):
                    self.DownLoadFileTree(Local, file)
                else:
                    try:
                        self.DownloadFile(Local, file)           
                    except Exception as e:
                        print(LocalDir, file, e)
        except Exception as e:
            print("directory listing failed, ", LocalDir, RemoteDir, e)


        self.ftp.cwd("..")
        return

    def show(self, list):
        result = list.split(" ")
        print("list", result)
        if self.path in result and result[0][0] == 'd':
            self.bIsDir = True

    def isDir(self, path):
        self.bIsDir = False
        self.path = path
        # this ues callback function ,that will change bIsDir value
        res = self.ftp.retrlines("LIST", self.show)
        print("isDir", res, self.bIsDir)
        return self.bIsDir

    def close(self):
        self.ftp.quit()


"""
1. We measure two things, first is the query execution time 
2. Then we measure the log size overhead.
3. Also calculate the percentage of permission denied requests!!!
"""

def getLogSize():

    return 0

if __name__ == "__main__":
    ftp = myFTP("localhost")
    ftp.Login("ftpuser1", "ftpuser1-pass")

    ftp.DownLoadFileTree(os.getcwd() + "/files/", "/files")  # ok
    # ftp.UpLoadFileTree(os.getcwd() +"/files/", "/files")
    ftp.close()
    print("ok!")
