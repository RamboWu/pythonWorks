# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys, os, time, atexit
from signal import SIGTERM

class Daemon:
    def __init__(self, pidfile, stderr='data/deamon_err.log', stdout='data/deamon_out.log', stdin='/dev/null'):
        self.stdin = stdin
        self.stdout = os.path.abspath(stdout)
        self.stderr = os.path.abspath(stderr)
        self.pidfile = pidfile

    def _daemonize(self):
        #脱离父进程
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        #脱离终端
        os.setsid()
        #修改当前工作目录
        os.chdir("/")
        #重设文件创建权限
        os.umask(0)

        #第二次fork，禁止进程重新打开控制终端
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        #重定向标准输入/输出/错误
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        #注册程序退出时的函数，即删掉pid文件
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)

    def delpid(self):
        os.remove(self.pidfile)
    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        #sys.stdout.write('xixixi')
        #sys.stderr.write('hahaha')
        # Start the daemon
        self._daemonize()
        self._run()
    def stop(self):
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return # not an error in a restart
        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)
    def restart(self):
        self.stop()
        self.start()
    def _run(self):
        i = 2

class MyDaemon(Daemon):
    def __init__(self, pidfile):
        Daemon.__init__(self,pidfile)
        task_mgr_log = time.strftime('%Y%m%d') + '.log'
        #self.logger = mod_logger.logger(task_mgr_log)

    def _run(self):
            #self.logger.debug("begin sleep")
            time.sleep(20)
            #self.logger.debug("end sleep")


if __name__ == "__main__":


    daemon = MyDaemon('/tmp/daemon-example.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print 'start daemon'
            daemon.start()
        elif 'stop' == sys.argv[1]:
            print 'stop daemon'
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            print 'restart daemon'
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
