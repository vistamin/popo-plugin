#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# author:  Hua Liang [ Stupid ET ]
# email:   et@everet.org
# website: http://EverET.org
# 

import time, httplib, urllib
from pprint import pprint
import win32gui, traceback

LINUX_HOST = "192.168.150.108"
PORT = 34567

def find_windows(class_name, window_name=None):
    hwnds = []
    print class_name
    try:
        hwnd = win32gui.FindWindow(class_name, window_name) 
        print "hwnd1 = %x" % hwnd
        while hwnd:
            try:
                hwnds.append(hwnd) 
                hwnd = win32gui.FindWindowEx(None, hwnd, class_name, window_name)
                print "hwnd2 = %x" % hwnd
            except:
                hwnd = 0
                print u"查询结束"
        return hwnds
    except:
        return hwnds 

def print_hwnds(hwnds):
    for hwnd in hwnds:
        print "hwnd1 = %x" % hwnd
        print 'hwnd:', hwnd, 'title:', win32gui.GetWindowText(hwnd)

def notify_linux(host, title, port=80): 
    try:
        title = title.encode('utf8')
        conn = httplib.HTTPConnection(host, port)
        query = {'title':title,} 
        url = '/' + "?" + urllib.urlencode(query)
        conn.request('GET', url)
        return conn.getresponse() 
    except:
        traceback.print_exc()

last_hwnds = set()
while True: 
    class_names = ["SessionForm","TeamForm", ]
    #window_names = [u"提示",u"兴趣组提示",]
    window_names = []
    allow_team_names = [
                        u"某某兴趣小组",
                        u"Hello - 兴趣组",
                        ]

    print '-' * 40
    hwnds = set()
    for name in class_names:
        hwnds |= set(find_windows(name))
    #for name in window_names:
    #    hwnds |= set(find_windows(None, name.encode('utf8')))

    need_notifies = hwnds - last_hwnds
    print_hwnds(need_notifies)

    last_hwnds = hwnds

    for hwnd in need_notifies:
        title = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        if class_name == "SessionForm":
            print hwnd, title
            rep = notify_linux(LINUX_HOST, title.decode('gbk'), port=PORT)
            print rep.read().decode('utf8').encode('gbk')
            continue
        elif class_name == "TeamForm":
            if title.decode('gbk') in allow_team_names:
                    print hwnd, title
                    rep = notify_linux(LINUX_HOST, title.decode('gbk'), port=PORT)
                    print rep.read().decode('utf8').encode('gbk')

    last_hwnds = hwnds
    time.sleep(1)
