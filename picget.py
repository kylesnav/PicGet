import urllib, re, os


def geturl():
	url = raw_input('\n\nEnter a url or an Instagram username (@example) or a tumblr username (example): ')
	rurl = raw_input('\nAlbum title (your choice): ')
	if (url[-11:] == '.tumblr.com' or '.tumblr.com' in url) and (url[-14:-11] != 'www'):
		turl = 'tumblr'
	elif '.com' not in url and url[0] != '@':
		turl = 'tumblr'
		print '\nFinding '+ url +'\'s, tumblr this may take a while. \n'
		return url, rurl, turl
	elif url[0] == '@':
		turl = 'instagram'
		print '\nFinding '+ url +'\'s, Instagram this may take a while. \n'
		return url, rurl, turl
	else:
		turl = 'url'
	if url[0:7] != 'http://' and turl != 'instagram':
		url = 'http://' + url
	print '\n' + url + ' is will be saved as: ' + rurl
	print '\nFinding '+ url +', this may take a while. \n'
	return url, rurl, turl


def gethtml(url):
	rhtml = urllib.urlopen(url)
	rhtml = rhtml.read()
	html = ''
	for i in rhtml:
		html += i
	return html


def tumblrhtml(url):
	name = url
	if '.tumblr.com' not in url:
		url = 'http://' + url + '.tumblr.com'
	if url[-1] != '/':
		url = url + '/page/'
	else:
		url = url + 'page/'
	x = 0
	fhtml = ''
	while x >= 0:
		rhtml = urllib.urlopen(url + str(x + 1))
		rhtml = rhtml.read()
		html = ''
		for i in rhtml:
			html += i
		fhtml += html
		if '"post-body' not in html: break
		else: x += 1
	html = fhtml
	print str(x), 'pages of images being saved from:', name + '\n'
	return html


def instagramhtml(url):
		name = url
		url = 'http://web.stagram.com/n/' + url[1:] + '/'
		rhtml = urllib.urlopen(url)
		rhtml = rhtml.read()
		nhtml = ''
		html = ''
		for i in rhtml:
			html += i
			nhtml += i
		next = re.findall('<a href="/n/.+/.+" rel="next">Earlier</a>', nhtml)
		x = 1
		while len(next) == 1: 
			x += 1
			page = next[0]
			page = 'http://web.stagram.com' + page[9:-24]
			rhtml = urllib.urlopen(page)
			rhtml = rhtml.read()
			nhtml = ''
			for i in rhtml:
				nhtml += i
				html += i
			next = re.findall('<a href="/n/.+/.+" rel="next">Earlier</a>', nhtml) 
		print str(x), 'pages of images being saved from:', name + '\'s instagram.\n'
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
	print 'You are currently in %s' % os.getcwd()
	print '\nThe current sub-directories are: %s' % os.listdir('.')
	act = raw_input('\nPress enter, or type the name of the desired directory. ')
	while act != '':
		os.chdir(act)
		print '\nYou are now currently in %s' % os.getcwd()
		print '\nThe current sub-directories are: %s' % os.listdir('.')
		act = raw_input('\nPress enter, or type the name of the desired directory. ')
	os.mkdir(rurl)
	os.chdir(rurl)
	return


def getimgs(imgs):
	print '\nDownloading images, this may take a while. \n'
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
	print 'Success, found ' + str(am) + ' image(s)!\n'


def main():
	url, rurl, turl = geturl()
	if turl == 'tumblr': html = tumblrhtml(url)
	elif turl == 'instagram': html = instagramhtml(url)
	else: html = gethtml(url)
	imgs = getlinks(html)
	finddir(rurl)
	getimgs(imgs)


if __name__ == '__main__':
	main()
