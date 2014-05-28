#!/usr/bin/python
import re
import webbrowser
import time
    
try:
    from mechanize import *
except ImportError:
    print "module 'mechanize' required but missing"
    sys.exit(104)

try:
    from BeautifulSoup import BeautifulSoup, NavigableString
#    from bs4 import BeautifulSoup
except ImportError:
    print "module 'BeautifulSoup' required but missing"
    sys.exit(105)
    
    
    

spoj_url="https://www.spoj.com"
    
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
    
    # SPOJ result strings
    result_strings={ 'compiling' : "compiling",
                     'compile_error' : "compilation error",
                     'running' : "running",
                     'running_j': "running judge",
                     'accepted' :  "accepted",
                     'wrong' : "wrong answer",
                     'error' : "runtime error",
                     'limit' : "time limit exceeded",
					 'waiting':"waiting"}
    
    # return true for temporary or active result status (with 'ing')
    def active_status(self,result):
        return (
          result == self.result_strings['compiling'] or
          result == self.result_strings['running'] or
          result == self.result_strings['waiting'] or
          result == self.result_strings['running_j'])
      
# methods
    def __init__(self, local_file=None):      
        # let browser fool robots.txt
        self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; \
              rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        self.br.set_handle_robots(False)
        
        if (local_file):
              self.br.open_local_file(local_file)

    # login with name and password specified in a .netrc file
    # this file has to be owned and accessible only by user which running the process
    def login_with_netrc(self, netrc_file):
        from netrc import netrc # read login data from .netrc
        user, _, password = netrc(netrc_file).authenticators('spoj.com')  # read from ~/.netrc
        return self.login( user, password)

    # login to the SPOJ under browser 'br'    
    def login(self, username, password):

        # authenticate the user
        # print "Authenticating " + username
        self.br.open (spoj_url)
        self.br.select_form (name="login")
        #print "User: '" + username +"'"
        #print "Pass: '" + password + "'"

        self.br["login_user"] = username
        self.br["password"] = password
        response = self.br.submit()
        verify = response.read()
        # print verify
        if (verify.find("Authentication failed!") != -1):
            print "Error authenticating - " + username
            return 0
        
        self.user_ = username
        self.pass_ = password
        return 1


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
        self.br.open(spoj_url + "/submit")
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


    # fetch given url    
    def fetch_from_link(self,  url, delay):
        # get page without visiting
        time.sleep(delay)        
        response=self.br.open_novisit(url)
        return response.read()
    #
    # Extract all accessible submission results.
    # Only search on the first page of the user status.
    #
    def get_sub_results(self,sub_id):
        # items on one status page
        items_per_page=20
        
        pg=self.br.open(spoj_url + "/status/" + self.user_ + "/all")
        #pg=self.br.open_local_file("status.html")
        #open("status.html","w").write( pg.read() )
               
        row_data = {}
        row_data['id'] = sub_id
        
        soup = BeautifulSoup( pg.read() )
        # get max id of the list (may not be presented)
        max_id=soup.find("input", { "id" : "max_id"}, recursive=True)['value']
        
        # get the link to the submitted source, the first cell on the status row
        # this link points to: /files/src/<sub_id>
        id_link=soup.find("a", {"sid" : str(sub_id), "title" :"View source code"}, recursive=True)
        
        row=id_link.parent.parent
        # cells on status row:
        # 0 - submition ID link
        # 1 - selection checkbox
        # 2 - date and time of submission
        # 3 - problem link
        # 4 - result (text + edit and run links)
        # 5 - time (link to best times)
        # 6 - mem (link to stdio for the problem author)
        # 7 - lang (link to results of individual tests)
        #cell_date = cell_id.nextSibling
            
        row_data['date'] = row.find("td", "status_sm").string.strip()
                
        status_cell=row.find("td", "statusres")
        
        #print status_cell.contents
        
        details=status_cell.find("a", {"title" : "View details."})
        if (details) :
            status = details.contents[0]
        else :
            status = status_cell.contents[0]
        
        row_data['result_full'] = status.strip()
        row_data['result'] = "unknown"
        for key,result in self.result_strings.iteritems() :
            if ( row_data['result_full'].find(result) > -1 ) :
                row_data['result'] = result
        #if (row_data['result'] == "unknown") : 
        #    row_data['result'] = ">" + row_data['result_full'] + "<"
        row_data['result_full'] = row_data['result']       
        
        # return if the judge is not finished, just report current status/result
        if (self.active_status(row_data['result'])):
            return row_data
                
        row_data['time'] = row.find("td", id="statustime_"+str(sub_id)).a.string.strip()
        cell_mem = row.find("td", id="statusmem_"+str(sub_id))
        if (cell_mem.a):
              row_data['mem'] = cell_mem.a.string.strip()
        else:
              row_data['mem'] = cell_mem.string.strip()
        
        row_data['stdio']=""
        if (row_data['result'] == "compile_error"):
            stdio_link = spoj_url + "/files/error/" + str(sub_id)
            row_data['stdio'] = self.fetch_from_link( stdio_link )
        else :
            if (row_data['result'] == "runtime error"):
                row_data['result_full']=""
                for item in status_cell.contents[:3] :
                    # print item.__class__.__name__
                    if ( type(item) == NavigableString ) :
                        row_data['result_full'] += item
                    else :
                        row_data['result_full'] += item.prettify()
                row_data['result_full'] = row_data['result_full'].strip()        

            stdio_link = spoj_url + "/files/stderr/" + str(sub_id)                
            row_data['stdio']= self.fetch_from_link(stdio_link, 5)
        
        cell_lang = row.find("td", "slang")

        test_link = spoj_url + "/files/psinfo/" + str(sub_id)
        row_data['test_info'] = self.fetch_from_link( test_link , 0)
        
        #print row_data
        return row_data
        
        