# Auth System

Il s'agit d'une API de production développée en Django intégrant un contrôle d'accès basé sur les rôles (RBAC), une authentification par jetons JWT, une authentification à deux facteurs (OTP) et le traitement asynchrone des tâches en arrière-plan avec Celery et Redis.

## Architecture

Le projet est structuré en plusieurs applications distinctes afin de garantir une séparation stricte des responsabilités :

- `accounts/` : Gère le modèle Utilisateur, la connexion/inscription JWT, et les routes d'authentification.
- `roles/` : S'occupe du système RBAC, des permissions dynamiques et du middleware de sécurité RBAC personnalisé.
- `security/` : Gère les journaux de sécurité (logs), la limitation de débit (Rate Limiting) et le cycle de vie des OTP via Redis.
- `common/` : Contient les utilitaires standardisés, les formats de réponse et les validateurs.
- `infrastructure/` : Orchestre l'intégration des services externes (Envoi d'E-mails, Clients Redis).

## Prérequis

- Docker et Docker Compose installés sur votre machine d'exécution.
- Un fichier local `.env` créé à la racine du projet contenant la configuration SMTP et les clés secrètes.

## Lancement de l'Application

L'ensemble de l'écosystème de l'application est conteneurisé à l'aide de Docker Compose.

1. Construire et lancer les services :
```bash
docker compose up --build
```

Cette commande démarre 4 conteneurs isolés :
- `web` : L'API Django REST fonctionnant sur le port 8000.
- `redis` : La base de données en mémoire fonctionnant sur le port 6379.
- `celery` : Le "worker" exécutant les tâches asynchrones en arrière-plan.
- `flower` : Le tableau de bord de surveillance pour les tâches Celery, disponible sur le port 5555.

2. Exécuter les migrations de base de données :
Ouvrez un nouveau terminal et exécutez les migrations à l'intérieur du conteneur `web` :
```bash
docker compose exec web python manage.py migrate
```

3. Créer un super-utilisateur :
```bash
docker compose exec web python manage.py createsuperuser
```

## Documentation de l'API

Les documentations standards Swagger et OpenAPI sont générées de manière automatique via `drf-spectacular`.

- Interface Swagger UI : `http://localhost:8000/api/docs/`
- Schéma OpenAPI brut : `http://localhost:8000/api/schema/`

Ces interfaces interactives vous permettent de tester directement les points de terminaison de l'API, de générer des codes OTP et de s'authentifier.

## Fonctionnalités Principales et Sécurité

- **Gestion de Profil et Sessions** : Inscription, route`/me/` pour la récupération des profils, et rafraîchissement des jetons d'accès via JWT.
- **Interface d'Administration Moderne** : Espace d'administration Django entièrement redessiné avec le thème `django-unfold` pour une expérience d'administration élégante et moderne.
- **Rate Limiting** : Imposé via Redis sur les routes sensibles (ex. 5 tentatives par minute pour la connexion).
- **Génération OTP** : Mots de passe à usage unique stockés de façon sécurisée dans Redis avec un délai d'expiration de 5 minutes.
- **Règles RBAC** : Middleware garantissant une vérification stricte des rôles et des autorisations d'accès.
- **Logs de Sécurité** : Tous les événements d'authentification (réussites et échecs) sont enregistrés avec suivi de l'adresse IP.

## Tâches en Arrière-plan (Background Tasks)

L'envoi des e-mails lors de la génération de l'OTP a été délégué à Celery. Lorsqu'un code OTP est généré, l'API répond instantanément au client web, pendant que le worker Celery se charge de contacter de façon asynchrone le serveur SMTP pour dispatcher l'e-mail.
