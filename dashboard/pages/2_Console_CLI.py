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

    display_str = f"python main.py --action {selection}"
    exec_str = f"python main.py {selection}"
    
    # Variables pour nettoyage post-exécution
    import os
    import tempfile
    temp_dir = None
    
    # Zone d'inputs dynamiques
    if selection == "extract":
        text_input = st.text_area("Texte clinique", height=150, placeholder="Entrez le rapport clinique ici...")
        if text_input:
            display_str += f' --text "{text_input[:20]}..."'
            # On échappe les guillemets pour le terminal et on map vers 'extract-all' + '--doc'
            safe_text = text_input.replace('"', '\\"')
            exec_str = f'python main.py extract-all --doc "{safe_text}"'
        else:
            exec_str = "python main.py extract-all"
    elif selection == "batch":
        upload_files = st.file_uploader("Importer fichiers txt", accept_multiple_files=True)
        if upload_files:
            display_str += " --inputs [files]"
            # On crée un dossier temporaire pour stocker les fichiers du batch
            temp_dir = tempfile.mkdtemp()
            for f in upload_files:
                file_path = os.path.join(temp_dir, f.name)
                with open(file_path, "wb") as out:
                    out.write(f.getbuffer())
            exec_str += f' --input_dir "{temp_dir}"'
            
    execute = st.button("▶ Exécuter", type="primary")
    
    if execute:
        st.info(f"Lancement : `{display_str}`")
        
        output_placeholder = st.empty()
        full_logs = ""
        
        if mock_mode:
            runner = MockCLIRunner.run_command(display_str, selection)
        else:
            runner = CLIRunner.run_command(exec_str)
            
        with st.spinner("Exécution en cours..."):
            for line in runner:
                # Capture terminal ansi ou output
                full_logs += line
                output_placeholder.code(full_logs, language="bash")
                
        st.success("Exécution terminée.")
        
        # Affichage de l'arbre PDF généré
        if selection == "tree":
            import os
            import base64
            
            root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
            
            # Recherche du fichier PDF généré
            possible_paths = [
                os.path.join(root_dir, "tree.pdf"),
                os.path.join(root_dir, "decision_tree.pdf"),
                os.path.join(root_dir, "Results", "tree.pdf"),
                os.path.join(root_dir, "Results", "figures", "decision_tree_visualization.png")
            ]
            
            filepath = None
            for p in possible_paths:
                if os.path.exists(p):
                    filepath = p
                    break
                    
            if filepath:
                st.markdown("---")
                st.subheader("🌳 Visualisation de l'Arbre Structurel")
                
                if filepath.endswith('.png'):
                    st.image(filepath, use_column_width=True)
                else:
                    with open(filepath, "rb") as f:
                        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                    
                    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
                    st.markdown(pdf_display, unsafe_allow_html=True)
            else:
                st.info("ℹ️ L'arbre n'a pas pu être chargé depuis le disque. Il se peut qu'il n'ait pas été créé (notamment en Mode Démonstration).")
                
        # Nettoyage batch si nécessaire
        if temp_dir and os.path.exists(temp_dir):
            import shutil
            try:
                shutil.rmtree(temp_dir)
            except Exception:
                pass

if __name__ == "__main__":
    main()