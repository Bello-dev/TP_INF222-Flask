#!/bin/bash
echo "=== DIAGNOSTIC RÉSEAU ==="
echo "Hostname actuel: $(hostname)"
echo "IP du conteneur: $(hostname -i)"

echo -e "\n1. Test de résolution DNS pour 'db':"
nslookup db || echo "❌ nslookup échoué"

echo -e "\n2. Contenu de /etc/hosts:"
cat /etc/hosts

echo -e "\n3. Test ping vers 'db':"
ping -c 3 db || echo "❌ ping échoué"

echo -e "\n4. Test de connectivité port 5432:"
nc -z db 5432 && echo "✅ Port 5432 accessible" || echo "❌ Port 5432 non accessible"

echo -e "\n5. Variables d'environnement importantes:"
echo "DATABASE_URL: $DATABASE_URL"
echo "FLASK_APP: $FLASK_APP"
echo "PYTHONPATH: $PYTHONPATH"

echo -e "\n6. Test de connexion PostgreSQL direct:"
psql "$DATABASE_URL" -c "SELECT version();" 2>/dev/null && echo "✅ Connexion PostgreSQL OK" || echo "❌ Connexion PostgreSQL échouée"

echo -e "\n7. Processus en cours:"
ps aux | grep -E "(python|gunicorn)" || echo "Aucun processus Python trouvé"