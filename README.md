# Support AI Agent (LangFlow + FastAPI)  
Ce projet fournit un **agent de support client intelligent** reposant sur :  
- **LangFlow** pour la logique d'agent + RAG  
- **FastAPI** pour exposer une API REST propre  
- **Docker** pour un déploiement simple et reproductible  
- **Flows LangFlow** exportés au format JSON, inclus dans `flows/`  

L'agent est capable de :  
- Comprendre la question de l'utilisateur  
- Analyser l'intention (question, incident, demande de fonctionnalité, facturation...)  
- Activer un RAG pour rechercher la réponse dans une base vectorielle  
- Déterminer s'il faut créer un ticket  
- Générer un JSON structuré compatible ticketing  

---  

## Contenu du dossier `flows/`  
Le dossier **flows/** contient deux fichiers JSON :  
```code
flows/
├── load_docs_into_vector_store.json    # Flow de création et mise à jour de la base RAG
└── support_helpdesk.json      # Flow principal utilisé par l’API backend
```  
Ces fichiers sont **directement importables dans LangFlow** via un glisser/déposer dans l'interface de LangFlow.  

1. `load_docs_into_vector_store.json`  
Ce flow :  
- Charge vos documents (`docs/`)  
- Lit et nettoie le texte  
- Génère les embeddings  
- Les stocke dans **Chroma DB**  

2. `support_helpdesk.json`  
Ce flow :  
- Analyse l'intention  
- Interroge le vector store  
- Construit le prompt final  
- Génère un JSON structuré contenant la réponse + ticket (si nécessaire)  
Ce flow est celui appelé via l'API backend.  

---  

## Architecture du projet  
```code
.
├── app/
│   ├── main.py
│   ├── langflow_client.py
│   ├── config.py
│   ├── schemas.py
│   ├── requirements.txt
│   ├── .env
│
├── flows/
│   ├── vload_docs_into_vector_store.json
│   └── support_helpdesk.json
│
├── docs/                     # Documents indexés par le RAG
│
├── Dockerfile
├── docker-compose.yml
└── README.md
```  

---  

## Installation  

1. Cloner le projet  
```code
git clone <repo_url>
cd agent-support-ai
```  

2. Importer les flows dans LangFlow  
Ouvrir LangFlow -> **Import Flow** -> sélectionner :  
- `flows/load_docs_into_vector_store.json`  
- `flows/support_helpdesk.json`  

Les flows seront automatiquement disponibles et prêts à l'usage (il faudra juste ajouter les clés API)  

3. Configurer `.env`  
```code
cp .env.example .env
```  

Puis renseigner :  
```code
LANGFLOW_URL=http://host.docker.internal:7860
LANGFLOW_FLOW_ID=<ID_du_flow_agent_support_flow>
LANGFLOW_API_KEY=<votre_api_key_langflow>
```  
Le `LANGFLOW_FLOW_ID` doit correspondre à l'**ID du flow support_helpdesk.json**, après import.  

4. Lancer le backend  
```code
docker compose up -d --build
```  

L'API démarre sur :  
```code
http://localhost:8000
```  

---  

## Utilisation  
**Charger la base RAG**  
1. Ajouter vos `.txt/.pdf/.docx` dans `docs/`  
2. Ouvrir le flow `load_docs_into_vector_store.json`  
3. Lancer une exécution ("Run")  

**Appeler l'agent via API**  
```code
POST http://localhost:8000/agent/query
{
  "message": "Comment changer mon mot de passe ?"
}
```  

**Réponse typique**  
```code
{
  "answer": "Pour changer votre mot de passe...",
  "intent": "question",
  "needs_ticket": false,
  "ticket": null,
  "ticket_created": false,
  "metadata": {
    "confidence": 0.95
  }
}
```  

**Exemple incluant ticket**  
```code
{
  "answer": "Une erreur 500 est une erreur interne du serveur...",
  "intent": "incident",
  "needs_ticket": true,
  "ticket": {
    "title": "Erreur 500 - Erreur interne du serveur",
    "description": "L'utilisateur rencontre une erreur 500",
    "priority": "medium",
    "category": "incident",
    "user_email": "test@example.com"
  },
  "ticket_created": false
}
```  

---  

## Personnalisation  
- Modifier les prompts dans LangFlow  
- Ajouter/supprimer des documents dans `docs/`  
- Modifier les instructions de génération de ticket  
- Changer le modèle LLM utilisé dans le flow  

---  

## Roadmap  
- Intégration à un système de ticketing (Zendesk, n8n, Freshdesk, ...)  
- Gestion de session multi-turn persistantes  
- Tableau de bord admin + visualisation des logs  
- Optimisation RAG (réecriture de requête, chunking dynamique, ...)  
