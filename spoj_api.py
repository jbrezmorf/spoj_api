#!/usr/bin/python
import re
import webbrowser

    
try:
    from mechanize import *
except ImportError:
    print "mechanize required but missing"
    sys.exit(1)

    
# create a browser object

# add proxy support to browser
#    if len(path_proxy) != 0: 
#        protocol,proxy = options.proxy.split("://")
#        br.set_proxies({protocol:proxy})


class SpojApi:
# data members
    user_=""
    pass_=""
    br=Browser()
# methods
    def __init__(self):      
        # let browser fool robots.txt
        self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; \
              rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        self.br.set_handle_robots(False)
          
    # login to the SPOJ under browser 'br'    
    def login(self, username, password):

        # authenticate the user
        # print "Authenticating " + username
        self.br.open ("http://spoj.pl")
        self.br.select_form (name="login")
        self.br["login_user"] = username
        self.br["password"] = password
        response = self.br.submit()
        verify = response.read()
        if (verify.find("Authentication failed!") != -1):
            print "Error authenticating - " + username
            exit(0)
        
        self.user_ = username
        self.pass_ = password


    #
    # Submit a problem solution in given language.
    #
    def submit(self, problem, source, lang):    
        # detects form for solution submission        
        def complete_form_predicate(form):
          try:
            form.find_control(type="textarea", name="file")
            form.find_control(type="select", name="lang")
            form.find_control(type="text", name="problemcode")
            return True
          except ControlNotFoundError: 
            return False

        # try to submit
        self.br.open("http://www.spoj.pl/submit")
        self.br.select_form(predicate=complete_form_predicate)
        self.br["file"] = source
        self.br["lang"] = [lang]
        self.br["problemcode"] = problem
        pg=self.br.submit()

        m = re.search(r'"newSubmissionId" value="(\d+)"/>', pg.read())  
        if (m == None):
            return -1   # submission failed
            
        submission_id = int(m.group(1))
        return submission_id

    #
    # Extract all accessible submission results.
    # Only search on the first page of the user status.
    #
    def get_sub_results(self,sub_id):
        # items on one status page
        items_per_page=20
        
        pg=self.br.open("http://www.spoj.pl/status/" + self.user_ + "/all")
        open("status.html","w").write(pg.read())
        
        # TODO:
        # use firefox and status.html to ...
        # use PyQuery (firefox like inspector) to get appropriate tags
        # 
    
    
###################################################################################### Main    
    
spoj = SpojApi()    
    
spoj.login( user, password )

source = open("test.bash.src", "r").read()
id=spoj.submit("TEST", source, "28")    

spoj.get_sub_results(id)







'''
#login_pg = br.response()

print " --- Second login ---"
#help(login_pg)

br.select_form(name="login")
br["login_user"] = username
br["password"] = password
resp=br.submit()

open("result.html","w").write(resp.read())
'''

'''  

from netrc import netrc # read login data from .netrc

from urllib import urlencode, quote
from urllib2 import urlopen

#user, _, password = netrc().authenticators('spoj.com')  # read from ~/.netrc



print data        
#r = urlopen("https://www.spoj.com/submit/complete/",  data)# no certificate test


#answer=r.read()
#print answer
#m = re.search(r'"newSubmissionId" value="(\d+)"/>', r.read())  # XXX dirty
#print("submission id %d" % int(m.group(1)))
#webbrowser.open("https://www.spoj.com/status/%s/" % quote(user))


{
    "7": "ADA 95 (gnat 4.3.2)",
    "13": "Assembler (nasm 2.03.01)",
    "104": "Awk (gawk-3.1.6)",
    "28": "Bash (bash-4.0.37)",
    "12": "Brainf**k (bff 1.0.3.1)",
    "11": "C (gcc 4.3.2)",
    "27": "C# (gmcs 2.0.1)",
    "41": "C++ (g++ 4.3.2)",
    "1": "C++ (g++ 4.0.0-8)",
    "34": "C99 strict (gcc 4.3.2)",
    "14": "Clips (clips 6.24)",
    "111": "Clojure (clojure 1.1.0)",
    "31": "Common Lisp (sbcl 1.0.18)",
    "32": "Common Lisp (clisp 2.44.1)",
    "20": "D (gdc 4.1.3)",
    "36": "Erlang (erl 5.6.3)",
    "124": "F# (fsharp 2.0.0)",
    "5": "Fortran 95 (gfortran 4.3.2)",
    "114": "Go (gc 2010-07-14)",
    "21": "Haskell (ghc 6.10.4)",
    "16": "Icon (iconc 9.4.3)",
    "9": "Intercal (ick 0.28-4)",
    "24": "JAR (JavaSE 6)",
    "10": "Java (JavaSE 6)",
    "35": "JavaScript (rhino 1.7R1-2)",
    "26": "Lua (luac 5.1.3)",
    "30": "Nemerle (ncc 0.9.3)",
    "25": "Nice (nicec 0.9.6)",
    "56": "Node.js (0.8.11)",
    "8": "Ocaml (ocamlopt 3.10.2)",
    "22": "Pascal (fpc 2.2.4)",
    "2": "Pascal (gpc 20070904)",
    "3": "Perl (perl 5.12.1)",
    "54": "Perl 6 (rakudo-2010.08)",
    "29": "PHP (php 5.2.6)",
    "19": "Pike (pike 7.6.112)",
    "15": "Prolog (swipl 5.6.58)",
    "4": "Python (python 2.7)",
    "116": "Python 3 (python 3.2.3)",
    "126": "Python 3 nbc (python 3.2.3 nbc)",
    "17": "Ruby (ruby 1.9.3)",
    "39": "Scala (scala 2.8.0)",
    "33": "Scheme (guile 1.8.5)",
    "18": "Scheme (stalin 0.11)",
    "46": "Sed (sed-4.2)",
    "23": "Smalltalk (gst 3.0.3)",
    "38": "Tcl (tclsh 8.5.3)",
    "62": "Text (plain text)",
    "6": "Whitespace (wspace 0.3)",
}
'''
