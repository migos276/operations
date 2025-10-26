import json
import os.path
import asyncio
import datetime
from pathlib import PurePosixPath

import httpx
import requests
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from qrcode.main import QRCode
from qrcode import image



'''
base_url="http://127.0.0.1:8000/"
base_dir=os.path.dirname(os.path.abspath(__file__))
auth_json=os.path.join(base_dir,"auth.json")
store=JsonStore(auth_json)


if store.exists("user"):
    me=store.get("user")
else:
    me ={}
print(me)
if "connected" in me.keys():
    connected=True
else:
    connected=False
my_restaurant={}
my_boutique={}
livreur_id=None
boutique_id=None
restaurant_id=None
my_restaurant = {}

#************** token ****************
if store.exists("tokens"):
    tokens=store.get("tokens")
else:
    tokens ={}
print("tokens: ",tokens)
token_url=f"{base_url}token/"
refresh_url=f"{base_url}token/refresh/"
logout_url=f"{base_url}logout/"



#connexion
def login_restaurant(code):

    try:
        url=f"{base_url}utilisateur/?profile=entreprise&email=&code={code}"
        response1=requests.get(url)
        restaurant=response1.json()[0]
        print("restau ",restaurant)
        data = {"email": restaurant["email"], "password": code}
        response = requests.post(token_url,json=data)
        response.raise_for_status()
        token = response.json()
        print(token)
        store.put("tokens",
                  access=token["access"],
                  refresh=token["refresh"])
        tokens=store.get("tokens")
        user_id=restaurant
        if user_id:
            print("user",user_id)
            store.put("user", id=user_id["id"],email=user_id["email"],profile=user_id["profile"],tel=user_id['tel'],code=user_id["code"],a_restaurant=user_id["a_restaurant"],a_boutique=user_id["a_boutique"],logo=user_id["logo"],quartier=user_id["quartier"], connected=True)
            me = {}
            me = store.get("user")

            if user_id["a_restaurant"]:
                print("restau ✅")
                restau=get_restaurant(user_id["id"])[0]
                store.put("restaurant",id=restau["id"])
            if user_id["a_boutique"]:
                print("boutique ✅")
                boutique=get_boutique(user_id["id"])
                store.put("boutique", id=boutique["id"])
            print("connexion reussie")
        else:
            return False

    except requests.RequestException as e:
        print(f"erreur de connexion: {e}")

def get_id(email):
    endpoint = f"{base_url}utilisateur/?email={email}"
    headers = {"Authorization": f"Bearer{tokens["access"]}"}
    try:
        response = requests.get(url=endpoint, headers=headers)
        if auto_refresh(response.status_code):
            headers = {"Authorization": f"Bearer{tokens["access"]}"}
            response = requests.get(url=endpoint, headers=headers)
        return response.json()
    except requests.RequestException as e:
        print("erreur refresh: ", e)
        return None
def get_restaurant(id):
    endpoint = f"{base_url}restaurant/?type_plat=&rate=&est_ouvert=&user={id}"
    headers = {"Authorization": f"Bearer{tokens["access"]}"}
    try:
        response = requests.get(url=endpoint, headers=headers)
        if auto_refresh(response.status_code):
            headers = {"Authorization": f"Bearer{tokens["access"]}"}
            response = requests.get(url=endpoint, headers=headers)
        return response.json()
    except requests.RequestException as e:
        print("erreur refresh: ", e)
        return None
def get_boutique(id):
    endpoint = f"{base_url}Boutique/?est_ouvert=&user={id}"
    headers = {"Authorization": f"Bearer{tokens["access"]}"}
    try:
        response = requests.get(url=endpoint, headers=headers)
        if auto_refresh(response.status_code):
            headers = {"Authorization": f"Bearer{tokens["access"]}"}
            response = requests.get(url=endpoint, headers=headers)
        return response.json()
    except requests.RequestException as e:
        print("erreur refresh: ", e)
        return None
#connexion
def login_livreur(email,password):
    data={"email":email,"password":password}
    try:
        response = requests.post(token_url,json=data)
        response.raise_for_status()
        token = response.json()
        store.put("tokens",
                  access=token["access"],
                  refresh=token["refresh"])
        tokens=store.get("tokens")
        user_id=get_id(email)[0]
        livreur_url=f"{base_url}livreur/?restaurant=&user={user_id["id"]}"
        response = requests.get(livreur_url)
        livreur=response.json()

        if livreur:
            user=livreur.pop["user"]
            print("user",user)
            store.put("user", id=user["id"],email=email,profile=user["profile"], connected=True)
            store.put("livreur", matricule=livreur["matricule"], restaurant=livreur["restaurant"], description=livreur["description"])

            me = {}
            me = store.get("user")
            work = {}
            work = store.get('livreur')
            return "connexion reussie"
        else:
            print("login good but not livreur")
            logout()


    except requests.RequestException as e:
        if tokens["refresh"]:
            logout()
        return f"erreur de connexion: {e}"


def logout():
    try:
        refresh = tokens["refresh"]
        response = requests.post(logout_url,data={"refresh":refresh})
        response.raise_for_status()
        token = response.json()
        store.clear()
        print("deconnexion reussie")
    except requests.RequestException as e:
        print("erreur logout: ",e)

#rafraichir le token
def refresh_access():
    try:
        response=requests.post(refresh_url,json={"refresh":tokens["refresh"]})
        response.raise_for_status()
        data=response.json()
        store.put("tokens",
                  access=data["access"],
                  refresh=tokens["refresh"])
    except requests.RequestException as e:
        print("erreur refresh: ",e)

#generer et rafraichir automatique
def auto_refresh(statut):

    if statut==401:
        print("access expiré tentative de rafraichissement")
        refresh_access()
        return True


##############################
#           Restaurant       #
##############################

#-----------------------Authentification
def get_my_restaurant_info():
    endpoint = f"{base_url}restaurant/{restaurant_id}"
    headers = {"Authorization": f"Bearer{tokens["access"]}"}
    try:
        response = requests.get(url=endpoint, headers=headers)
        print(response.json())
        if auto_refresh(response.status_code):
            headers = {"Authorization": f"Bearer{tokens["access"]}"}
            response = requests.get(url=endpoint, headers=headers)
        return response.json()
    except requests.RequestException as e:
        print("erreur get_my_info: ", e)
        return None


def create_restaurant(type_plat,user_id):
    data={"type_plat":type_plat,"user_id":user_id}
    endpoint = f"{base_url}restaurant/"
    headers = {"Authorization": f"Bearer{tokens["access"]}"}
    try:
        response = requests.post(url=endpoint,json=data, headers=headers)
        print(response.json())
        if auto_refresh(response.status_code):
            headers = {"Authorization": f"Bearer{tokens["access"]}"}
            response = requests.post(url=endpoint,json=data, headers=headers)
        restau=response.json()
        store.put("restaurant", id=restau["id"])
        restaurant_id = store.get('restaurant')["id"]
        store.put("user",**{**store.get("user"),"a_restaurant":True})
        me = store.get("user")
        return restau
    except requests.RequestException as e:
        print("erreur create_restaurant: ", e)
        return None
def add_menu_hebdo():
    endpoint = f"{base_url}menu_hebdo/"
    print("tokens: ",tokens)
    headers = {"Authorization": f"Bearer{tokens["access"]}"}
    data={"restaurant":restaurant_id}
    try:
        response = requests.post(url=endpoint, headers=headers,json=data)
        if auto_refresh(response.status_code):
            headers = {"Authorization": f"Bearer{tokens["access"]}"}
            response = requests.post(url=endpoint, headers=headers,json=data)
        my_restaurant=get_my_restaurant_info()
        return response.json()
    except requests.RequestException as e:
        print("erreur add_menu_hebdo: ", e)
        return None

def create_plat(image="",nom=""):
    endpoint = f"{base_url}restaurant_plat/"
    headers = {"Authorization": f"Bearer{tokens["access"]}"}
    data = {"restaurant": restaurant_id,"plat": {"nom": nom}}
    print(data)
    try:
        response = requests.post(url=endpoint, headers=headers, json=data)
        if auto_refresh(response.status_code):
            headers = {"Authorization": f"Bearer{tokens["access"]}"}
            response = requests.post(url=endpoint, headers=headers, json=data)
        return response.json()
    except requests.RequestException as e:
        print("erreur create_plat: ", e)
        return None

def add_exist_plat_to_menu(menu,plat_id,prix,description):
    endpoint = f"{base_url}menu_plat/"
    print("tokens: ", tokens)
    headers = {"Authorization": f"Bearer{tokens["access"]}"}
    data = {"plat_id": plat_id, "prix": prix,"description":description,"menu":menu}
    try:
        response = requests.post(url=endpoint, headers=headers, json=data)
        if auto_refresh(response.status_code):
            headers = {"Authorization": f"Bearer{tokens["access"]}"}
            response = requests.post(url=endpoint, headers=headers, json=data)
        return response.json()
    except requests.RequestException as e:
        print("erreur add_exist_plat_to_menu: ", e)
        return None

def add_new_plat_to_menu(menu,nom,image,prix,description):
    endpoint = f"{base_url}menu_plat/"
    print("tokens: ", tokens)
    plat=create_plat(image,nom)
    print(plat)
    headers = {"Authorization": f"Bearer{tokens["access"]}"}
    data = {"plat_id": plat["id"], "prix": prix,"description":description,"menu":menu}
    try:
        response = requests.post(url=endpoint, headers=headers, json=data)
        if auto_refresh(response.status_code):
            headers = {"Authorization": f"Bearer{tokens["access"]}"}
            response = requests.post(url=endpoint, headers=headers, json=data)
        return response.json()
    except requests.RequestException as e:
        print("erreur add_exist_plat_to_menu: ", e)
        return None

def get_menu_plat(menu_id):
    endpoint = f"{base_url}menu/{menu_id}"
    headers = {"Authorization": f"Bearer{tokens["access"]}"}
    try:
        response = requests.get(url=endpoint, headers=headers)
        print(response.json())
        if auto_refresh(response.status_code):
            headers = {"Authorization": f"Bearer{tokens["access"]}"}
            response = requests.get(url=endpoint, headers=headers)
            print(response.json())
        return response.json()
    except requests.RequestException as e:
        print("erreur get_menu_plat: ", e)
        return None

def clear_menu(menu_id):
    endpoint = f"{base_url}menu/{menu_id}/clear"
    headers = {"Authorization": f"Bearer{tokens["access"]}"}
    try:
        response = requests.delete(url=endpoint, headers=headers)
        if auto_refresh(response.status_code):
            headers = {"Authorization": f"Bearer{tokens["access"]}"}
            response = requests.delete(url=endpoint, headers=headers)
        print("menu vidé")
        return response.json()
    except requests.RequestException as e:
        print("erreur delete_menu_plat: ", e)
        return None

def delete_menu_plat(menu_plat_id):
    endpoint = f"{base_url}menu_plat/{menu_plat_id}"
    headers = {"Authorization": f"Bearer{tokens["access"]}"}
    try:
        response = requests.delete(url=endpoint, headers=headers)
        if auto_refresh(response.status_code):
            headers = {"Authorization": f"Bearer{tokens["access"]}"}
            response = requests.delete(url=endpoint, headers=headers)
        print("menu supprimé")
        return response.json()
    except requests.RequestException as e:
        print("erreur delete_menu_plat: ", e)
        return None


def search_plat(text=""):
    endpoint = f"{base_url}restaurant/{restaurant_id}/plats?search={text}"
    print(endpoint)
    headers = {"Authorization": f"Bearer{tokens["access"]}"}
    try:
        response = requests.get(url=endpoint, headers=headers)
        if auto_refresh(response.status_code):
            headers = {"Authorization": f"Bearer{tokens["access"]}"}
            response = requests.get(url=endpoint, headers=headers)
        return response.json()
    except requests.RequestException as e:
        print("erreur search_plat: ", e)
        return None

##############################
#           boutique         #
##############################
def get_my_boutique_info():
    endpoint = f"{base_url}boutique/{boutique_id}"
    headers = {"Authorization": f"Bearer{tokens["access"]}"}
    print("inside")
    try:
        response = requests.get(url=endpoint, headers=headers)
        print(response.json())
        if auto_refresh(response.status_code):
            headers = {"Authorization": f"Bearer{tokens["access"]}"}
            response = requests.get(url=endpoint, headers=headers)
            print(response.json())
        return response.json()
    except requests.RequestException as e:
        print("erreur get_my_info: ", e)
        return None

def create_boutique():
    data={}
    endpoint = f"{base_url}boutique/"
    headers = {"Authorization": f"Bearer{tokens["access"]}"}
    try:
        response = requests.post(url=endpoint,json=data, headers=headers)
        print(response.json())
        if auto_refresh(response.status_code):
            headers = {"Authorization": f"Bearer{tokens["access"]}"}
            response = requests.post(url=endpoint,json=data, headers=headers)
        boutique=response.json()
        store.put("boutique", id=boutique["id"])
        boutique_id = store.get('boutique')["id"]
        store.put("user", **{**store.get("user"), "a_boutique": True})
        me = store.get("user")
        return boutique
    except requests.RequestException as e:
        print("erreur create_boutique: ", e)
        return None

##############################
#           Livreur          #
##############################
def get_my_livreur_info():
    endpoint = f"{base_url}livreur/{livreur_id}"
    headers = {"Authorization": f"Bearer{tokens["access"]}"}
    print("inside")
    try:
        response = requests.get(url=endpoint, headers=headers)
        print(response.json())
        if auto_refresh(response.status_code):
            headers = {"Authorization": f"Bearer{tokens["access"]}"}
            response = requests.get(url=endpoint, headers=headers)
            print(response.json())
        return response.json()
    except requests.RequestException as e:
        print("erreur get_my_info: ", e)
        return None



if me:
    if me["profile"]=="livreur" and store.exists("livreur"):
        livreur_id=store.get('livreur')["id"]
    if me["profile"]=="entreprise" :
        if me["a_restaurant"]:
            print(("ezz"))
            restaurant_id=store.get('restaurant')["id"]
            my_restaurant=get_my_restaurant_info()
        if me["a_boutique"]:
            boutique_id=store.get('boutique')["id"]
            my_boutique = get_my_boutique_info()
'''
def get_json(data_json):
    with open(data_json, "r") as data:
        tmp = json.load(data)
    return tmp

class DailySales:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_json = os.path.join(base_dir, "data.json")
        self.store = JsonStore(data_json)
        self.data={}
        self.init_daily_stats()

    def get_today_key(self):
        return str(datetime.date.today())

    def init_daily_stats(self):
        """Vérifie la date et initialise si besoin."""
        today = self.get_today_key()

        if not self.store.exists("stats"):
            # Première ouverture
            self.store.put("stats", date=today, plats_vendus=0, montant_gagne=0)

        else:
            self.data = self.store.get("stats")
            if self.data["date"] != today:
                # Nouveau jour → on réinitialise
                self.store.put("stats", date=today, plats_vendus=0, montant_gagne=0)
                self.data = self.store.get("stats")

    def add_sale(self,prix):
        """Ajoute un plat vendu et met à jour le montant."""
        self.data = self.store.get("stats")
        plats = self.data["plats_vendus"] + 1
        montant = self.data["montant_gagne"] + prix
        self.store.put("stats", date=self.data["date"], plats_vendus=plats, montant_gagne=montant)


class Restaurant:

    def __init__(self,id,user):
        self.restaurant_id = id
        self.my_restaurant = {}
        self.user=user

    def get_my_restaurant_info(self):
        endpoint = f"{self.user.base_url}restaurant/{self.restaurant_id}/"
        headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
        try:
            response =  requests.get(url=endpoint, headers=headers)
            if self.user.auto_refresh(response.status_code):
                headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
                response = requests.get(url=endpoint, headers=headers)
            self.my_restaurant = response.json()
            return True
        except requests.RequestException as e:
            print("erreur get_my_info: ", e)
            return None

    async def add_menu_hebdo(self):
        endpoint = f"{self.user.base_url}menu_hebdo/"
        headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
        data = {"restaurant": self.restaurant_id}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.post(url=endpoint, headers=headers, json=data)
                if self.user.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
                    response = await client.post(url=endpoint, headers=headers, json=data)
                self.get_my_restaurant_info()
                return response.json()
        except httpx.RequestError as e:
            print("erreur add_menu_hebdo: ", e)
            return None

    async def create_plat(self,image="", nom=""):
        with open(image, "rb") as f:
            files = {"image": f}
            print("image ",image,"files ",files)
            endpoint = f"{self.user.base_url}restaurant_plat/"
            headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
            data = {"restaurant": self.restaurant_id, "plat_nom": nom}
            print(data)
            try:
                async with (httpx.AsyncClient() as client):
                    response = await client.post(url=endpoint, headers=headers, data=data,files=files)
                    if self.user.auto_refresh(response.status_code):
                        headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
                        response = await client.post(url=endpoint, headers=headers, data=data)
                    return response.json()
            except httpx.RequestError as e:
                print("erreur create_plat: ", e)
                return None

    async def add_exist_plat_to_menu(self,menu, plat_id, prix, description):
        endpoint = f"{self.user.base_url}menu_plat/"
        print("tokens: ", self.user.tokens)
        headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
        data = {"plat_id": plat_id, "prix": prix, "description": description, "menu": menu}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.post(url=endpoint, headers=headers, json=data)
                if self.user.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
                    response = await client.post(url=endpoint, headers=headers, json=data)
                self.get_my_restaurant_info()
                return response.status_code
        except httpx.RequestError as e:
            print("erreur add_exist_plat_to_menu: ", e)
            return None

    async def add_new_plat_to_menu(self,menu, nom, image, prix, description):
        endpoint = f"{self.user.base_url}menu_plat/"
        plat = await self.create_plat(image, nom)
        print(plat)
        headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
        data = {"plat_id": plat["id"], "prix": prix, "description": description, "menu": menu}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.post(url=endpoint, headers=headers, json=data)
                if self.user.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
                    response = await client.post(url=endpoint, headers=headers, json=data)
                self.get_my_restaurant_info()
                return response.json()
        except httpx.RequestError as e:
            print("erreur add_exist_plat_to_menu: ", e)
            return None

    async def get_menu_plat(self,menu_id):
        endpoint = f"{self.user.base_url}menu/{menu_id}/"
        headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.get(url=endpoint, headers=headers)
                print(response.json())
                if self.user.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
                    response = await client.get(url=endpoint, headers=headers)
                    print(response.json())
                    self.get_my_restaurant_info()
            return response.json()
        except httpx.RequestError as e:
            print("erreur get_menu_plat: ", e)
            return None

    async def clear_menu(self,menu_id):
        endpoint = f"{self.user.base_url}menu/{menu_id}/clear/"
        headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.delete(url=endpoint, headers=headers)
                if self.user.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
                    response = await client.delete(url=endpoint, headers=headers)
                print("menu vidé")
                self.get_my_restaurant_info()
                return response.status_code
        except httpx.RequestError as e:
            print("erreur delete_menu_plat: ", e)
            return None

    async def delete_menu_plat(self,menu_plat_id):
        endpoint = f"{self.user.base_url}menu_plat/{menu_plat_id}/"
        headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.delete(url=endpoint, headers=headers)
                if self.user.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
                    response = await client.delete(url=endpoint, headers=headers)
                self.get_my_restaurant_info()
                return response.status_code
        except httpx.RequestError as e:
            print("erreur delete_menu_plat: ", e)
            return None

    async def search_plat(self,text=""):
        endpoint = f"{self.user.base_url}restaurant/{self.restaurant_id}/plats/?search={text}"
        print(endpoint)
        headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.get(url=endpoint, headers=headers)
                if self.user.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
                    response = await client.get(url=endpoint, headers=headers)
                return response.json()
        except httpx.RequestError as e:
            print("erreur search_plat: ", e)
            return None


    async def add_exist_static_plat_to_menu(self, menu, plat_id, prix, description):
        endpoint = f"{self.user.base_url}menu_static_plat/"
        print("tokens: ", self.user.tokens)
        headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
        data = {"plat_id": plat_id, "prix": prix, "description": description, "menu": menu}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.post(url=endpoint, headers=headers, json=data)
                if self.user.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
                    response = await client.post(url=endpoint, headers=headers, json=data)
                self.get_my_restaurant_info()
                return response.json()
        except httpx.RequestError as e:
            print("erreur add_exist_plat_to_menu: ", e)
            return None

    async def add_new_static_plat_to_menu(self, menu, nom, image, prix, description):
        endpoint = f"{self.user.base_url}menu_static_plat/"
        plat = self.create_plat(image, nom)
        print(plat)
        headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
        data = {"plat_id": plat["id"], "prix": prix, "description": description, "menu": menu}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.post(url=endpoint, headers=headers, json=data)
                if self.user.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
                    response = await client.post(url=endpoint, headers=headers, json=data)
                self.get_my_restaurant_info()
                return response.json()
        except httpx.RequestError as e:
            print("erreur add_exist_plat_to_menu: ", e)
            return None

    async def add_static_menu(self):
        endpoint = f"{self.user.base_url}menu_statique/"
        headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
        data = {"restaurant": self.restaurant_id}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.post(url=endpoint, headers=headers, json=data)
                if self.user.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
                    response = await client.post(url=endpoint, headers=headers, json=data)
                self.get_my_restaurant_info()
                return response.json()
        except httpx.RequestError as e:
            print("erreur add_static_menuo: ", e)
            return None

    async def clear_static_menu(self,menu_id):
        endpoint = f"{self.user.base_url}menu_statique/{menu_id}/clear/"
        headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.delete(url=endpoint, headers=headers)
                if self.user.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
                    response = await client.delete(url=endpoint, headers=headers)
                print("menu statique vidé")
                self.get_my_restaurant_info()
                return response.status_code
        except httpx.RequestError as e:
            print("erreur clear_static_menu: ", e)
            return None

    async def get_all_plat(self):
        endpoint = f"{self.user.base_url}restaurant/{self.restaurant_id}/plats/"
        headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.get(url=endpoint, headers=headers)
                print(response.json())
                if self.user.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
                    response = await client.get(url=endpoint, headers=headers)

            return response.json()
        except httpx.RequestError as e:
            print("erreur get_all_plat: ", e)
            return None

    async def delete_plat(self,plat_id):
        endpoint = f"{self.user.base_url}restaurant_plat/{plat_id}/"
        headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.delete(url=endpoint, headers=headers)
                if self.user.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
                    response = await client.delete(url=endpoint, headers=headers)

            return response.status_code
        except httpx.RequestError as e:
            print("erreur delete_plat: ", e)
            return None

    async def update_horaire(self,horaire_id,data):
        endpoint = f"{self.user.base_url}horaire/{horaire_id}/"
        headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.patch(url=endpoint, headers=headers,json=data)
                if self.user.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.user.tokens["access"]}"}
                    response = await client.patch(url=endpoint, headers=headers,json=data)
                self.get_my_restaurant_info()
            return response.status_code
        except httpx.RequestError as e:
            print("erreur update_horaire: ", e)
            return None




    class Boutique:
        def __init__(self,user):
            self.boutique_id = 0
            self.my_boutique = {}
            self.user=user

class Entreprise:

    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/"
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        auth_json = os.path.join(self.base_dir, "auth.json")
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

        self.token_url = f"{self.base_url}token/"
        self.refresh_url = f"{self.base_url}token/refresh/"
        self.logout_url = f"{self.base_url}logout/"
        self.get_info()


    def get_info(self):
        if self.me and self.me["profile"] == "entreprise":
            print(self.me)
            if self.me["a_restaurant"]:
                restau_id=self.store.get('restaurant')["id"]
                self.restaurant=Restaurant(id=restau_id,user=self)
                self.restaurant.get_my_restaurant_info()
            if self.me["a_boutique"]:
                boutique_id = self.store.get('boutique')["id"]
                #self.boutique = Boutique(id=boutique_id,user=self)
                #self.boutique.get_my_restaurant_info()

    async def login_restaurant(self,code):

        try:
            async with (httpx.AsyncClient() as client):
                url = f"{self.base_url}utilisateur/?profile=entreprise&email=&code={code}"
                response1 = await client.get(url)
                entreprise = response1.json()[0]
                print("restau ", entreprise)
                data = {"email": entreprise["email"], "password": code}
                response = await client.post(self.token_url, json=data)
                response.raise_for_status()
                token = response.json()
                print(token)
                self.store.put("tokens",
                          access=token["access"],
                          refresh=token["refresh"])
                self.tokens = self.store.get("tokens")
                user_id = entreprise
                if user_id:
                    print("user", user_id)
                    self.store.put("user", id=user_id["id"], email=user_id["email"], profile=user_id["profile"],
                              tel=user_id['tel'], code=user_id["code"], a_restaurant=user_id["a_restaurant"],
                              a_boutique=user_id["a_boutique"], logo=user_id["logo"], quartier=user_id["quartier"],
                              connected=True)
                    self.me = {}
                    self.me = self.store.get("user")

                    if user_id["a_restaurant"]:
                        print("restau ✅")
                        restau =await self.get_restaurant(user_id["id"])[0]
                        self.store.put("restaurant", id=restau["id"])
                    if user_id["a_boutique"]:
                        print("boutique ✅")
                        boutique =await self.get_boutique(user_id["id"])
                        self.store.put("boutique", id=boutique["id"])
                    self.get_info()
                    print("connexion reussie")
                else:
                    return False

        except requests.RequestException as e:
            print(f"erreur de connexion: {e}")

    async def get_id(self,email):
        endpoint = f"{self.base_url}utilisateur/?email={email}"
        headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.get(url=endpoint, headers=headers)
                if self.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
                    response = await client.get(url=endpoint, headers=headers)
                return response.json()
        except requests.RequestException as e:
            print("erreur refresh: ", e)
            return None

    async def get_restaurant(self,id):
        endpoint = f"{self.base_url}restaurant/?type_plat=&rate=&est_ouvert=&user={id}"
        headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.get(url=endpoint, headers=headers)
                if self.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
                    response = await client.get(url=endpoint, headers=headers)
                return response.json()
        except requests.RequestException as e:
            print("erreur refresh: ", e)
            return None

    async def get_boutique(self,id):
        endpoint = f"{self.base_url}Boutique/?est_ouvert=&user={id}"
        headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.get(url=endpoint, headers=headers)
                if self.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
                    response = await client.get(url=endpoint, headers=headers)
                return response.json()
        except requests.RequestException as e:
            print("erreur refresh: ", e)
            return None

    async def logout(self):
        try:
            async with (httpx.AsyncClient() as client):
                refresh = self.tokens["refresh"]
                response = await client.post(self.logout_url, data={"refresh": refresh})
                response.raise_for_status()
                token = response.json()
                self.store.clear()
            print("deconnexion reussie")
        except requests.RequestException as e:
            print("erreur logout: ", e)

    # rafraichir le token
    def refresh_access(self):
        try:
            response = requests.post(self.refresh_url, json={"refresh": self.tokens["refresh"]})
            response.raise_for_status()
            data = response.json()
            self.store.put("tokens",
                      access=data["access"],
                      refresh=self.tokens["refresh"])
            self.tokens = self.store.get("tokens")
        except requests.RequestException as e:
            print("erreur refresh: ", e)

    # generer et rafraichir automatique
    def auto_refresh(self, statut):
        if statut == 401:
            print("Access expiré, tentative de rafraîchissement")
            self.refresh_access()
            return True
        return False

    async def create_restaurant(self,type_plat):
        data = {"type_plat": type_plat, "user_id": self.me["id"]}
        endpoint = f"{self.base_url}restaurant/"
        headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
        try:
            async with (httpx.AsyncClient() as client):
                response = await client.post(url=endpoint, json=data, headers=headers)
                print(response.json())
                if self.auto_refresh(response.status_code):
                    headers = {"Authorization": f"Bearer{self.tokens["access"]}"}
                    response = await client.post(url=endpoint, json=data, headers=headers)
                restau = response.json()
                self.store.put("restaurant", id=restau["id"])
                self.restaurant = Restaurant(id=restau["id"],user=self)
                self.store.put("user", **{**self.store.get("user"), "a_restaurant": True})
                self.me = self.store.get("user")
                return restau
        except httpx.RequestError as e:
            print("erreur create_restaurant: ", e)
            return None

    def generate_qrcode(self):
        if os.path.isfile("img/qrcode.png"):
            pass
        else:
            code = QRCode(version=1.0, box_size=15, border=4)
            code.add_data(self.me["id"])
            code.make(fit=True)
            img = code.make_image(fill='BLACK', back_color="WHITE")
            img.save(os.path.join(self.base_dir, "img/qrcode.png"))

        path=os.path.join(self.base_dir, "img/qrcode.png")
        path=path.replace("\\","/")
        print(path)
        return  path

    def send_image(self,image_path): # Ton API
        filename = os.path.basename(image_path)
        ext = os.path.splitext(filename)[1].lower()

        if ext in [".jpg", ".jpeg"]:
            mime_type = "image/jpeg"
        elif ext == ".png":
            mime_type = "image/png"
        else:
            return None# fallback générique

        return {"image": (filename, open(image_path, "rb"), mime_type)}


entreprise_api=Entreprise()
restaurant_api=entreprise_api.restaurant
dailystat=DailySales()
print(restaurant_api.my_restaurant)