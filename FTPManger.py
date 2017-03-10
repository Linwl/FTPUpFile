# !usr/bin/env python
# coding:utf-8

import datetime
import sys
import os
from ftplib import FTP

_XFER_FILE = 'FILE'
_XFER_DIR = 'DIR'


class FTPManger(object):
    '''''
    FTP管理类
    '''

    def __init__(self):
        self.ftp = None

    def __del__(self):
        pass

    def setFtpParams(self, ip, uname, pwd, port=21, timeout=60):
        self.ip = ip
        self.uname = uname
        self.pwd = pwd
        self.port = port
        self.timeout = timeout

    def initEnv(self):
        if self.ftp is None:
            try:
                self.ftp = FTP()
                print '### connect ftp server: %s ...' % self.ip
                self.ftp.connect(self.ip, self.port, self.timeout)
                self.ftp.login(self.uname, self.pwd)
                print self.ftp.getwelcome()
            except Exception,e:
                raise e.message

    def clearEnv(self):
        if self.ftp:
            self.ftp.close()
            print "上传成功!"
            print '### disconnect ftp server: %s!' % self.ip
            self.ftp = None

    def uploadDir(self, localdir='./',remotedir='./'):
        if not os.path.isdir(localdir):
            return
        self.ftp.cwd(remotedir)
        for file in os.listdir(localdir):
            src = os.path.join(localdir, file)
            if os.path.isfile(src):
                self.uploadFile(src, file)
            elif os.path.isdir(src):
                try:
                    self.ftp.mkd(file)
                except:
                    sys.stderr.write('the dir is exists %s' % file)
                self.uploadDir(src, file)
        self.ftp.cwd('..')

    def uploadFile(self, localpath,remotepath='./'):
        if not os.path.isfile(localpath):
            return
        print '正在上传文件到 %s to %s:%s' % (localpath, self.ip, remotepath)
        self.ftp.storbinary('STOR ' + remotepath, open(localpath, 'rb'))

    def __filetype(self, src):
        if os.path.isfile(src):
            index = src.rfind('\\')
            if index == -1:
                index = src.rfind('/')
            return _XFER_FILE, src[index + 1:]
        elif os.path.isdir(src):
            return _XFER_DIR, ''

    def upload(self, src,ftp_path):
        try:
            starttime = datetime.datetime.now()
            filetype, filename = self.__filetype(src)
            self.initEnv()
            if filetype == _XFER_DIR:
                self.srcDir = src
                ftp_path='./'+ftp_path
                self.uploadDir(self.srcDir,ftp_path)
            elif filetype == _XFER_FILE:
                self.uploadFile(src, filename)
            self.clearEnv()
            endtime = datetime.datetime.now()
            print "总耗时%d秒"%(endtime - starttime).seconds
        except Exception,e:
            print e.message
