import re
import htmlentitydefs
from BeautifulSoup import BeautifulSoup, SoupStrainer
import httplib2
import sqlite3
import urlparse
import json
import logging

logging.basicConfig(filename="professor_profile_scraper.log", level=logging.DEBUG)

h = httplib2.Http(".cache", disable_ssl_certificate_validation=True)

def gen_example_data(h):
    """
    list of professors, here is a professor

    Professor
    ----------
    id, name, profile_full_text, dept
    """
    pass

def make_links_absolute(soup, url):
    for tag in soup.findAll('a', href=True):
        tag['href'] = urlparse.urljoin(url, tag['href'])
    return soup

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)


def get_all_profile_links(h):
    """
    Gets ALL profile links
    """
    profile_links = set()
    page_number = 0

    #sqlite db setup
    con = sqlite3.connect('professors.db')
    cur = con.cursor()

    profile_list_url = 'https://faculty.unt.edu/searchresults.php?faculty=true&search=+search+FPS...&searchtype=basic&image2.x=6&image2.y=4'
    response, content = h.request(profile_list_url)

    logging.info("First pages response status: %s" % (response['status']))

    # remember, header values are strings
    while 1:
        # end condition is no links being found on page
        if page_number == 0:
            # first page, don't need to set page variable
            pass
        else:
            profile_list_url = 'https://faculty.unt.edu/searchresults.php?faculty=true&search=+search+FPS...&searchtype=basic&image2.x=6&image2.y=4&page=%d'\
                    % (page_number)
            logging.info("Getting <%s>" % (profile_list_url))
            response, content = h.request(profile_list_url)

        # link example: https://faculty.unt.edu/editprofile.php?onlyview=1&pid=1938
        profiles_only = SoupStrainer('a', href=re.compile('editprofile'))
        soup = BeautifulSoup(content, parseOnlyThese=profiles_only)
        all_links_for_page = make_links_absolute(soup, 'https://faculty.unt.edu')

        for link in all_links_for_page:
            # also add to sqlite3 db
            if link.get('href', None):
                try:
                    href = link.get('href')
                    sql = "insert into profile_links(link, type) values(?, ?);"
                    cur.execute(sql, (link.get('href'), "professor"))
                    con.commit()
                    logging.info("inserted: <%s> into profile_links"  % (href) )
                except sqlite3.IntegrityError, e:
                    logging.info("<%s> is a duplicate"  % (href) )
                    
        #[profile_links.add(link.get('href') for link in BeautifulSoup(content, parseOnlyThese=profiles_only)]
        logging.debug("Got %d links on page %d" % (len(all_links_for_page), page_number))

        if len(all_links_for_page) == 0:
            logging.debug("No links found on page %d, breaking" % (page_number))
            break
            logging.info("closing db connection")
            con.close()

        page_number += 1

    logging.info("closing db connection")
    con.close()


class Professor:
    """
    TODO: Make sure that all publications are added
    """
    def __init__(self, profile_url=None, name=None, dept=None, full_profile_text=None):
        self.http = httplib2.Http(".cache", disable_ssl_certificate_validation=True)
        response = {}
        response['status'] = "404"

        self.url = profile_url
        if profile_url:
            response, self.profile_html = self.http.request(profile_url)

        if response['status'] == "200" and url != None:
            self.name = self.get_name()
            self.publications = self.get_Publications()
            self.dept = self.get_dept()
            self.full_profile_text = self.get_full_profile_text()
            self.save()

        if profile_url == None:
            self.name = name
            self.dept = dept
            self.full_profile_text = full_profile_text

    def __str__(self):
        return self.name or "unset"

    def get_name(self):
        """
        parses professors name from their profile page

        name html examples:
        <td id="name" align="left">

        3 verified the same, going to scrape them and see what we get
        """
        tds = SoupStrainer('td', {'id' : 'name'})
        logging.info("getting name for <%s>" % (self.url) )
        soup = BeautifulSoup(self.profile_html, parseOnlyThese=tds)
        return unescape(soup.find(text=True))

    def get_dept(self):
        """
        Get's professors dept or returns "uknown"
        """
        logging.info("getting dept for <%s>" % (self.url) )
        form_elements_text_span = SoupStrainer('span', {'class': 'form_elements_text'})
        soup = BeautifulSoup(self.profile_html, parseOnlyThese=form_elements_text_span)
        dept = unescape(soup.find(text=True))
        dept = dept[dept.find('-')+1:]
        return dept
    
    def get_full_profile_text(self):
        logging.info("getting profile text for <%s>" % (self.url) )
        tables = SoupStrainer('table')
        soup = BeautifulSoup(self.profile_html, parseOnlyThese=tables)
        texts = soup.findAll(text=True)
        
        def visible(element):
            if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                return False
            elif re.match('<!--.*-->', str(element)):
                return False
            return True 

        bad_chars = ['', '\n', '\r\n', '&nbsp;']
        visible_text = ' '.join([s.strip() for s in filter(visible, texts) if s.strip() not in bad_chars])
        return visible_text

    def get_Publications(self):
        tables = SoupStrainer('table')
        dataText = self.profile_html

        soup = BeautifulSoup(dataText, parseOnlyThese=tables)
        publicationParse = soup.findAll('span', {'class':'form_elements_text'})
        dataText = ''
        for s in publicationParse:
            dataText = dataText + str(s) + '\n'
        
        
        startIndex = dataText.find('<span class="form_elements_text">Publication</span>')
        endIndex = len(dataText)



    def save(self):
        con = sqlite3.connect('professors.db')

        with con:
            cur = con.cursor()
            try:
                cur.execute("update profile_links set scraped = ? where link is ?;", (1, self.url) )
                logging.info("update profile_links set scraped = %s where link is %s;" %\
                    (0, self.url) )

                cur.execute('insert into professors(name, profile_full_text, dept) values(?, ?, ?);',\
                    (self.name, self.full_profile_text, self.dept) )


                con.commit()

                logging.info('insert into professors(name, profile_full_text, dept) values("%s", "%s...", "%s");' %\
                    (self.name, self.full_profile_text[:10], self.dept) )
                logging.debug("saved: <name: %s>, <dept: %s>, <profile_full_text: %s>" %\
                    (self.name, self.dept, self.full_profile_text[:10]) )

            except sqlite3.IntegrityError, e:
                cur.execute("update profile_links set scraped = ? where link is ?;", (1, self.url) )
                logging.info("update profile_links set scraped = %s where link is %s;" %\
                    (0, self.url) )
                logging.debug("Not saving, <%s> already exists" % self.name)

            except Exception, e:
                print e

def get_professors():
    con = sqlite3.connect('professors.db')

    urls = None
    with con:
        cur = con.cursor()
        
        cur.execute('select link from profile_links where type == "professor" and scraped is 0;')
        urls = [d[0] for d in cur.fetchall()]

        le_professors = [Professor(url) for url in urls]
        with open('professor_data.json', 'w') as f:
            f.write(json.dumps(le_professors))

        #for professor in le_professors:
        #    print professor.name, professor.publications


def write_professors_data():
    con = sqlite3.connect('professors.db')

    cur = con.cursor()
    cur.execute('select name, dept, profile_full_text from professors')
    rows = cur.fetchall()


    professors = []

    for row in rows:
        name = row[0]
        dept = row[1]
        full_profile_text = row[2]
        if row[2] != None:
            full_profile_text = row[2]
        #print "Professor<'%s', '%s', '%s'>" % (name, dept, full_profile_text)
        professor = Professor(profile_url=None, name=name, dept=dept, full_profile_text=full_profile_text)
        professor_data = \
                {'name': professor.name, 'profile_url': professor.url, 'dept': professor.dept,\
                'full_profile_text': professor.full_profile_text}
        professors.append(professor_data)

    with open('professor_data.json', 'wb') as f:
        f.write(json.dumps(professors))

    con.close()



if __name__ == "__main__":
    #get_professors()
    #get_all_profile_links(h)
    write_professors_data()

