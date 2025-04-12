import streamlit as st # type: ignore
import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore

# Streamlit UI
st.title("Générateur de citation de site web 📚")
st.write("Entrez l'URL d'un site et obtenez la référence bibliographique formatée en français.")

# URL input box
url = st.text_input("🔗 Entrez l'URL du site:")

if url:
    try:
        # Fetch and parse the site
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract metadata (try to find author)
        author = ""
        if soup.find("meta", attrs={"name": "author"}):
            author = soup.find("meta", attrs={"name": "author"})["content"]
        elif soup.find("meta", attrs={"property": "article:author"}):
            author = soup.find("meta", attrs={"property": "article:author"})["content"]

        # Try to split author name
        if author:
            parts = author.strip().split()
            last_name = parts[-1].upper()
            first_name = " ".join(parts[:-1]).capitalize()
            author_formatted = f"{last_name}, {first_name}."
        else:
            author_formatted = "AUTEUR INCONNU, ."

        # Organization (site name)
        org = soup.find("meta", property="og:site_name")
        org = org["content"] if org else "Organisation inconnue"

        # Title of the page
        title = soup.title.string.strip() if soup.title else "Titre inconnu"

        # Final formatted citation
        citation = f"{author_formatted} {org}, *{title} [en ligne]*, {url}"

        st.subheader("📄 Citation générée :")
        st.write(citation)

    except Exception as e:
        st.error(f"Erreur lors du traitement de l'URL : {e}")
