import bs4    #parser HTML
import requests		#rend l’intégration avec des webservices très facile
import os    #utiliser les fonctionnalités dépendantes du système d'exploitation
import sys	
import re	#opérations sur les expressions rationnelles
from io import BytesIO
from PIL import Image

def getImages(urlEpisode, currentChap):	#defintion de la fonction qui permet de recuperer l'image
	while urlEpisode:		
		data = requests.get(urlEpisode)		#Recuperation de l'URL de l'episode
		base = bs4.BeautifulSoup(data.text, 'html.parser')
		try:
			img = base.select_one("img[id='img']").get('src')
			print(f"Downloading {urlEpisode}")
			res = requests.get(img)
			imgFile = Image.open(BytesIO(res.content))
			imgFile.save(os.path.basename(urlEpisode)+'.jpg')
		except Exception as e:
			print("Telechargement impossible")

		nextUrl  = base.select_one("div[id='imgholder'] a").get('href')	#URL de l'episode suivant 
		if int(nextUrl.split("/")[2]) != currentChap:
			break
		urlEpisode =f"{baseUrl+nextUrl}"

		
def downloadManga(nom, parametres):			#defintion de la fonction qui indique comment telecharger l'image
	sep = "".join(re.findall(r"[-,]", parametres))
	parametres = re.split(r"[-,]",sys.argv[2])
	parametres = list(map(int, parametres))
	url = f"{baseUrl}/{nom}"		#Nouveau URL de la page
	if len(parametres)==2:
		if sep == '-':			#Cas dans lequel nous avons -
			debut, fin = parametres[0], parametres[1]+1
			for i in range(debut, fin):
				urlEpisode = f"{url}/{i}/1"
				if not os.path.exists(f"Chapitre{i}"):
					try:
						os.mkdir(f"Chapitre{i}")
					except :
						print(f"Creation Impossible le dossier du chapitre{i}")
						sys.exit()

				os.chdir(f"Chapitre{i}")
				getImages(urlEpisode, i)  #Appel de lafonction getImage
				os.chdir("..")
				

		elif sep == ',':		#Cas dans lequel nous avons ,
			for i in parametres:
				urlEpisode = f"{url}/{i}/1"
				if not os.path.exists(f"Chapitre{i}"):
					try:
						os.mkdir(f"Chapitre{i}")
					except :
						print(f"Creation Impossible le dossier du chapitre{i}")
						sys.exit()
						
				os.chdir(f"Chapitre{i}")
				getImages(urlEpisode, i)
				os.chdir("..")

	elif len(parametres) == 1:		#Cas dans lequel nous avons un seul parametre 
		chap = parametres[0]
		if not os.path.exists(f"Chapitre{chap}"):
			try:
				os.mkdir(f"Chapitre{chap}")
			except :
				print(f"Creation Impossible le dossier du chapitre{i}")
				sys.exit()
						
		os.chdir(f"Chapitre{chap}")
		urlEpisode = f"{url}/{chap}/1"
		getImages(urlEpisode, chap)
	print("Download Completed")
if __name__ == "__main__": #Page d'acceuil
	nom = sys.argv[1]
	chapiters = sys.argv[2]
	baseUrl = "http://www.mangapanda.com"
	os.chdir("/home/junior/Bureau/Projet")

	if not os.path.exists(nom):
		try:
			os.mkdir(nom)
		except :
			print(f"Creation Impossible le dossier du chapitre{i}")
			sys.exit()

	os.chdir(nom)
	downloadManga(nom, chapiters)
