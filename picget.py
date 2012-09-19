import urllib, re, os

def gethtml(url):
	rhtml = urllib.urlopen(url)
	rhtml = rhtml.read()
	html = ''
	for i in rhtml:
		html += i
	return html

def tumblrhtml(url):
	url = 'http://' + url + '.tumblr.com/page/'
	x = 0
	fhtml = ''
	while x >= 0:
		html = gethtml(url + str(x + 1))
		fhtml += html
		if '"post-body ' not in html: break
		else: x += 1
	html = fhtml
	return html

def instagramhtml(url):
	url = 'http://web.stagram.com/n/' + url + '/'
	nhtml = gethtml(url)
	html = nhtml
	next = re.findall('<a href="/n/.+/.+" rel="next">Earlier</a>', nhtml)
	while len(next) >= 1: 
		page = next[0]
		page = 'http://web.stagram.com' + page[9:-24]
		nhtml = gethtml(page)
		html += nhtml
		next = re.findall('<a href="/n/.+/.+" rel="next">Earlier</a>', nhtml)
	return html

def getlinks(html):
    html = html
    ohtml = html
    links = []
    imgs = {}
    while html.find('"') != -1:
        p = html.find('src="')
        html = html[p+5:]
        pp = html.find('"')
        link = html[:pp]
        html = html[pp:]
        if 'http://' in link and link not in links:
            if '.js' not in link and link[-4] == '.':
                links.append(link)
        else:
            continue   
    while ohtml.find('"') != -1:
        p = ohtml.find('href="')
        ohtml = ohtml[p+6:]
        pp = ohtml.find('"')
        link = ohtml[:pp]
        ohtml = ohtml[pp:]
        if 'http://' in link and link not in links:
            if '.js' not in link and link[-4] == '.':
                links.append(link)
        else:
            continue
	for i in links:
		t = i
		while t.find('/') != -1:
			t = t[(t.find('/') + 1):]
		imgs[i] = t
	return imgs

def editdir(name, location):
	os.chdir(location)
	os.mkdir(name)
	os.chdir(name)

def getimgs(imgs):
	am = 0
	for key in imgs.iterkeys():
		try:
			urllib.urlretrieve(key, imgs[key])
			stat = os.stat(imgs[key])
			size = stat.st_size / 1000
			if size < 1:
				os.remove(imgs[key])
			else:
				am +=1
		except IOError:
			continue

def main():
	url, urltype = 'whdime', 'tumblr' # URL (or Instagram/Tumblr username) and URL type, leave as is if not a 'tumblr' or 'instagram'.
	name, location = 'PicGet', '/Users/kylesnav/Desktop' # Name of the will be created folder (your choice) and location
	if urltype == 'tumblr':
		html = tumblrhtml(url)
	elif urltype == 'instagram':
		html = instagramhtml(url)
	else:
		html = gethtml(url)
	editdir(name, location)
	imgs = getlinks(html)
	getimgs(imgs)

if __name__ == '__main__':
	main()
