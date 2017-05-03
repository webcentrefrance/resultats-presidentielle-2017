#!/usr/bin/python
from lxml import etree
import unicodecsv as csv

departements = ["03", "15", "43", "63"]
ficsv = open('pr017_auvergne.csv', 'w')

try:
	majcsv = csv.DictWriter(ficsv, ['code insee', 'ville', 'inscrits', 'votants', 'exprimes', 'abstentions', 'blancs', 'nuls', 'MACRON', 'ARTHAUD', 'FILLON','CHEMINADE', 'LE PEN', u'M\xc9LENCHON', 'POUTOU', 'DUPONT-AIGNAN', 'LASSALLE', 'ASSELINEAU', 'HAMON'])
	majcsv.writeheader()
	for departement in departements:
		arbre = etree.parse("http://elections.interieur.gouv.fr/telechargements/PR2017/resultatsT1/084/0"+departement+"/0"+departement+"com.xml")
		print ("Departement numero "+departement)
		for noeud in arbre.xpath("//Election/Departement/Communes/Commune"):
			objet = {}
			for insee in noeud.xpath("CodSubCom"):
				objet["code insee"] = departement+insee.text
			for commune in noeud.xpath("LibSubCom"):
				objet["ville"] = commune.text
			for resultats in noeud.xpath("Tours/Tour[NumTour=1]"):
				for inscrits in resultats.xpath("Mentions/Inscrits/Nombre"):
					objet["inscrits"] = int(inscrits.text)
				for abstentions in resultats.xpath("Mentions/Abstentions/Nombre"):
					objet["abstentions"] = int(abstentions.text)
				for votants in resultats.xpath("Mentions/Votants/Nombre"):
					objet["votants"] = int(votants.text)
				for blancs in resultats.xpath("Mentions/Blancs/Nombre"):
					objet["blancs"] = int(blancs.text)
				for nuls in resultats.xpath("Mentions/Nuls/Nombre"):
					objet["nuls"] = int(nuls.text)
				for exprimes in resultats.xpath("Mentions/Exprimes/Nombre"):
					objet["exprimes"] = int(exprimes.text)
				for liste in resultats.xpath("Resultats/Candidats/Candidat"):
					nu = ""
					vox = 0
					for nuance in liste.xpath("NomPsn"):
						nu = nuance.text
					for voix in liste.xpath("RapportExprime"):
						vox = voix.text.strip()
					objet[nu] = vox
				#print(objet)
				majcsv.writerow(objet)
finally:
	ficsv.close()