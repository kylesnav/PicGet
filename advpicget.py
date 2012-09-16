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
		if '"post - body' not in html: break
		else: x += 1
	html = fhtml
	return html

def instagramhtml(url):
	url = 'http://web.stagram.com/n/' + url + '/'
	nhtml = gethtml(url)
	html = ''
	next = re.findall('<a href="/n/.+/.+" rel="next">Earlier</a>', nhtml)
	while len(next) >= 1: 
		page = next[0]
		page = 'http://web.stagram.com' + page[9:-24]
		nhtml = gethtml(page)
		html += nhtml
		next = re.findall('<a href="/n/.+/.+" rel="next">Earlier</a>', nhtml)
	return html

def getlinks(html):
	png = re.findall(r"src='.+\.png'", html) + re.findall(r'src=".+\.png"', html)
	jpg = re.findall(r"src='.+\.jpg'", html) + re.findall(r'src=".+\.jpg"', html)
	jpeg = re.findall(r"src='.+\.jpeg'", html) + re.findall(r'src=".+\.jpeg"', html)
	gif = re.findall(r"src='.+\.gif'", html) + re.findall(r'src=".+\.gif"', html)
	bmp = re.findall(r"src='.+\.bmp'", html) + re.findall(r'src=".+\.bmp"', html)
	thm = re.findall(r"src='.+\.thm'", html) + re.findall(r'src=".+\.thm"', html)
	rlinks = png + jpg + jpeg + gif + bmp + thm
	links = []
	imgs = {}
	for i in rlinks:
		link = i[5:-1]
		links.append(link)
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
			if size < 5:
				os.remove(imgs[key])
			else:
				am +=1
		except IOError:
			continue

def main():
	url, urltype = 'http://cnn.com', 'url' # URL (or Instagram/Tumblr username) and URL type, leave as is if not a 'tumblr' or 'instagram'.
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
