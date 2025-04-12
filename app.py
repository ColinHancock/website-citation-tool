import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore

url = input("Colle l'URL de l'article : ")

# Téléchargement de la page
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Titre
title = soup.title.string.strip() if soup.title else "Titre non trouvé"

# Auteur
author = "Auteur non trouvé"
author_tag = soup.find("meta", attrs={"name": "author"})
if author_tag:
    raw_author = author_tag.get("content", author)
    # Séparer prénom et nom
    parts = raw_author.strip().split()
    if len(parts) >= 2:
        last_name = parts[-1].upper()
        first_name = " ".join(parts[:-1]).lower()
        author = f"{last_name}, {first_name}"
    else:
        author = raw_author

# Organisme / site name
organization = "Organisme non trouvé"
org_tag = soup.find("meta", attrs={"property": "og:site_name"})
if org_tag:
    organization = org_tag.get("content", organization)

# Affichage
print("\n--- Citation en français ---")
print(f"{author}. {organization}, \x1B[3m{title} [en ligne]\x1B[0m, {url}")
