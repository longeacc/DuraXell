import subprocess
import os
import sys
from typing import Iterator, Dict

class CLIRunner:
    """Wrapper pour exécuter des commandes CLI (via subprocess)."""
    
    @staticmethod
    def run_command(command: str) -> Iterator[str]:
        """
        Exécute une ligne de commande et retourne la sortie ligne par ligne.
        
        Args:
            command (str): La commande système à exécuter.
            
        Yields:
            str: Chaque ligne de la sortie standard.
        """
        # Exécuter les commandes de CLI depuis la racine du projet (2 niveaux au-dessus)
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        
        # Mettre à jour vers le python de l'environnement virtuel pour éviter le mauvais PATH
        venv_python = os.path.join(root_dir, ".venv", "Scripts", "python.exe")
        if os.path.exists(venv_python):
            command = command.replace("python ", f"\"{venv_python}\" ")
        else:
            command = command.replace("python ", f"\"{sys.executable}\" ")

        process = subprocess.Popen(
            command,
            shell=True,
            cwd=root_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        if process.stdout:
            for line in process.stdout:
                yield line
        process.wait()


class MockCLIRunner:
    """Wrapper mock pour simuler des commandes CLI sans exécution pure."""
    
    MOCK_RESPONSES: Dict[str, list[str]] = {
        "extract": [
            "Initialisation du pipeline...",
            "Chargement du module RULES...",
            "Entités détectées : {'ER': 'Positif', 'Ki67': '20%'}",
            "Rendement d'extraction (Yield) = 0.91",
            "Terminé."
        ],
        "batch": [
            "Analyse du dossier en cours...",
            "10 / 100 rapports traités...",
            "50 / 100 rapports traités...",
            "100 / 100 rapports traités...",
            "Traitement batch terminé. L2 Metrics calculées."
        ],
        "metrics": [
            "Calcul de l'entropie de Shannon...",
            "Te=0.92 He=0.88 R=0.94",
            "Mise à jour metrics terminée."
        ],
        "tree": [
            "Génération de l'arbre...",
            "Arbre structurel exporté vers tree.pdf"
        ],
        "evaluate": [
            "Évaluation sur le dataset de test :",
            "Précision globale : 0.89",
            "Rappel global     : 0.90",
            "F1 Score           : 0.895"
        ],
        "serve": [
            "Démarrage du serveur REST sur http://127.0.0.1:8000...",
            "API Prête."
        ],
        "info": [
            "OS : Windows/Linux Mock",
            "Python : 3.x",
            "Dépendances OK."
        ]
    }

    @staticmethod
    def run_command(command: str, type_cmd: str) -> Iterator[str]:
        """
        Simule l'exécution d'une commande système et retourne du texte progressif.
        
        Args:
            command (str): La commande d'intention.
            type_cmd (str): Le type de réponse du mock défini dans le dict.
            
        Yields:
            str: Les lignes mock.
        """
        yield f"$ {command}\n"
        import time
        responses = MockCLIRunner.MOCK_RESPONSES.get(type_cmd, ["Commande inconnue."])
        for line in responses:
            time.sleep(0.3)
            yield line + "\n"
