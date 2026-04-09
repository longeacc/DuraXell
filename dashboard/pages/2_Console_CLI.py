import streamlit as st
from core.cli_runner import CLIRunner, MockCLIRunner

st.set_page_config(page_title="Console CLI", page_icon="🖥️", layout="wide")

CLI_COMMANDS = {
    "extract": "Extraction d'entités sur un texte",
    "batch": "Traitement batch de fichiers",
    "metrics": "Calcul des métriques L2",
    "tree": "Affichage de l'arbre de décision",
    "evaluate": "Évaluation sur corpus de test",
    "serve": "Lancement du serveur API",
    "info": "Informations système"
}

def main() -> None:
    st.title("🖥️ Console de Commandes CLI")
    
    mock_mode = st.sidebar.checkbox("Mode démonstration (Mock)", value=True)
    
    st.sidebar.subheader("Commandes Disponibles")
    selection = st.sidebar.radio("Sélectionnez l'action :", list(CLI_COMMANDS.keys()), format_func=lambda x: f"{x} - {CLI_COMMANDS[x]}")

    st.markdown(f"**Action active :** `{selection}` - {CLI_COMMANDS[selection]}")

    commande_str = f"python main.py --action {selection}"
    
    # Zone d'inputs dynamiques
    if selection == "extract":
        text_input = st.text_area("Texte clinique", height=150, placeholder="Entrez le rapport clinique ici...")
        if text_input:
            commande_str += f' --text "{text_input[:20]}..."'
    elif selection == "batch":
        upload = st.file_uploader("Importer fichiers txt", accept_multiple_files=True)
        if upload:
            commande_str += " --inputs [files]"
            
    execute = st.button("▶ Exécuter", type="primary")
    
    if execute:
        st.info(f"Lancement : `{commande_str}`")
        
        output_placeholder = st.empty()
        full_logs = ""
        
        if mock_mode:
            runner = MockCLIRunner.run_command(commande_str, selection)
        else:
            runner = CLIRunner.run_command(commande_str)
            
        with st.spinner("Exécution en cours..."):
            for line in runner:
                # Capture terminal ansi ou output
                full_logs += line
                output_placeholder.code(full_logs, language="bash")
                
        st.success("Exécution terminée.")

if __name__ == "__main__":
    main()