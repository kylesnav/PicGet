import urllib, re, os


def geturl():
	url = raw_input('\n\nEnter a url (all pages of a Tumblr are saved): ')
	rurl = raw_input('\nAlbum title (your choice): ')
	if url[0:7] != 'http://':
		url = 'http://' + url
	print '\n' + url + ' is will be saved as: ' + rurl
	print '\nFinding '+ url +', this may take a while. \n'
	return url, rurl


def gethtml(url):
	#tumblr
	if url[-11:] == '.tumblr.com':
		name = url
		url = url + '/page/'
		x = 0
		fhtml = ''
		while x >= 0:
			x += 1
			rhtml = urllib.urlopen(url + str(x))
			rhtml = rhtml.read()
			html = ''
			for i in rhtml:
				html += i
			fhtml += html
			if '"post-body' not in html:
				break
		html = fhtml
		print str(x), 'pages of images being saved from:', name + '\n'
	#not tumblr
	else:
		rhtml = urllib.urlopen(url)
		rhtml = rhtml.read()
		html = ''
		for i in rhtml:
			html += i
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
	print 'Found ' + str(len(links)) + ' potential image(s).\n'
	return imgs


def finddir(rurl):
	act = ' '
	os.chdir('/Users')
	print 'You are currently in %s' % os.getcwd()
	print '\nThe current sub-directories are: %s' % os.listdir('.')
	act = raw_input('\nPress enter, or type the name of the desired directory. ')
	while act != '':
		os.chdir(act)
		print '\n\nYou are now currently in %s' % os.getcwd()
		print '\nThe current sub-directories are: %s' % os.listdir('.')
		act = raw_input('\nPress enter, or type the name of the desired directory. ')
	os.mkdir(rurl)
	os.chdir(rurl)
	return


def getimgs(imgs):
	print '\nDownloading images, this may take a while. \n'
	am = 0
	for key in imgs.iterkeys():
		urllib.urlretrieve(key, imgs[key])
		stat = os.stat(imgs[key])
		size = stat.st_size / 1000
		if size < 5:
			os.remove(imgs[key])
		else:
			am +=1
	print '\nSuccess, found ' + str(am) + ' image(s)!\n'

def main():
	url, rurl = geturl()
	html = gethtml(url)
	imgs = getlinks(html)
	finddir(rurl)
	getimgs(imgs)


if __name__ == '__main__':
	main()