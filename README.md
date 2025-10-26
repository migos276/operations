# Documentation de l'API Camer-Eat

Ce document fournit une description détaillée des points de terminaison (endpoints) de l'API pour l'application Camer-Eat, un service de livraison de nourriture.

## Base URL

Toutes les URL de l'API sont préfixées par `http://127.0.0.1:8000/`.

---

## Authentification

### 1. Obtenir les jetons JWT

- **Endpoint:** `/token/`
- **Méthode:** `POST`
- **Description:** Connecte un utilisateur et retourne des jetons d'accès (`access`) et de rafraîchissement (`refresh`).
- **Corps de la requête (`JSON`):**
  ```json
  {
      "email": "user@example.com",
      "password": "your_password"
  }
  ```

### 2. Rafraîchir le jeton d'accès

- **Endpoint:** `/token/refresh/`
- **Méthode:** `POST`
- **Description:** Utilise un jeton de rafraîchissement pour obtenir un nouveau jeton d'accès.
- **Corps de la requête (`JSON`):**
  ```json
  {
      "refresh": "refresh_token_here"
  }
  ```

### 3. Déconnexion

- **Endpoint:** `/logout/`
- **Méthode:** `POST`
- **Description:** Invalide le jeton de rafraîchissement pour déconnecter l'utilisateur.

---

## Gestion des Utilisateurs (`/utilisateur/`)

### 1. Créer un utilisateur (Inscription)

- **Endpoint:** `/utilisateur/`
- **Méthode:** `POST`
- **Description:** Crée un nouvel utilisateur client.
- **Corps de la requête (`JSON`):**
  ```json
  {
      "username": "testuser",
      "tel": 123456789,
      "email": "test@example.com",
      "password": "strongpassword"
  }
  ```

### 2. Lister et filtrer les utilisateurs

- **Endpoint:** `/utilisateur/`
- **Méthode:** `GET`
- **Description:** Récupère une liste d'utilisateurs.
- **Paramètres de requête:**
  - `profile` (e.g., `client`, `restaurant`, `livreur`, `entreprise`)
  - `email`
  - `code`

### 3. Récupérer/Modifier/Supprimer un utilisateur

- **Endpoint:** `/utilisateur/{id}/`
- **Méthodes:** `GET`, `PUT`, `PATCH`, `DELETE`
- **Description:**
  - `GET`: Récupère les informations d'un utilisateur spécifique.
  - `PUT/PATCH`: Met à jour les informations d'un utilisateur.
  - `DELETE`: Supprime un utilisateur.

### 4. Créer une entreprise

- **Endpoint:** `/restaurants/new/`
- **Méthode:** `POST`
- **Description:** Crée un nouvel utilisateur entreprise (restaurant ou boutique).
- **Corps de la requête (`JSON`):**
  ```json
  {
      "username": "restaurant_name",
      "email": "restaurant@example.com",
      "tel": 123456789,
      "quartier": "nom_du_quartier"
  }
  ```

### 5. Mettre à jour la position d'un livreur

- **Endpoint:** `/utilisateur/update_position/`
- **Méthode:** `POST`
- **Description:** Met à jour la position GPS d'un livreur pour une commande.
- **Corps de la requête (`JSON`):**
  ```json
  {
      "order_id": 123,
      "livreur_id": 456,
      "latitude": 3.8667,
      "longitude": 11.5167
  }
  ```

---

## Restaurants (`/restaurant/`)

### 1. Lister et rechercher des restaurants

- **Endpoint:** `/restaurant/`
- **Méthode:** `GET`
- **Description:** Récupère une liste de restaurants.
- **Paramètres de requête:**
  - `search`: Recherche par nom, email ou quartier de l'utilisateur.
  - `type_plat`: Filtre par type de plat.
  - `rate`: Filtre par note.
  - `est_ouvert`: Filtre par statut (ouvert/fermé).
  - `user`: Filtre par ID utilisateur.

### 2. Créer/Récupérer/Modifier/Supprimer un restaurant

- **Endpoint:** `/restaurant/{id}/`
- **Méthodes:** `GET`, `POST`, `PUT`, `PATCH`, `DELETE`
- **Description:** Opérations CRUD sur les restaurants.

### 3. Obtenir les types de plats

- **Endpoint:** `/types-plats/`
- **Méthode:** `GET`
- **Description:** Retourne une liste de tous les types de plats uniques disponibles dans les restaurants.

### 4. Obtenir les plats d'un restaurant spécifique

- **Endpoint:** `/restaurant/{restaurant_id}/plats/`
- **Méthode:** `GET`
- **Description:** Récupère tous les plats associés à un restaurant spécifique.
- **Paramètres de requête:**
  - `search`: Recherche par nom de plat.

---

## Boutiques (`/boutique/`)

### 1. Lister et rechercher des boutiques

- **Endpoint:** `/boutique/`
- **Méthode:** `GET`
- **Description:** Récupère une liste de boutiques.
- **Paramètres de requête:**
  - `search`: Recherche par nom, email ou quartier de l'utilisateur.
  - `est_ouvert`: Filtre par statut (ouvert/fermé).
  - `user`: Filtre par ID utilisateur.

### 2. Créer/Récupérer/Modifier/Supprimer une boutique

- **Endpoint:** `/boutique/{id}/`
- **Méthodes:** `GET`, `POST`, `PUT`, `PATCH`, `DELETE`
- **Description:** Opérations CRUD sur les boutiques.

---

## Livreurs (`/livreur/`)

### 1. Lister et filtrer les livreurs

- **Endpoint:** `/livreur/`
- **Méthode:** `GET`
- **Description:** Récupère une liste de livreurs.
- **Paramètres de requête:**
  - `entreprise`: Filtre par entreprise.
  - `user`: Filtre par ID utilisateur.

### 2. Créer/Récupérer/Modifier/Supprimer un livreur

- **Endpoint:** `/livreur/{id}/`
- **Méthodes:** `GET`, `POST`, `PUT`, `PATCH`, `DELETE`
- **Description:** Opérations CRUD sur les livreurs.

---

## Plats et Menus

### 1. Plats globaux

- **Endpoint:** `/plat/`
- **Méthodes:** `GET`, `POST`
- **Description:**
  - `GET`: Liste tous les plats globaux.
  - `POST`: Crée un nouveau plat global.
- **Paramètres de requête (GET):**
  - `ordering`: Tri par nom ou ID (e.g., `nom`, `-nom`, `id`).

### 2. Gestion des plats individuels

- **Endpoint:** `/plat/{id}/`
- **Méthodes:** `GET`, `PUT`, `PATCH`, `DELETE`
- **Description:** Opérations CRUD sur un plat global spécifique.

### 3. Plats des restaurants

- **Endpoint:** `/restaurant-plat/`
- **Méthodes:** `GET`, `POST`
- **Description:**
  - `GET`: Liste les associations plat-restaurant.
  - `POST`: Associe un plat à un restaurant.
- **Paramètres de requête (GET):**
  - `restaurant__id`: Filtre par restaurant.
  - `plat__id`: Filtre par plat.
  - `search`: Recherche par nom de plat.

### 4. Gestion des plats de restaurant individuels

- **Endpoint:** `/restaurant-plat/{id}/`
- **Méthodes:** `GET`, `PUT`, `PATCH`, `DELETE`
- **Description:** Opérations CRUD sur une association plat-restaurant spécifique.

### 5. Plats du menu du jour

- **Endpoint:** `/today/`
- **Méthode:** `GET`
- **Description:** Récupère les plats du menu du jour actuel.
- **Paramètres de requête:**
  - `search`: Recherche par nom de plat ou description.
  - `menu`: Filtre par ID de menu.

### 6. Plats des menus hebdomadaires

- **Endpoint:** `/menu-plat/`
- **Méthodes:** `GET`, `POST`
- **Description:** Gestion des plats dans les menus hebdomadaires.

- **Endpoint:** `/menu-plat/{id}/`
- **Méthodes:** `GET`, `PUT`, `PATCH`, `DELETE`
- **Description:** Opérations CRUD sur un plat de menu hebdomadaire spécifique.

### 7. Plats des menus statiques

- **Endpoint:** `/menu_static_plat/`
- **Méthodes:** `GET`, `POST`
- **Description:** Gestion des plats dans les menus statiques.
- **Paramètres de requête (GET):**
  - `search`: Recherche par nom de plat ou description.
  - `prix`: Filtre par prix.
  - `plat__rate`: Filtre par note du plat.

- **Endpoint:** `/menu_static_plat/{id}/`
- **Méthodes:** `GET`, `PUT`, `PATCH`, `DELETE`
- **Description:** Opérations CRUD sur un plat de menu statique spécifique.

### 8. Menus hebdomadaires

- **Endpoint:** `/menu/`
- **Méthodes:** `GET`, `POST`
- **Description:** Gestion des menus hebdomadaires.
- **Paramètres de requête (GET):**
  - `search`: Recherche par nom de plat.
  - `jour`: Filtre par jour (lundi, mardi, etc.).

- **Endpoint:** `/menu/{id}/`
- **Méthodes:** `GET`, `PUT`, `PATCH`, `DELETE`
- **Description:** Opérations CRUD sur un menu hebdomadaire spécifique.

### 9. Vider un menu hebdomadaire

- **Endpoint:** `/menu/{id}/clear/`
- **Méthode:** `DELETE`
- **Description:** Supprime tous les plats d'un menu hebdomadaire donné.

### 10. Menus hebdomadaires globaux

- **Endpoint:** `/menu_hebdo/`
- **Méthodes:** `GET`, `POST`
- **Description:** Gestion des configurations de menus hebdomadaires.
- **Paramètres de requête (GET):**
  - `search`: Recherche par nom de plat ou jour.
  - `menus__jour`: Filtre par jour.
  - `restaurant__id`: Filtre par restaurant.

- **Endpoint:** `/menu_hebdo/{id}/`
- **Méthodes:** `GET`, `PUT`, `PATCH`, `DELETE`
- **Description:** Opérations CRUD sur une configuration de menu hebdomadaire spécifique.

### 11. Menus statiques

- **Endpoint:** `/menu_statique/`
- **Méthodes:** `GET`, `POST`
- **Description:** Gestion des menus statiques.
- **Paramètres de requête (GET):**
  - `restaurant__id`: Filtre par restaurant.
  - `search`: Recherche par nom de plat ou description.

- **Endpoint:** `/menu_statique/{id}/`
- **Méthodes:** `GET`, `PUT`, `PATCH`, `DELETE`
- **Description:** Opérations CRUD sur un menu statique spécifique.

### 12. Vider un menu statique

- **Endpoint:** `/menu-statique/{id}/clear/`
- **Méthode:** `DELETE`
- **Description:** Supprime tous les plats d'un menu statique donné.

### 13. Plats pas chers du menu du jour

- **Endpoint:** `/plats/pas_cher/`
- **Méthode:** `POST`
- **Description:** Récupère les plats du menu du jour dont le prix est inférieur ou égal à un maximum.
- **Corps de la requête (`JSON`):**
  ```json
  {
      "prix_max": 200
  }
  ```

---

## Commandes

### 1. Commandes restaurant

- **Endpoint:** `/commande_restau/`
- **Méthodes:** `GET`, `POST`
- **Description:** Gestion des commandes passées dans les restaurants.
- **Paramètres de requête (GET):**
  - `search`: Recherche par plat commandé, client.
  - `statut`: Filtre par statut (attente, validée, etc.).
  - `jour`, `mois`, `annee`: Filtre par date.

- **Endpoint:** `/commande_restau/{id}/`
- **Méthodes:** `GET`, `PUT`, `PATCH`, `DELETE`
- **Description:** Opérations CRUD sur une commande restaurant spécifique. Note: Impossible de supprimer une commande déjà validée.

### 2. Commandes boutique

- **Endpoint:** `/commande_boutique/`
- **Méthodes:** `GET`, `POST`
- **Description:** Gestion des commandes passées dans les boutiques.
- **Paramètres de requête (GET):**
  - `search`: Recherche par produit, client.
  - `statut`: Filtre par statut.
  - `jour`, `mois`, `annee`: Filtre par date.

- **Endpoint:** `/commande_boutique/{id}/`
- **Méthodes:** `GET`, `PUT`, `PATCH`, `DELETE`
- **Description:** Opérations CRUD sur une commande boutique spécifique. Note: Impossible de supprimer une commande déjà validée.

### 3. Plats commandés

- **Endpoint:** `/commande_plat/`
- **Méthodes:** `GET`, `POST`
- **Description:** Gestion des plats individuels dans les commandes.
- **Paramètres de requête (GET):**
  - `commande_id`: Filtre par ID de commande.

- **Endpoint:** `/commande_plat/{id}/`
- **Méthodes:** `GET`, `PUT`, `PATCH`, `DELETE`
- **Description:** Opérations CRUD sur un plat commandé spécifique.

### 4. Noter un plat commandé

- **Endpoint:** `/commande/plats/rate/`
- **Méthode:** `POST`
- **Description:** Permet à un client de noter un plat commandé, ce qui met à jour la note du plat et du restaurant.
- **Corps de la requête (`JSON`):**
  ```json
  {
      "commande": 123,
      "rating": 4.5
  }
  ```

---

## Livraisons (`/livraison/`)

### 1. Lister les livraisons

- **Endpoint:** `/livraison/`
- **Méthodes:** `GET`, `POST`
- **Description:** Gestion des livraisons.

### 2. Gestion individuelle des livraisons

- **Endpoint:** `/livraison/{id}/`
- **Méthodes:** `GET`, `PUT`, `PATCH`, `DELETE`
- **Description:** Opérations CRUD sur une livraison spécifique.

### 3. Noter un livreur

- **Endpoint:** `/livraisons/livreur/{commande_id}/rate/`
- **Méthode:** `POST`
- **Description:** Permet de noter un livreur après livraison.
- **Corps de la requête (`JSON`):**
  ```json
  {
      "rating": 4.0
  }
  ```

---

## Paiements (`/payement/`)

### 1. Envoyer de l'argent (Collecte)

- **Endpoint:** `/payement/send/`
- **Méthode:** `POST`
- **Description:** Initie un paiement (envoi d'argent via mobile money).
- **Corps de la requête (`JSON`):**
  ```json
  {
      "numero": "237123456789",
      "montant": 5000,
      "service": "MTN"
  }
  ```

### 2. Recevoir de l'argent (Dépôt)

- **Endpoint:** `/payement/receive/`
- **Méthode:** `POST`
- **Description:** Initie un dépôt d'argent sur un compte mobile money.
- **Corps de la requête (`JSON`):**
  ```json
  {
      "numero": "237123456789",
      "montant": 10000,
      "service": "MTN"
  }
  ```

---

## Produits et Rayons (`/shop/`)

### 1. Produits

- **Endpoint:** `/produit/`
- **Méthodes:** `GET`, `POST`
- **Description:** Gestion des produits dans les boutiques.
- **Paramètres de requête (GET):**
  - `search`: Recherche par nom ou nom de rayon.
  - `prix`: Filtre par prix.

- **Endpoint:** `/produit/{id}/`
- **Méthodes:** `GET`, `PUT`, `PATCH`, `DELETE`
- **Description:** Opérations CRUD sur un produit spécifique.

### 2. Mettre à jour le stock d'un produit

- **Endpoint:** `/produit/update/`
- **Méthode:** `POST`
- **Description:** Met à jour la quantité en stock d'un produit.
- **Corps de la requête (`JSON`):**
  ```json
  {
      "produit": 123,
      "quantite": 50
  }
  ```

### 3. Rayons

- **Endpoint:** `/rayons/`
- **Méthodes:** `GET`, `POST`
- **Description:** Gestion des rayons dans les boutiques.
- **Paramètres de requête (GET):**
  - `search`: Recherche par nom.

- **Endpoint:** `/rayons/{id}/`
- **Méthodes:** `GET`, `PUT`, `PATCH`, `DELETE`
- **Description:** Opérations CRUD sur un rayon spécifique.

---

## Horaires

### 1. Horaires individuels

- **Endpoint:** `/horaire/`
- **Méthodes:** `GET`, `POST`
- **Description:** Gestion des horaires individuels.

- **Endpoint:** `/horaire/{id}/`
- **Méthodes:** `GET`, `PUT`, `PATCH`, `DELETE`
- **Description:** Opérations CRUD sur un horaire spécifique.

### 2. Horaires hebdomadaires

- **Endpoint:** `/horaire_hebdomadaire/`
- **Méthodes:** `GET`, `POST`
- **Description:** Gestion des configurations d'horaires hebdomadaires.

- **Endpoint:** `/horaire_hebdomadaire/{id}/`
- **Méthodes:** `GET`, `PUT`, `PATCH`, `DELETE`
- **Description:** Opérations CRUD sur une configuration d'horaires hebdomadaire spécifique.

---

## Administration

### 1. Interface d'administration Django

- **Endpoint:** `/admin/`
- **Méthode:** `GET`
- **Description:** Accès à l'interface d'administration Django (réservé aux administrateurs).

---

## Notes importantes

- **Authentification:** La plupart des endpoints nécessitent une authentification via JWT. Incluez le token d'accès dans l'en-tête `Authorization: Bearer <access_token>`.
- **Permissions:** Certaines opérations sont réservées aux utilisateurs authentifiés avec des rôles spécifiques (client, restaurant, livreur, entreprise).
- **Formats de données:** Toutes les requêtes POST/PUT/PATCH utilisent le format JSON.
- **Filtres et recherche:** De nombreux endpoints supportent des paramètres de requête pour filtrer et rechercher des données.
- **Statuts de commande:** Les commandes ont différents statuts (attente, validée, etc.) qui affectent les opérations possibles.
- **Notes et évaluations:** Le système permet de noter les plats, restaurants et livreurs, ce qui met à jour leurs moyennes automatiquement.
