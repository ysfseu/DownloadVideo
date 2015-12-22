from bs4 import BeautifulSoup
import urllib3
import getopt, sys
import _thread, threading
import time,random
urls = [];
filenames = [] ;
CONDITION = threading.Condition();

def downloadFile(link):
	http = urllib3.PoolManager();
	response = http.request("GET",link);
	#print(response.data);
	return response.data;

def parseHtml(html_doc):
	global urls;
	global filenames;
	soup = BeautifulSoup(html_doc, 'html.parser');
	table = soup.find('table');
	text = table.encode('utf-8');
	#print(text);
	#table_body = table.find('tbody');
	for a in table.find_all("a"):
		if a.string != None:
			urls.append(a.get('href'));
			filenames.append(a.string);
	#		print(a.get('href'));
	#return (urls,filenames);


def downloadVideo(urls,filenames):
	for url, filename in zip(urls,filenames):
		http = urllib3.PoolManager();
		download = http.request("GET",url);
		f = open(filename, 'wb');
		f.write(download.data);
		f.close();
	return;
def downloadMThread():
	http = urllib3.PoolManager();
	while True :
            CONDITION.acquire()
            if len(urls) == 0 :
                CONDITION.release();
                return;
            url = urls.pop(0);
            filename = filenames.pop(0);
            CONDITION.notify();
            CONDITION.release();
            try:
            	download = http.request("GET",url);
            	f = open(filename, 'wb');
            	f.write(download.data);
            	f.close();
            except:
            	continue;
            time.sleep(random.random());
def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "l", ["help"]);
        except getopt.GetoptError as err:
        # print help information and exit:
        	print(err) # will print something like "option -a not recognized"
        	usage();
        	sys.exit(2);
        # more code, unchanged
    except:
    	print("error");
    global urls;
    link = args[0];
    if(link[-1]!='/'):
    	link+='/';
    htmlFile = downloadFile(link);
    parseHtml(htmlFile);
    urls = [link+url for url in urls];
    for i in range(15):
    	myTread = threading.Thread(target = downloadMThread,args = ());
    	myTread.start();
    	myTread.join();
    #downloadVideo(urls,filenames);
    return;

if __name__ == "__main__":
    sys.exit(main());
