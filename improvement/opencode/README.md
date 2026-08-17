# OpenCode + MCP (etape 4 du plan — NON TESTE en sandbox)

Objectif (mail de Juan) : remplacer les appels API manuels par l'agent
OpenCode, avec le RAG expose en serveur MCP que l'agent interroge lui-meme,
et une boucle d'erreurs autour (`agent_loop.py`).

## Mise en place (une fois)

```bash
# 1. OpenCode
curl -fsSL https://opencode.ai/install | bash    # ou npm i -g opencode-ai

# 2. Config : fusionner opencode.jsonc (ce dossier) dans
#    ~/.config/opencode/opencode.jsonc

# 3. Enregistrer la cle EdenAI (une seule fois)
opencode          # puis /connect -> EdenAI -> coller la cle du mail d'Adrian

# 4. Le serveur MCP a besoin de uv (pour uvx) et de Qdrant lance
curl -LsSf https://astral.sh/uv/install.sh | sh
sudo docker start qdrant
```

## Verification rapide

```bash
opencode run --model edenai/deepseek/deepseek-v4-flash "Say OK and nothing else"
```

Puis en interactif, verifier que l'outil MCP `qdrant-maude` apparait et
repond a une recherche ("look up owise in the Maude manual").

## Boucle d'erreurs

```bash
cd ~/improve-rag/improvement/opencode
source ../.venv/bin/activate
python agent_loop.py ../specs/maudec/maude/pow.txt -v
```

## Reserves connues (a verifier au premier run)

1. **Compatibilite de collection** : `mcp-server-qdrant` ecrit/lit ses
   propres noms de vecteurs FastEmbed ; la collection `maude_manual` de
   rag-system utilise un vecteur anonyme. S'il ne la lit pas, deux options :
   laisser le serveur creer sa propre collection et y re-indexer les memes
   chunks, ou ecrire un petit serveur MCP maison au-dessus de
   rag-system/rag/builder_ask.py (une trentaine de lignes avec fastmcp).
2. **Format de sortie de l'agent** : `agent_loop.py` suppose que l'agent
   ecrit le programme dans le fichier demande ; le nettoyage des blocs ```
   est gere, mais un agent bavard peut necessiter d'ajuster PROMPT_TURN.
3. **Budget** : 10 $ EdenAI ; DeepSeek flash est tres bon marche mais la
   boucle agentique consomme plus de tokens qu'un appel direct (outils,
   allers-retours MCP). Commencer par UN fichier avec -v avant toute serie.
