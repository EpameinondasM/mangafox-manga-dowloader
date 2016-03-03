#!python35

#Download manga from mangafox script
#By Mataragkas Epameinondas "notis.sephiroth@yahoo.gr"

import requests, os, bs4, threading,re,sys
import windowsuser



file_location = windowsuser.expand_user() + '\\' + "Desktop" + "\\" + "manga"

print (file_location)


manga = input("What manga you want to download?\n")
manga = re.sub('[^a-zA-Z0-9\n\.]', '_', manga) # Changes all special characters to " "
startChapter = int(input("Select starting Chapter\n"))
endChapter = int(input("Select ending Chapter\n"))
manga_url = 'http://mangafox.me/manga/{0}'.format(manga)



print (manga_url)
os.makedirs(file_location, exist_ok = True) #Creates a file to store the manga images at -> file_location



#next page
def next(comicElem):

	res = requests.get(comicElem)
	res.raise_for_status
	soup = bs4.BeautifulSoup(res.text, "html.parser")
	
	temp = [] #list created to not corrupt the "next" list
	next = [] #list that will be used as the next page link
	while(len(temp) < 8 ):	#manga links that are inside temp can go up to 7 until they find the comment page that is larger and is the end of the manga pages
	
		for link in soup.select('a.btn.next_page'):	#searches the page for the "href" inside the "a.btn.next_page" class that contains the next page link 
			temp = link.get('href') # parses the "href" into temp list
			print (len(temp))
			
			if (len(temp) < 8):
				x = len(comicElem) - 7 # starting point for temp 
				next = comicElem[:x] + "/" + temp
				print ("next is",next)
				
			res = requests.get(next)
			res.raise_for_status
			soup = bs4.BeautifulSoup(res.text, "html.parser")

			manga_page = manga_image(next) #Sends the next manga page link so that the functions find the new page image

			break #For some reason this "for" was executed twice with the same values so have to break the second time
			
#url of manga image
def manga_image(comicElem):

	res = requests.get(comicElem)
	res.raise_for_status
	soup = bs4.BeautifulSoup(res.text, "html.parser")
	
	temp = soup.select('img#image')
	manga_page = temp[0].get('src')
	save_image(manga_page)
	
	print (manga_page)
	return manga_page
	
# Save the image to C:\Users\XXXX\Desktop\manga
def save_image(manga_page):

	res = requests.get(manga_page)
	res.raise_for_status
	
	imageFile = open(os.path.join(file_location, "one_" + os.path.basename(manga_page)), 'wb')
	
	for chunk in res.iter_content(1):
		imageFile.write(chunk)
	imageFile.close()

#Downloads manga by chapters that the user inputs
def download_manga_chapter(manga_url,startChapter,endChapter):

	#Downloads the manga page.
	print('Downloading page %s...' % manga_url)
	res = requests.get(manga_url)
	res.raise_for_status
	soup = bs4.BeautifulSoup(res.text, "html.parser")
	
	
	
	#Finds the URL of the manga chapter
	while startChapter <= endChapter: #loop starts at the value of the first manga chapter provided by the user and runs untill the final manga chapter
		if startChapter < 100 and startChapter >= 10:	#mangafox chapter naming works like this : http://mangafox.me/manga/manga_name/cXXX/Y.html XXX stands for the number of manga chapter with 001 being first chapter and Y stands for the number of manga page
			comicElem = manga_url + "/c0" + str(startChapter) + "/1.html" 
		elif startChapter < 10:
			comicElem = manga_url + "/c00" + str(startChapter) + "/1.html"
		else:
			comicElem = manga_url + "/c" + str(startChapter) + "/1.html"
		print ("manga url",comicElem)
		#Find the URL of each page
		print('Downloading image %s...' % (comicElem))
		#downloads the first page of the startChapter
		manga_page = manga_image(comicElem) 
		#proceeds with the next pages of the manga
		next(comicElem)
		#increments the chapter by 1
		startChapter += 1
		
		
#Downloads the entire manga
def download_manga(manga_url):
	#Download the page.
	print('Downloading page %s...' % manga_url)
	res = requests.get(manga_url)
	res.raise_for_status
	soup = bs4.BeautifulSoup(res.text, "html.parser")
	
	#Downloads chapter by chapter starting from last and ending with first
	for link in soup.select('a.tips'):
		comicElem = link.get('href')
		manga_page = manga_image(comicElem)
		next(comicElem)
	

		
		






