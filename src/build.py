'''
Created on 21.08.2014

@author: flyninja
'''

import sys, traceback
from _pyio import StringIO
from xml.dom import pulldom
from xml.sax.expatreader import ExpatParser
import MySQLdb as mysql
from django.core import management


class DatabaseAccount(object):
    
    def __init__(self, fl, **kw):
        
        self._user = None
        self._password = None
        self._host = None
        
        with open(fl, 'r') as f: self.stream = pulldom.parse(StringIO(f.read()), ExpatParser())
        
        for event, node in self.stream:
            if node.nodeName != 'account' : continue
            if node.hasAttribute('host'): self._host = node.getAttribute('host')
            if node.hasAttribute('user'): self._user = node.getAttribute('user')
            if node.hasAttribute('password'): self._password = node.getAttribute('password')
        
    def get_user (self): return self._user
    def get_password (self): return self._password
    def get_host (self): return self._host
    

def create_database (cnf):
    
    sql = "DROP DATABASE IF EXISTS `djangotest`;\n"
    sql += "CREATE DATABASE `djangotest`\n"
    sql += "DEFAULT CHARACTER SET utf8\n"
    sql += "DEFAULT COLLATE utf8_general_ci;\n"
    sql += "GRANT ALL PRIVILEGES ON djangotest.* TO '%s'@'%s' IDENTIFIED BY '%s'\n"
    sql += "WITH GRANT OPTION;\n"
    sql += "FLUSH PRIVILEGES;\n"
    
    sql = sql % (cnf.get_user(), cnf.get_host(), cnf.get_password())
    
    db = mysql.connect(host=cnf.get_host(),user=cnf.get_user(),passwd=cnf.get_password())
    cursor = db.cursor()
    cursor.execute(sql)
    
    pass


def build_project (args):
    
    dbacc = DatabaseAccount('src/db.xml')
    create_database(dbacc);
    

if __name__ == '__main__':
    
    try:
        build_project(sys.argv[1:])
    except:
        traceback.print_exc()
        sys.exit(-1)