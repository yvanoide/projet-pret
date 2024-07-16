import streamlit as st
import requests

class TraducteurApp:
    def __init__(self):
        self.URL_TRADUCTEUR = "http://127.0.0.1:8080/traductions"
        self.URL_VERSIONS = "http://127.0.0.1:8080/versions"
        self.URL_LOGIN = "http://127.0.0.1:8080/login"
        self.URL_TRADUCTIONS = "http://127.0.0.1:8080/traductions/auteur/"
        self.titre = "Traducteur"

        st.set_page_config(
            page_title="Traducteur",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded",
        )

        if "logged_in" not in st.session_state:
            st.session_state["logged_in"] = None

        self.show_login_form()
        if st.session_state["logged_in"]:
            self.show_app()
        else:
            self.show_index()

    def show_login_form(self):
        def login(username, password):
            data = {
                "login": username,
                "mdp": password
            }
            response = requests.post(self.URL_LOGIN, json=data)
            if response.status_code == 200:
                response_login = response.json()
                if response_login["authentifié"]:
                    st.session_state["logged_in"] = response_login["id"]
            if not st.session_state["logged_in"]:
                st.sidebar.error("Nom d'utilisateur ou mot de passe incorrect")

        st.sidebar.title("Connexion")
        
        # Vérifier si l'utilisateur est connecté pour afficher le bouton de déconnexion
        if st.session_state["logged_in"]:
            self.show_logout_button()
        else:
            username = st.sidebar.text_input("Nom d'utilisateur")
            password = st.sidebar.text_input("Mot de passe", type="password")
            st.sidebar.button("Se connecter", on_click=login, args=(username, password))

    def show_logout_button(self):
        def logout():
            st.session_state["logged_in"] = None
            # Réinitialisation des états ou actions nécessaires lors de la déconnexion
            # Par exemple, effacer des éléments de session ou réinitialiser des variables

            # Afficher un message de confirmation ou rediriger vers la page de connexion
            st.sidebar.success("Vous avez été déconnecté avec succès.")
            # Rediriger automatiquement vers la page d'index après la déconnexion
            self.show_index()

        st.sidebar.title("Déconnexion")
        st.sidebar.button("Se déconnecter", on_click=logout)

    def show_index(self):
        st.title(self.titre)
        if not st.session_state["logged_in"]:
            st.write("Veuillez vous connecter pour accéder aux fonctionnalités sécurisées.")

    def show_app(self):
        st.title(self.titre)
        versions = self.get_versions()
        option = st.sidebar.selectbox("Choisissez la traduction à réaliser :", versions)
        self.add_form(option)
        self.add_chat()

    def get_versions(self):
        response = requests.get(self.URL_VERSIONS)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur : {response.status_code}")
            return ["Aucune langue détectée !"]

    def add_form(self, option):
        st.subheader(option)
        atraduire = st.text_input("Texte à traduire")

        if st.button("Traduire"):
            if st.session_state["logged_in"] is not None:
                try:
                    utilisateur_id = int(st.session_state["logged_in"])
                except ValueError:
                    st.error("Identifiant utilisateur invalide")
                    return

                data = {
                    "atraduire": atraduire,
                    "version": option,
                    "utilisateur": utilisateur_id
                }
                response = requests.post(self.URL_TRADUCTEUR, json=data)
                if response.status_code == 200:
                    st.success("Voici votre traduction !")
                    response_data = response.json()
                    reponse = f"{response_data['traduction'][0]['translation_text']}"
                    st.write(reponse)
                else:
                    st.error(f"Erreur : {response.status_code}")
                    st.json(response.json())
            else:
                st.error("Veuillez vous connecter avant de traduire.")

    def add_chat(self):
        if st.session_state["logged_in"]:
            url = f"{self.URL_TRADUCTIONS}{st.session_state['logged_in']}"
            response = requests.get(url)
            if response.status_code == 200:
                chat_messages = response.json()
                for prompt in chat_messages:
                    st.write(f"Utilisateur : {prompt['atraduire']}")
                    st.write(f"Traduction : {prompt['traduction']}")
            else:
                st.error(f"Erreur : {response.status_code}")

if __name__ == "__main__":
    TraducteurApp()
