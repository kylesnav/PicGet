import urllib, re, os


def geturl():
	url = raw_input('Enter a url: ')
	rurl = raw_input('Album title (your choice): ')
	if url[0:7] != 'http://':
		url = 'http://' + url
	print url + ' is being saved as: ' + rurl
	return url, rurl


def gethtml(url):
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
	return imgs


def finddir(rurl):
	act = ' '
	os.chdir('/Users')
	print '\n\nYou are currently in %s' % os.getcwd()
	print '\nThe current sub-directories are: %s' % os.listdir('.')
	act = raw_input('\nIf this is the proper directory press enter, or type the name of the desired directory. ')
	while act != '':
		os.chdir(act)
		print '\n\nYou are now currently in %s' % os.getcwd()
		print '\nThe current sub-directories are: %s' % os.listdir('.')
		act = raw_input('\nIf this is the proper directory press enter, or type the name of the desired directory. ')
	os.mkdir(rurl)
	os.chdir(rurl)
	return


def getimgs(imgs):
	for key in imgs.iterkeys():
		urllib.urlretrieve(key, imgs[key])
		stat = os.stat(imgs[key])
		size = stat.st_size / 1000
		if size < 5:
			os.remove(imgs[key])
	print 'Success!'


def main():
	url, rurl = geturl()
	html = gethtml(url)
	imgs = getlinks(html)
	finddir(rurl)
	getimgs(imgs)


if __name__ == '__main__':
	main()