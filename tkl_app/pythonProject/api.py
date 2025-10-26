import requests
import os
import asyncio
import httpx
from kivy.storage.jsonstore import JsonStore

img_url='https://res.cloudinary.com/dznrirg5t/'

#connexion

'''def logout():
    try:
        response = requests.post(logout_url)
        response.raise_for_status()
        token = response.json()
        store.put("tokens",
                  access=token["access"],
                  refresh=token["refresh"])
        tokens=store.get("tokens")
        user_id=get_id(email)
        if user_id:
            store.put("user", id=user_id["id"],email=email,profile=user_id["profile"], connected=True)
        else:
            return False
        me=store.get("user")
        print("connexion reussie")
    except requests.RequestException as e:
        print("erreur login: ",e)
'''
##############################
#           Client           #
##############################


#[{'id': 1, 'menus': [{'id': 1, 'plats': [{'id': 1, 'plat': None, 'prix': 1500}, {'id': 2, 'plat': None, 'prix': 1000}], 'jour': 'lundi', 'menu_hebdo': 1}, {'id': 2, 'plats': [{'id': 3, 'plat': None, 'prix': 1500}, {'id': 4, 'plat': None, 'prix': 1000}], 'jour': 'mardi', 'menu_hebdo': 1}, {'id': 3, 'plats': [{'id': 5, 'plat': None, 'prix': 1000}], 'jour': 'mercredi', 'menu_hebdo': 1}], 'restaurant': {'id': 1, 'nom': 'fpka foods', 'type_plat': 'africaine', 'code': '', 'menu_hebdo': 1, 'quartier': 'logbessu', 'user': {'id': 1, 'username': 'Fotie', 'email': 'kieranarol@gmail.com', 'tel': 658308288, 'profile': 'client'}, 'livreurs': []}}]

#----------------------------------Commande
'''
add command data
data={
    "position":{"latitude":4.0511,"longitude":9.7679,"nom":"Douala"},
    "prix_total":18000,
    "jour":0,
    "mois":0,
    "annee":0,
    "commande_plat_set":
        [
    {"plat_commander":1,"quantite":10,"prix_total":15000},
    {"plat_commander":5,"quantite":3,"prix_total":3000},
],
    }'''
#data===> om,momo,position=>[{nom,longitude,latitude}],promo_time
class Data:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        data_json = os.path.join(self.base_dir, "data.json")
        self.store = JsonStore(data_json)
        if self.store.exists("paiement") and self.store.exists("positions") and self.store.exists("commande"):
            self.paid = self.store.get("paiement")
            self.position=self.store.get("positions")
            self.command=self.store.get("commande")
        else:
            self.create()

    def create(self):
        self.store.put("paiement", momo="aucun", om="aucun")
        self.store.put("positions", data=[])
        self.store.put("commande",position={},prix_total=0,data={})# data==>{"restaurant":{"id":id,"frais de livraison":0,"command":[]}
        self.paid = self.store.get("paiement")
        self.position = self.store.get("positions")
        self.command = self.store.get("commande")

    def update_paid(self,om,momo):
        if self.store.exists("paiement"):
            self.store.put("paiement", momo=momo, om=om)
            self.paid = self.store.get("paiement")

    def add_place(self,place):
        if self.store.exists("positions"):
            data=self.position["data"]
            data.append(place)
            self.store.put("positions", data=data)
            self.position = self.store.get("positions")

    def add_prix_total(self,value):
        if self.store.exists("commande"):
            prix=int(self.command["prix_total"])+value
            self.store.put("commande", **{**self.store.get("commande"), "prix_total": prix})
            self.command = self.store.get("commande")

    def reduce_prix_total(self,value):
        if self.store.exists("commande"):
            prix=int(self.command["prix_total"])-value
            self.store.put("commande", **{**self.store.get("commande"), "prix_total": prix})
            self.command = self.store.get("commande")

    def add_command(self,restau,id_restau,livraison,data):
        if self.store.exists("commande"):
            old_data = self.command["data"]
            if restau in old_data:
                old_data[restau]["command"].append(data)
            else:
                old_data[restau]["id"]=id_restau
                old_data[restau]["livraison"]=livraison
                self.add_prix_total(livraison)
                old_data[restau]["command"].append(data)
            self.store.put("commande", **{**self.store.get("commande"), "data": old_data})
            self.command = self.store.get("commande")

    def delete_command(self,restau,livraison,data):
        if self.store.exists("commande"):
            old_data = self.command["data"]
            if restau in old_data and old_data[restau]["command"]:
                i=old_data[restau]["command"].index(data)
                old_data[restau]["command"].pop(i)
            else:
                del old_data[restau]["command"]
                self.reduce_prix_total(livraison)

            self.store.put("commande", **{**self.store.get("commande"), "data": old_data})
            self.command = self.store.get("commande")




class UserApi:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/"
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        auth_json = os.path.join(self.base_dir, "auth.json")
        self.data=Data()
        self.store = JsonStore(auth_json)

        if self.store.exists("user"):
            self.me = self.store.get("user")
        else:
            self.me = {}
        if "connected" in self.me.keys():
            self.connected = True
        else:
            self.connected = False
        self.restaurant = None
        self.boutique = None
        if self.store.exists("tokens"):
            self.tokens = self.store.get("tokens")
        else:
            self.tokens = {}
        self.my_info={}
        self.token_url = f"{self.base_url}token/"
        self.refresh_url = f"{self.base_url}token/refresh/"
        self.logout_url = f"{self.base_url}logout/"

        self.get_my_info()

    def get_id(self,email):
        endpoint = f"{self.base_url}utilisateur/r/?profile=&email={email}&code="
        headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
        try:

            response = requests.get(url=endpoint, headers=headers)
            if self.auto_refresh(response.status_code):
                headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
                response = requests.get(url=endpoint, headers=headers)
            return response.json()
        except requests.RequestException as e:
            print("erreur refresh: ", e)
            return None

    async def login_client(self,email, password):
        data = {"email": email, "password": password}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.post(self.token_url, json=data)
                response.raise_for_status()
                token = response.json()
                self.store.put("tokens",
                          access=token["access"],
                          refresh=token["refresh"])
                self.tokens = self.store.get("tokens")
                user_id = self.get_id(email)[0]
                if user_id:
                    print("user", user_id)
                    self.store.put("user", id=user_id["id"], email=email, profile=user_id["profile"], connected=True)
                else:
                    return False
                me = {}
                me = self.store.get("user")
                return "connexion reussie"
        except httpx.RequestError as e:
            return f"erreur de connexion: {e}"

    def refresh_access(self):
        try:
            response = requests.post(self.refresh_url, json={"refresh": self.tokens["refresh"]})
            response.raise_for_status()
            data = response.json()
            self.store.put("tokens",
                      access=data["access"],
                      refresh=self.tokens["refresh"])
        except httpx.RequestError as e:
            print("erreur refresh: ", e)

    # generer et rafraichir automatique
    def auto_refresh(self,statut):

        if statut == 401:
            print("access expiré tentative de rafraichissement")
            self.refresh_access()
            return True

    # -----------------------Authentification
    def get_my_info(self):
        endpoint = f"{self.base_url}utilisateur/{self.me["id"]}"
        headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
        print("inside")
        try:
            response = requests.get(url=endpoint, headers=headers)
            print(response.json())
            if self.auto_refresh(response.status_code):
                headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
                response = requests.get(url=endpoint, headers=headers)
            self.my_info=response.json()
            return True
        except requests.RequestException as e:
            print("erreur get_my_info: ", e)
            return None


    async def sign_client(self,data):  # data={ username,tel,email,password}
        url = f"{self.base_url}utilisateur/"
        data["profile"] = "client"
        data["code"] = ""
        data["a_restaurant"] = False
        data["a_boutique"] = False
        data["logo"] = None
        data["quartier"] = ""

        try:
            print(data)
            async with (httpx.AsyncClient() as client):
                response = await client.post(url=url, json=data)
                print(response.status_code)
                user = response.json()
                print("connecté")
                self.store.put("user", id=user["id"],username=user["username"], email=user["email"], profile="client", connected=True)
                self.me = self.store.get("user")
                return "inscription avec succes"
        except requests.RequestException as e:
            return ("erreur d'inscription: ", e)

    async def update_my_info(self,data):  # data={ info to change (username,tel)}
        endpoint = f"{self.base_url}utilisateur/{self.me["id"]}/"
        print(endpoint)
        headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.patch(url=endpoint, headers=headers, json=data)
                if self.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
                    response = await client.patch(url=endpoint, headers=headers, json=data)
                return response.json()
        except requests.RequestException as e:
            print("erreur update_my_info: ", e)

    # ----------------------------Exploration des restaurants et plats
    async def recupérer_les_type_plat(self):
        endpoint = f"{self.base_url}types-plats/"
        headers = {"Authorization": f"Bearer{self.tokens["access"]}"}

        try:
            async with (httpx.AsyncClient() as client):
                response = await client.get(url=endpoint, headers=headers)
                if self.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
                    response = await client.get(url=endpoint, headers=headers)
                return response.json()
        except requests.RequestException as e:
            print("erreur recupérer_les_type_plat: ", e)
            return None

    async def filtre_restaurant(self,type_plat="",rate="",open=None):

        endpoint = f"{self.base_url}restaurant/?type_plat={type_plat}&rate={rate}&est_ouvert={open}&user="
        headers = {"Authorization": f"Bearer{self.tokens["access"]}"}

        try:
            async with (httpx.AsyncClient() as client):
                response = await client.get(url=endpoint, headers=headers)
                if self.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
                    response = await client.get(url=endpoint, headers=headers)
                return response.json()
        except requests.RequestException as e:
            print("erreur filtre_restaurant: ", e)
            return None

    # [{'id': 1, 'nom': 'fpka foods', 'type_plat': 'africaine', 'code': '', 'menu_hebdo': 1, 'quartier': 'logbessu', 'user': {'id': 1, 'username': 'Fotie', 'email': 'kieranarol@gmail.com', 'tel': 658308288, 'profile': 'client'}, 'livreurs': []}, {'id': 2, 'nom': 'kmc', 'type_plat': 'fast-food', 'code': 'tIRTeIMPoD', 'menu_hebdo': None, 'quartier': 'bonamoussadi', 'user': {'id': 2, 'username': 'kmc-Bonamoussadi', 'email': 'kmc@gmail.com', 'tel': 655784123, 'profile': 'restaurant'}, 'livreurs': []}]

    # Recherche d'un restaurant par nom
    async def rechercher_restaurant(self,recherche=""):
        endpoint = f"{self.base_url}restaurant/?search={recherche}"
        headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.get(url=endpoint, headers=headers)
                if self.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
                    response = requests.get(url=endpoint, headers=headers)
                return response.json()
        except httpx.RequestError as e:
            print("erreur rechercher_restaurant: ", e)
            return None

    async def rechercher_boutique(self,recherche=""):
        endpoint = f"{self.base_url}boutique/?search={recherche}"
        headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.get(url=endpoint, headers=headers)
                if self.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
                    response = requests.get(url=endpoint, headers=headers)
                return response.json()
        except httpx.RequestError as e:
            print("erreur rechercher_restaurant: ", e)
            return None

    # Recherche d'un plat dans le menu du jour
    async def rechercher_plat(self,nom=""):
        endpoint1 = f"{self.base_url}today/?search={nom}"
        endpoint2 = f"{self.base_url}menu_static_plat/?search={nom}"
        headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
        try:
            async with (httpx.AsyncClient() as client):
                response1 = await client.get(url=endpoint1, headers=headers)
                response2 = await client.get(url=endpoint2, headers=headers)
                if self.auto_refresh(response1.status_code) or self.auto_refresh(response2.status_code):
                    headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
                    response1 = await client.get(url=endpoint1, headers=headers)
                    response2 = await client.get(url=endpoint2, headers=headers)
                print(response1.status_code)
                print(response1.json())
                data1=response1.json()
                data2=response2.json()
                response=self.combine(data1,data2)
                return response
        except httpx.RequestError as e:
            print("erreur rechercher_plat: ", e)
            return None

    async def rechercher_produit(self,recherche=""):
        endpoint = f"{self.base_url}produit/?search={recherche}"
        headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.get(url=endpoint, headers=headers)
                if self.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
                    response = requests.get(url=endpoint, headers=headers)
                return response.json()
        except httpx.RequestError as e:
            print("erreur rechercher_restaurant: ", e)
            return None



    def combine(self,list1,list2):
        combined=[]
        while list1 or list2:
            print(list1)
            if list1:
                combined.append(list1.pop(0))
            print(list2)
            if list2:
                combined.append(list2.pop(0))
        combined.sort(key=lambda x: -x["prix"])
        return combined
    # recuperer le menu d'aujourd'hui et des autres jours pour un restaurant

    async def avoir_restaurant(self,restaurant_id=""):
        endpoint = f"{self.base_url}restaurant/{restaurant_id}/"
        headers = {"Authorization": f"Bearer{self.tokens["access"]}"}

        try:
            async with (httpx.AsyncClient() as client):
                response = await client.get(url=endpoint, headers=headers)
                if self.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
                    response = await client.get(url=endpoint, headers=headers)
                return response.json()
        except httpx.RequestError as e:
            print("erreur refresh: ", e)
            return None

    async def add_command(self,data):  # data={ position={latitude,longitude,nom},prix_total,commande_plat_set=[{plat_commander,quantite,prix_total},...]}
        endpoint = f"{self.base_url}commande/"
        headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
        data["client_id"] = self.me["id"]
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.post(url=endpoint, headers=headers, json=data)
                if self.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
                    response = await client.post(url=endpoint, headers=headers, json=data)
                return response.json()
        except httpx.RequestError as e:
            print("erreur add_command: ", e)

    async def delete_command(self,restau,data,livraison,id_command):
        endpoint = f"{self.base_url}commande/{id_command}"
        headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.delete(url=endpoint, headers=headers)
                if self.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
                    response = await client.delete(url=endpoint, headers=headers)
                self.data.delete_command(restau, livraison, data)
                return response.json()
        except requests.RequestException as e:
            print("erreur get_my_info: ", e)

    # ---------------------------Suivi de commandes

    async def rate_commande(self,data):  # data={ commande, rating}
        endpoint = f"{self.base_url}commande/plats/rate/"
        headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.post(url=endpoint, headers=headers, json=data)
                if self.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
                    response = await client.post(url=endpoint, headers=headers, json=data)
                return response.json()
        except httpx.RequestError as e:
            print("erreur rate_commande: ", e)

    async def rate_delivery(self,data):  # data={ livraison, rating}
        livraison_id = data.pop('livraison')
        endpoint = f"{self.base_url}livraisons/livreur/{livraison_id}/rate/"
        headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.post(url=endpoint, headers=headers, json=data)
                if self.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
                    response = await client.post(url=endpoint, headers=headers, json=data)
                return response.json()
        except httpx.RequestError as e:
            print("erreur rate_delivery: ", e)

    async def commande_history(self):
        endpoint = f"{self.base_url}commande/?client_id={self.me["id"]}"
        headers = {"Authorization": f"Bearer{self.tokens["access"]}"}

        try:
            async with (httpx.AsyncClient() as client):
                response = await client.get(url=endpoint, headers=headers)
                if self.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
                    response = await client.get(url=endpoint, headers=headers)
                return response.json()
        except httpx.RequestError as e:
            print("erreur commande history: ", e)
            return None

    # payer via om
    async def payement(self,data):
        endpoint = f"{self.base_url}payement/collect/"
        headers = {"Authorization": f"Bearer{self.tokens["access"]}"}

        try:
            async with (httpx.AsyncClient() as client):
                response = await client.post(url=endpoint, headers=headers, json=data)
                if self.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
                    response = await client.post(url=endpoint, headers=headers, json=data)
                return response.json()
        except httpx.RequestError as e:
            print("erreur payement: ", e)
            return None

userapi=UserApi()