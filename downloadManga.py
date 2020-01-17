import bs4
import requests
import os
import sys
import re
from io import BytesIO
from PIL import Image

def getImages(urlEpisode, curChap):
	while urlEpisode:		
		data = requests.get(urlEpisode)
		base = bs4.BeautifulSoup(data.text, 'html.parser')
		try:
			img = base.select_one("img[id='img']").get('src')
			print(f"Downloading {urlEpisode}")
			res = requests.get(img)
			imgFile = Image.open(BytesIO(res.content))
			imgFile.save(os.path.basename(urlEpisode)+'.jpg')
		except Exception as e:
			print("Impossible de telecharger cettte image")

		nextUrl  = base.select_one("div[id='imgholder'] a").get('href')
		if int(nextUrl.split("/")[2]) != curChap:
			break
		urlEpisode =f"{baseUrl+nextUrl}"


def downloadManga(nom, params):
	sep = "".join(re.findall(r"[-,]", params))
	params = re.split(r"[-,]",sys.argv[2])
	params = list(map(int, params))
	url = f"{baseUrl}/{nom}"
	if len(params)==2:
		if sep == '-':
			debut, fin = params[0], params[1]+1
			for i in range(debut, fin):
				urlEpisode = f"{url}/{i}/1"
				if not os.path.exists(f"Chapitre{i}"):
					try:
						os.mkdir(f"Chapitre{i}")
					except :
						print(f"Impossible de cree le dossier du chapitre{i}")
						sys.exit()

				os.chdir(f"Chapitre{i}")
				getImages(urlEpisode, i)
				os.chdir("..")
				

		elif sep == ',':
			for i in params:
				urlEpisode = f"{url}/{i}/1"
				if not os.path.exists(f"Chapitre{i}"):
					try:
						os.mkdir(f"Chapitre{i}")
					except :
						print(f"Impossible de cree le dossier du chapitre{i}")
						sys.exit()
						
				os.chdir(f"Chapitre{i}")
				getImages(urlEpisode, i)
				os.chdir("..")

	elif len(params) == 1:
		chap = params[0]
		if not os.path.exists(f"Chapitre{chap}"):
			try:
				os.mkdir(f"Chapitre{chap}")
			except :
				print(f"Impossible de cree le dossier du chapitre{i}")
				sys.exit()
						
		os.chdir(f"Chapitre{chap}")
		urlEpisode = f"{url}/{chap}/1"
		getImages(urlEpisode, chap)
	print("Download Completed")
if __name__ == "__main__":
	nom = sys.argv[1]
	chapiters = sys.argv[2]
	baseUrl = "http://www.mangapanda.com"
	os.chdir("/home/junior/Bureau/Projet")

	if not os.path.exists(nom):
		try:
			os.mkdir(nom)
		except :
			print(f"Impossible de cree le dossier du chapitre{i}")
			sys.exit()

	os.chdir(nom)
	downloadManga(nom, chapiters)
