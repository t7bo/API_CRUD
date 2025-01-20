# API_CRUD
[Lien du brief](https://zippy-twig-11a.notion.site/Brief-D-veloppement-d-une-API-CRUD-1621f9041c96808ba910e8dd8399d638)

## Veille sur l'authentification

### Exploration des solutions d'authentification

- **OAuth2 et JWT** : Une solution largement utilisée pour sécuriser les API avec des tokens. Elle est adaptée aux systèmes modernes de microservices.
- **Authentification basique (Basic Auth)** : Bien que simple, elle est moins sécurisée et n'est pas recommandée pour des applications de production.

### Pertinence de la solution choisie (OAuth2 avec JWT)

J'ai choisi OAuth2 avec JWT pour plusieurs raisons :
- Il s'agit d'une solution sécurisée et largement utilisée pour la gestion des accès API.
- Les tokens JWT permettent de gérer les sessions de manière décentralisée, ce qui est adapté à des environnements scalables.
- La solution est idéale pour des API modernes avec une architecture distribuée.