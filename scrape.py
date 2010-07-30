import sys
import re
import urllib2
import urlparse 
#import html5lib
#from html5lib.filters import sanitizer
from BeautifulSoup import BeautifulSoup
url_prefix = re.compile('''^(http[s]?://)[^+]*?''')

# requires Beautiful Soup 3.0.8.1 (NOT the 3.1 series which has a worse parsing engine)


def main(input_url):
    message = ""
    title = ""
    description = ""
    url_set = set()
    request = urllib2.Request(input_url)
    split_input_url = urlparse.urlparse(input_url)
    #host = request.get_host()
    #scheme = request.get_type()
    #selector = request.get_selector()

    if not message:
        if not url_prefix.match(input_url):
            message = "Bad input url"

    if not message: 
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            message  = 'The server couldn\'t fulfill the request.'
            message += 'Error code: %s' %  str(e.code)
        except urllib2.URLError, e:
            message = 'We failed to reach a server.'
            message += 'Reason: %s' % str(e.reason)
        except ValueError, e:
            message =  "Bad url type. Must start with http or https"
        else:
            pass

    if not message:
        html = response.read()
        #html = html.replace("\"=", "=\"")  
        #html = html.replace('/</g', '&lt;');
        #html = html.replace('/>/g', '&gt;');
  
        #p = html5lib.HTMLParser()
        #parse_tree =  p.parse(html)
        #walker = html5lib.treewalkers.getTreeWalker("dom")
        #stream = walker(parse_tree)
        #clean_stream = sanitizer.Filter(stream) 
        #print dir(clean_stream)
        #print clean_stream.source
        #s = html5lib.serializer.htmlserializer.HTMLSerializer(omit_optional_tags=False)
        #output_generator = s.serialize(stream)
        #for i in output_generator:
         #   print i

        #exit()
        #try:
        soup = BeautifulSoup(html)
        #except: 
        #   message = "html parse error"
   

    if not message:
        #print soup.prettify()
        try:
           title = soup.title.string
        except:
           pass
    
        for meta_tag in soup.findAll('meta'):
            this_one_is_desc = False
            for j in meta_tag.attrs:
                 icontinue = True
                 try:
                   j[0]
                 except IndexError:
                   icontinue = False

                 try:
                   j[1]
                 except IndexError:
                   icontinue = False

                 if icontinue:
                     attr_key = j[0]
                     attr_val = j[1]
                     if this_one_is_desc:
                        if str(attr_key.lower()) == 'content':
                            description = u"%s" % (attr_val)

                     if str(attr_key.lower()) == 'name' and \
                        str(attr_val.lower()) == 'description':
                         this_one_is_desc = True
                 

        for img_tag in soup.findAll('img'):
            for j in img_tag.attrs:
                 icontinue = True

                 try:
                   j[0]
                 except IndexError:
                   icontinue = False

                 try:
                   j[1]
                 except IndexError:
                   icontinue = False

                 if icontinue:
                     attr_key = j[0]
                     if str(attr_key.lower()) == 'src':
                         url = j[1]
                         abs_url_match = url_prefix.match(url)
                         if not abs_url_match:
                             url_set.add(urlparse.urljoin(input_url,url))
                         else:
                             split_url = urlparse.urlparse(url)
                             input_domain = ".".join((split_input_url.netloc).split(".")[-2:])
                             image_domain = ".".join((split_url.netloc).split(".")[-2:]) 
                             if image_domain == input_domain:
                                 url_set.add(url)
        return  title, description, url_set
    else:
        print message
        return None, None, set()

if __name__ == "__main__":
    title, description, urls = main(sys.argv[1])
    print title
    print description
    for i in urls:
        print i
