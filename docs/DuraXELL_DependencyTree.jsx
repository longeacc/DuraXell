import { useState } from "react";

// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
// PALETTE
// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
const C = {
  data:      "#37474F",  // donnÃ©es brutes
  ner:       "#1B5E20",  // pipeline NER
  metrics:   "#0D47A1",  // mÃ©triques ESMO2025
  decision:  "#4A148C",  // arbre de dÃ©cision
  rest:      "#880E4F",  // REST-interface
  cascade:   "#BF360C",  // cascade/orchestrateur
  connector: "#4E342E",  // connecteurs
  config:    "#E65100",  // fichiers de config pivots
  eval:      "#006064",  // Ã©valuation / scoring
  entry:     "#1A237E",  // points d'entrÃ©e (main, notebook)
  output:    "#212121",  // sorties finales
  test:      "#37474F",  // tests
};

// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
// NODES  {id, x, y, w, h, c, label, sub, bold?}
// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
const N = {
  // â•â•â•â•â•â• COUCHE 0 â€” DONNÃ‰ES D'ENTRÃ‰E (y=30) â•â•â•â•â•â•
  brat_train: {x:40,   y:30,  w:190, h:55, c:C.data,    label:"NER/data/Breast/",   sub:"train/ val/ test/ (*.txt + *.ann)"},
  lung_data:  {x:250,  y:30,  w:165, h:55, c:C.data,    label:"NER/data/Lung/",     sub:"Ã€ crÃ©er â€” extension poumon"},
  eval_csv:   {x:430,  y:30,  w:230, h:55, c:C.data,    label:"breast_cancer_biomarker_eval_summary.csv", sub:"donnÃ©es existantes"},
  consumtion: {x:680,  y:30,  w:215, h:55, c:C.data,    label:"Consumtion_of_Duraxell.csv", sub:"Suivi eco2ai existant"},
  eco2ai:     {x:915,  y:30,  w:120, h:55, c:C.data,    label:"eco2ai",             sub:"lib externe"},

  // â•â•â•â•â•â• COUCHE 1 â€” PIPELINE NER (y=150) â•â•â•â•â•â•
  convert:    {x:40,   y:150, w:195, h:50, c:C.ner,     label:"1convert_brat_to_conll.py",  sub:"BRAT â†’ train.conll"},
  sweep:      {x:260,  y:150, w:160, h:50, c:C.ner,     label:"2sweep_ner.py",              sub:"PubMedBERT / CancerBERT â€” sweep F1"},
  infer:      {x:445,  y:150, w:135, h:50, c:C.ner,     label:"3infer.py",                  sub:"InfÃ©rence â†’ prÃ©dictions"},
  pred_brat:  {x:605,  y:150, w:180, h:50, c:C.ner,     label:"4predict_to_brat.py",        sub:"prÃ©dictions â†’ BRAT"},
  eval_ner:   {x:810,  y:150, w:180, h:50, c:C.ner,     label:"5evaluate_ner.py",           sub:"F1/P/R par entitÃ©"},
  
  // Sorties intermÃ©diaires NER
  conll:      {x:40,   y:238, w:130, h:35, c:C.output,  label:"train.conll",        sub:""},
  best_model: {x:260,  y:238, w:150, h:35, c:C.output,  label:"models/best_model/", sub:"meilleur checkpoint"},
  sweep_csv:  {x:445,  y:238, w:150, h:35, c:C.output,  label:"sweep_results.csv",  sub:"hyperparams + F1"},

  // â•â•â•â•â•â• COUCHE 2 â€” MÃ‰TRIQUES ESMO2025 (y=330) â•â•â•â•â•â•
  te_mod:     {x:30,   y:330, w:165, h:65, c:C.metrics, label:"E_templatability.py", sub:"templatabilityScorer\ncompute(entity) â†’ Te âˆˆ [0,1]"},
  he_mod:     {x:215,  y:330, w:165, h:65, c:C.metrics, label:"E_homogeneity.py",   sub:"HomogeneityScorer\ncompute(entity) â†’ He âˆˆ [0,1]"},
  risk_mod:   {x:400,  y:330, w:165, h:65, c:C.metrics, label:"E_risk_context.py",  sub:"RiskContextScorer\ncompute(entity) â†’ R âˆˆ [0,1]"},
  freq_mod:   {x:585,  y:330, w:165, h:65, c:C.metrics, label:"E_frequency.py",     sub:"FrequencyScorer\ncompute(entity) â†’ Freq"},
  yield_mod:  {x:770,  y:330, w:185, h:65, c:C.metrics, label:"E_annotation_yield.py", sub:"AnnotationYieldScorer\ncompute(entity) â†’ Yield âˆˆ [0,1]"},
  feas_mod:   {x:975,  y:330, w:165, h:65, c:C.metrics, label:"E_feasibility_NER.py",sub:"FeasibilityScorer\ncompute(entity) â†’ Feas"},

  // â•â•â•â•â•â• COUCHE 3 â€” ARBRE DE DÃ‰CISION (y=470, gauche) â•â•â•â•â•â•
  arbre:      {x:300,  y:470, w:255, h:75, c:C.decision, label:"E_creation_arbre_decision.py", sub:"DecisionTree\n6 critÃ¨res Ã— 6 feuilles â†’ recommandation", bold:true},
  thresh_doc: {x:40,   y:480, w:200, h:55, c:C.decision, label:"THRESHOLDS_JUSTIFICATION.md", sub:"TE_HIGH/LOW HE_HIGH\nRISK_LOW YIELD_MIN"},

  // â•â•â•â•â•â• COUCHE 3 â€” REST ANNOTATION (y=330+, droite) â•â•â•â•â•â•
  rest_annot: {x:1180, y:330, w:185, h:65, c:C.rest,    label:"rest_annotator.py",  sub:"RESTAnnotator\nâ†’ BratAnnotation[] (pilote 40 docs)"},
  yield_calc: {x:1390, y:330, w:175, h:65, c:C.rest,    label:"yield_calculator.py", sub:"Yield empirique\nAnnotation timing"},
  rest_eval:  {x:1180, y:430, w:185, h:65, c:C.rest,    label:"rest_evaluator.py",  sub:"RESTEvaluator\nâ†’ RESTEntityReport"},
  rest_pipe:  {x:1390, y:430, w:175, h:55, c:C.rest,    label:"rest_pipeline.py",   sub:"driver REST complet"},

  // â•â•â•â•â•â• COUCHE 4 â€” FICHIER PIVOT (y=620, centre) â•â•â•â•â•â•
  dec_cfg:    {x:275,  y:620, w:305, h:80, c:C.config,  label:"â˜…  decision_config.json  â˜…", sub:"FICHIER PIVOT â€” gÃ©nÃ©rÃ© par arbre\nPilote CascadeOrchestrator | version: 2.0", bold:true},

  // â•â•â•â•â•â• COUCHE 4 â€” REST BRIDGE (y=540+, droite) â•â•â•â•â•â•
  rest_bridge:{x:1180, y:540, w:185, h:75, c:C.rest,    label:"rest_decision_bridge.py", sub:"RESTDecisionBridge\nâ˜… Validation croisÃ©e â˜…\nConcordance â‰¥ 80%", bold:true},
  conv_anal:  {x:1390, y:540, w:175, h:65, c:C.rest,    label:"convergence_analyzer.py", sub:"Analyse divergences\nâ†’ rest_convergence_plot.png"},
  demo_rest:  {x:1390, y:630, w:175, h:45, c:C.rest,    label:"demo_rest.py",        sub:"Script de dÃ©monstration"},

  // Sorties REST
  annot_json: {x:1180, y:700, w:195, h:38, c:C.output,  label:"annotation_yield_by_entity.json", sub:""},
  conv_json:  {x:1390, y:700, w:185, h:38, c:C.output,  label:"convergence_tree_vs_rest.json",  sub:""},

  // â•â•â•â•â•â• COUCHE 4 â€” VISUALISATIONS (y=780) â•â•â•â•â•â•
  viz_tree:   {x:40,   y:780, w:210, h:55, c:C.decision, label:"visualize_decision_tree.py", sub:"â†’ figures/decision_tree.png (.svg)"},
  sensit:     {x:640,  y:780, w:210, h:55, c:C.decision, label:"sensitivity_analysis.py",    sub:"Seuils Â±10%/Â±20% â†’ sensitivity_output.csv"},

  // â•â•â•â•â•â• COUCHE 5 â€” CONNECTEURS (y=900) â•â•â•â•â•â•
  bio_annot:  {x:40,   y:900, w:205, h:50, c:C.connector, label:"biomarker_brat_annotator.py", sub:"Rules/src/Breast/ â€” regex biomarqueurs"},
  rules_eval: {x:265,  y:900, w:170, h:50, c:C.connector, label:"rules_evaluator.py",          sub:"PrÃ©cision/Rappel des rÃ¨gles"},
  rules_conn: {x:460,  y:900, w:205, h:50, c:C.connector, label:"rules_cascade_connector.py",  sub:"RulesCascadeConnector\n.predict(text, entity)"},
  ner_conn:   {x:690,  y:900, w:205, h:50, c:C.connector, label:"ner_cascade_connector.py",    sub:"NERCascadeConnector\n.predict(text, entity)"},
  energy_tr:  {x:920,  y:900, w:195, h:50, c:C.connector, label:"energy_tracker.py",           sub:"EnergyTracker | eco2ai wrapper\n@contextmanager .measure()"},

  // â•â•â•â•â•â• COUCHE 6 â€” ORCHESTRATEUR CASCADE (y=1020) â•â•â•â•â•â•
  cascade:    {x:260,  y:1020,w:330, h:90, c:C.cascade,  label:"cascade_orchestrator.py",     sub:"â˜… PIÃˆCE MAÃŽTRESSE â˜…\nCascadeOrchestrator\nRules â†’ ML-CRF â†’ Transformer â†’ LLM\n.extract() | .extract_all() | .extract_batch()", bold:true},

  // RÃ¨gles Lung (parallÃ¨le)
  lung_rules: {x:940,  y:1020,w:175, h:55, c:C.connector, label:"Rules/Lung/\nlung_biomarker_rules.py", sub:"EGFR ALK ROS1 KRAS PD-L1"},

  // Tests
  tests:      {x:1155, y:900, w:195, h:55, c:C.test,    label:"ESMO2025/tests/",              sub:"test_*.py (8 fichiers)\npytest â€” unitaires + intÃ©gration"},

  // â•â•â•â•â•â• COUCHE 7 â€” Ã‰VALUATION COMPOSITE (y=1175) â•â•â•â•â•â•
  composite:  {x:100,  y:1175,w:255, h:70, c:C.eval,    label:"E_composite_scorer.py",       sub:"CompositeScorer\nC = 0.4Â·F1 + 0.3Â·Expl + 0.3Â·(1-E_norm)\nPareto analysis"},
  init_py:    {x:800,  y:1175,w:215, h:55, c:C.eval,    label:"ESMO2025/__init__.py",         sub:"Exports publics : 9 classes\n__all__ = [templatabilityScorer, ...]"},

  // â•â•â•â•â•â• COUCHE 8 â€” POINTS D'ENTRÃ‰E (y=1315) â•â•â•â•â•â•
  main_py:    {x:80,   y:1315,w:240, h:75, c:C.entry,   label:"main.py",                     sub:"â˜… CLI DuraXELL â˜…\n8 commandes : extract batch metrics\ntree rest evaluate serve info", bold:true},
  notebook:   {x:380,  y:1315,w:255, h:75, c:C.entry,   label:"DuraXELL_Pipeline.ipynb",      sub:"Notebook maÃ®tre reproductible\n7 sections â€” rÃ©sultats complets"},
  readme_md:  {x:690,  y:1315,w:175, h:60, c:C.entry,   label:"README.md",                   sub:"Documentation maÃ®tre\nInstallation + Usage"},
  audit_doc:  {x:885,  y:1315,w:175, h:60, c:C.entry,   label:"AUDIT_24FEV.md",              sub:"Ã‰tat des lieux\n+ ARCHITECTURE_RECAP.md"},

  // â•â•â•â•â•â• COUCHE 9 â€” SORTIES FINALES (y=1460) â•â•â•â•â•â•
  bench_perf: {x:30,   y:1460,w:175, h:40, c:C.output,  label:"benchmark_performance.csv",   sub:""},
  bench_expl: {x:220,  y:1460,w:185, h:40, c:C.output,  label:"benchmark_explainability.csv", sub:""},
  bench_energy:{x:420, y:1460,w:175, h:40, c:C.output,  label:"benchmark_energy.csv",        sub:""},
  bench_casc: {x:610,  y:1460,w:195, h:40, c:C.output,  label:"benchmark_cascade_vs_mono.csv",sub:""},
  fig_radar:  {x:820,  y:1460,w:175, h:40, c:C.output,  label:"figures/radar_trilemma.png",  sub:""},
  fig_bench:  {x:1010, y:1460,w:200, h:40, c:C.output,  label:"figures/benchmark_comparison.png", sub:""},
  bilan:      {x:1225, y:1460,w:170, h:40, c:C.output,  label:"BILAN_VACANCES.md",           sub:""},
  frugalite:  {x:1410, y:1460,w:195, h:40, c:C.output,  label:"conference_frugalite_*.md+.pptx", sub:""},
};

// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
// EDGES  [from, to, label, style]
// style: "main"=bleu, "gen"=orange, "val"=rose, "data"=gris, "test"=vert foncÃ©
// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
const EDGES = [
  // === DONNÃ‰ES â†’ NER ===
  ["brat_train","convert","BRAT","data"],
  ["convert","conll","â†’","data"],
  ["convert","sweep","CoNLL","data"],
  ["sweep","best_model","â†’","data"],
  ["sweep","sweep_csv","â†’","data"],
  ["sweep","infer","best_model","data"],
  ["infer","pred_brat","prÃ©dictions","data"],
  ["pred_brat","eval_ner","pred.brat","data"],
  ["brat_train","eval_ner","gold.brat","data"],

  // === DONNÃ‰ES â†’ MÃ‰TRIQUES ===
  ["brat_train","te_mod","corpus","data"],
  ["brat_train","he_mod","corpus","data"],
  ["brat_train","risk_mod","corpus","data"],
  ["brat_train","freq_mod","corpus","data"],
  ["brat_train","yield_mod","corpus","data"],
  ["brat_train","feas_mod","corpus","data"],
  ["bio_annot","yield_mod","rÃ¨gles","data"],

  // === MÃ‰TRIQUES â†’ ARBRE ===
  ["te_mod","arbre","Te","main"],
  ["he_mod","arbre","He","main"],
  ["risk_mod","arbre","R","main"],
  ["freq_mod","arbre","Freq","main"],
  ["yield_mod","arbre","Yield","main"],
  ["feas_mod","arbre","Feas","main"],

  // === ARBRE â†’ CONFIG ===
  ["arbre","dec_cfg","gÃ©nÃ¨re decision_config.json","gen"],
  ["arbre","thresh_doc","documente seuils","gen"],
  ["arbre","viz_tree","appelle","main"],
  ["dec_cfg","sensit","seuils Ã  tester","main"],

  // === CONFIG â†’ CASCADE ===
  ["dec_cfg","cascade","pilote mÃ©thode par entitÃ©","gen"],
  ["dec_cfg","rest_bridge","tree_decisions","val"],

  // === REST CHAIN ===
  ["brat_train","rest_annot","corpus pilote","data"],
  ["rest_annot","rest_eval","BratAnnotation[]","val"],
  ["yield_calc","rest_eval","Yield empirique","val"],
  ["rest_pipe","rest_annot","lance","val"],
  ["rest_pipe","rest_eval","Ã©value","val"],
  ["rest_pipe","rest_bridge","bridge","val"],
  ["rest_eval","rest_bridge","rest_decisions","val"],
  ["rest_bridge","conv_anal","ConvergenceReport","val"],
  ["rest_annot","annot_json","â†’","val"],
  ["rest_bridge","conv_json","â†’","val"],

  // === CONNECTORS â†’ CASCADE ===
  ["bio_annot","rules_conn","rÃ¨gles regex","main"],
  ["rules_eval","rules_conn","prÃ©cision","main"],
  ["infer","ner_conn","modÃ¨le","main"],
  ["best_model","ner_conn","weights","main"],
  ["rules_conn","cascade","RulesCascadeConnector","main"],
  ["ner_conn","cascade","NERCascadeConnector","main"],
  ["eco2ai","energy_tr","mesure kWh/CO2","data"],
  ["energy_tr","cascade","EnergyTracker","main"],
  ["energy_tr","consumtion","log","data"],

  // === CASCADE â†’ Ã‰VALUATION ===
  ["cascade","composite","ExtractionResult[]","main"],
  ["eval_ner","composite","F1 par entitÃ©","main"],
  ["eval_ner","bench_perf","â†’","gen"],

  // === COMPOSITE â†’ OUTPUTS ===
  ["composite","bench_perf","â†’","gen"],
  ["composite","bench_expl","â†’","gen"],
  ["composite","bench_energy","â†’","gen"],
  ["composite","bench_casc","â†’","gen"],
  ["composite","fig_radar","â†’","gen"],
  ["composite","fig_bench","â†’","gen"],

  // === VISUALISATIONS â†’ OUTPUTS ===
  ["viz_tree","fig_radar","â†’ tree.png","gen"],
  ["sensit","bench_casc","sensitivity_output.csv","gen"],

  // === INIT.PY ===
  ["te_mod","init_py","export","main"],
  ["he_mod","init_py","export","main"],
  ["risk_mod","init_py","export","main"],
  ["cascade","init_py","export","main"],
  ["composite","init_py","export","main"],

  // === TESTS ===
  ["te_mod","tests","test_templatability.py","test"],
  ["he_mod","tests","test_homogeneity.py","test"],
  ["risk_mod","tests","test_risk_context.py","test"],
  ["arbre","tests","test_decision_tree.py","test"],
  ["cascade","tests","test_cascade.py","test"],
  ["rest_bridge","tests","test_rest_bridge.py","test"],

  // === main.py â†’ tout ===
  ["main_py","cascade","orchestre","entry"],
  ["main_py","composite","benchmark","entry"],
  ["main_py","arbre","tree/calibrate","entry"],
  ["main_py","rest_pipe","rest","entry"],
  ["main_py","bilan","â†’","entry"],
  ["main_py","readme_md","â†’","entry"],

  // === NOTEBOOK ===
  ["notebook","cascade","section 5","entry"],
  ["notebook","composite","section 5","entry"],
  ["notebook","arbre","section 3","entry"],
  ["notebook","rest_bridge","section 4","entry"],
  ["notebook","frugalite","section 7","entry"],
  ["notebook","fig_radar","section 5","entry"],
];

// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
// HELPERS
// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
const EDGE_COLORS = {
  main:  "#64B5F6",  // bleu - flux principal
  gen:   "#FFB74D",  // orange - gÃ©nÃ¨re/crÃ©e
  val:   "#F48FB1",  // rose - validation REST
  data:  "#90A4AE",  // gris - donnÃ©es brutes
  test:  "#81C784",  // vert - tests
  entry: "#CE93D8",  // violet - points d'entrÃ©e
};

function getExit(n, targetN) {
  // Choix du cÃ´tÃ© de sortie selon la position relative
  const sc = { x: n.x + n.w/2, y: n.y + n.h/2 };
  const tc = { x: targetN.x + targetN.w/2, y: targetN.y + targetN.h/2 };
  const dy = tc.y - sc.y, dx = tc.x - sc.x;
  if (Math.abs(dy) > Math.abs(dx)) {
    // vertical dominant
    if (dy > 0) return { x: n.x + n.w/2, y: n.y + n.h, side:'bottom' };
    else        return { x: n.x + n.w/2, y: n.y,        side:'top'    };
  } else {
    if (dx > 0) return { x: n.x + n.w, y: n.y + n.h/2, side:'right' };
    else        return { x: n.x,        y: n.y + n.h/2, side:'left'  };
  }
}
function getEntry(n, sourceN) {
  const sc = { x: sourceN.x + sourceN.w/2, y: sourceN.y + sourceN.h/2 };
  const tc = { x: n.x + n.w/2,             y: n.y + n.h/2 };
  const dy = tc.y - sc.y, dx = tc.x - sc.x;
  if (Math.abs(dy) > Math.abs(dx)) {
    if (dy > 0) return { x: n.x + n.w/2, y: n.y,        side:'top'    };
    else        return { x: n.x + n.w/2, y: n.y + n.h,  side:'bottom' };
  } else {
    if (dx > 0) return { x: n.x,         y: n.y + n.h/2, side:'left'  };
    else        return { x: n.x + n.w,   y: n.y + n.h/2, side:'right' };
  }
}

function buildPath(from, to) {
  const sn = N[from], tn = N[to];
  if (!sn || !tn) return null;
  const s = getExit(sn, tn);
  const t = getEntry(tn, sn);
  const dx = Math.abs(t.x - s.x), dy = Math.abs(t.y - s.y);
  let cx1 = s.x, cy1 = s.y, cx2 = t.x, cy2 = t.y;
  if (s.side === 'bottom' || s.side === 'top') {
    cy1 = s.y + (s.side==='bottom' ? 1 : -1) * Math.max(30, dy * 0.45);
    cy2 = t.y + (t.side==='top'    ? -1 : 1) * Math.max(30, dy * 0.45);
    cx1 = s.x; cx2 = t.x;
  } else {
    cx1 = s.x + (s.side==='right' ? 1 : -1) * Math.max(30, dx * 0.45);
    cx2 = t.x + (t.side==='left'  ? -1 : 1) * Math.max(30, dx * 0.45);
    cy1 = s.y; cy2 = t.y;
  }
  return { path: `M ${s.x} ${s.y} C ${cx1} ${cy1}, ${cx2} ${cy2}, ${t.x} ${t.y}`, tx: (s.x+t.x)/2, ty: (s.y+t.y)/2 };
}

// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
// LAYER LABELS
// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
const LAYERS = [
  { y: 30,   h: 70,  label: "COUCHE 0 â€” DONNÃ‰ES D'ENTRÃ‰E", color:"#1C2B33" },
  { y: 145,  h: 130, label: "COUCHE 1 â€” PIPELINE NER", color:"#0A1F0C" },
  { y: 320,  h: 90,  label: "COUCHE 2 â€” MÃ‰TRIQUES ESMO2025  (Te Â· He Â· R Â· Freq Â· Yield)", color:"#0A1133" },
  { y: 455,  h: 200, label: "COUCHE 3 â€” ARBRE DE DÃ‰CISION  +  REST ANNOTATION", color:"#160A27" },
  { y: 670,  h: 130, label: "COUCHE 4 â€” FICHIER PIVOT  +  REST Ã‰VALUATION / BRIDGE", color:"#2D1200" },
  { y: 770,  h: 70,  label: "COUCHE 4bis â€” VISUALISATIONS & SENSIBILITÃ‰", color:"#1A0040" },
  { y: 880,  h: 80,  label: "COUCHE 5 â€” CONNECTEURS (Rules + NER + Energy)", color:"#1A0C08" },
  { y: 1010, h: 120, label: "COUCHE 6 â€” CASCADE ORCHESTRATOR  â˜… PIÃˆCE MAÃŽTRESSE â˜…", color:"#2C0A00" },
  { y: 1155, h: 100, label: "COUCHE 7 â€” Ã‰VALUATION COMPOSITE  +  __init__.py", color:"#002626" },
  { y: 1300, h: 100, label: "COUCHE 8 â€” POINTS D'ENTRÃ‰E (main.py Â· Notebook Â· Docs)", color:"#0A0A2A" },
  { y: 1445, h: 65,  label: "COUCHE 9 â€” SORTIES FINALES", color:"#111111" },
];

// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
// LEGEND
// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
const LEGEND_NODES = [
  { c: C.data,      label: "DonnÃ©es brutes / sources" },
  { c: C.ner,       label: "Pipeline NER" },
  { c: C.metrics,   label: "MÃ©triques ESMO2025" },
  { c: C.decision,  label: "Arbre de dÃ©cision" },
  { c: C.rest,      label: "REST-interface (Bazin)" },
  { c: C.cascade,   label: "Cascade Orchestrator" },
  { c: C.connector, label: "Connecteurs" },
  { c: C.config,    label: "Fichier pivot / config" },
  { c: C.eval,      label: "Ã‰valuation composite" },
  { c: C.entry,     label: "Points d'entrÃ©e" },
  { c: C.output,    label: "Sorties finales" },
];
const LEGEND_EDGES = [
  { c: EDGE_COLORS.main,  label: "Flux principal de donnÃ©es" },
  { c: EDGE_COLORS.gen,   label: "GÃ©nÃ©ration / crÃ©ation" },
  { c: EDGE_COLORS.val,   label: "Validation croisÃ©e REST" },
  { c: EDGE_COLORS.data,  label: "Transfert de donnÃ©es brutes" },
  { c: EDGE_COLORS.test,  label: "Tests unitaires / intÃ©gration" },
  { c: EDGE_COLORS.entry, label: "Points d'entrÃ©e CLI / notebook" },
];

// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
// COMPOSANT PRINCIPAL
// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
export default function DuraXELLDependencyTree() {
  const [hoveredNode, setHoveredNode] = useState(null);
  const [hoveredEdge, setHoveredEdge] = useState(null);
  const [showLabels, setShowLabels] = useState(true);

  const SVG_W = 1640, SVG_H = 1540;

  // Edges connectÃ©s au nÅ“ud survolÃ©
  const relatedEdges = hoveredNode
    ? new Set(EDGES.filter(([f,t]) => f===hoveredNode||t===hoveredNode).map((_,i)=>i))
    : null;

  return (
    <div style={{ background:"#0D0D1A", minHeight:"100vh", fontFamily:"'JetBrains Mono', monospace", padding:"16px" }}>
      
      {/* TITRE */}
      <div style={{ marginBottom:"12px", display:"flex", alignItems:"center", gap:"16px", flexWrap:"wrap" }}>
        <div>
          <h1 style={{ color:"#E3F2FD", fontSize:"18px", margin:0, fontWeight:700 }}>
            DuraXELL / ESMO2025 â€” Arbre des DÃ©pendances
          </h1>
          <p style={{ color:"#78909C", fontSize:"11px", margin:"2px 0 0" }}>
            Flux de donnÃ©es Â· Classes Â· Fonctions Â· EntrÃ©es/Sorties de chaque fichier
          </p>
        </div>
        <button
          onClick={() => setShowLabels(v => !v)}
          style={{ background:"#1E3A5F", color:"#90CAF9", border:"1px solid #1565C0", borderRadius:"6px",
                   padding:"4px 12px", cursor:"pointer", fontSize:"11px" }}>
          {showLabels ? "Masquer labels flÃ¨ches" : "Afficher labels flÃ¨ches"}
        </button>
      </div>

      {/* SVG PRINCIPAL */}
      <div style={{ overflow:"auto", border:"1px solid #1E3A5F", borderRadius:"8px" }}>
        <svg width={SVG_W} height={SVG_H} style={{ display:"block" }}>
          <defs>
            {Object.entries(EDGE_COLORS).map(([k,col]) => (
              <marker key={k} id={`arr-${k}`} markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
                <path d="M0,0 L0,6 L8,3 z" fill={col} />
              </marker>
            ))}
          </defs>

          {/* COUCHES (background) */}
          {LAYERS.map((l,i) => (
            <g key={i}>
              <rect x={0} y={l.y} width={SVG_W} height={l.h} fill={l.color} rx={0} />
              <text x={8} y={l.y + 12} fill="#2D3F52" fontSize="9" fontFamily="monospace" fontWeight="700">
                {l.label}
              </text>
            </g>
          ))}

          {/* EDGES */}
          {EDGES.map(([from, to, label, style], i) => {
            const result = buildPath(from, to);
            if (!result) return null;
            const { path, tx, ty } = result;
            const col = EDGE_COLORS[style] || EDGE_COLORS.main;
            const isHighlighted = relatedEdges && relatedEdges.has(i);
            const isHovered = hoveredEdge === i;
            const opacity = relatedEdges
              ? (isHighlighted ? 1 : 0.07)
              : (isHovered ? 1 : 0.35);
            const sw = isHighlighted || isHovered ? 2.5 : 1.2;
            return (
              <g key={i}
                 onMouseEnter={() => setHoveredEdge(i)}
                 onMouseLeave={() => setHoveredEdge(null)}
                 style={{ cursor:"default" }}>
                <path d={path} stroke={col} strokeWidth={sw+6} fill="none" opacity={0}
                      style={{ cursor:"pointer" }} />
                <path d={path} stroke={col} strokeWidth={sw} fill="none"
                      opacity={opacity}
                      markerEnd={`url(#arr-${style})`} />
                {showLabels && label && label !== "â†’" && (isHighlighted || isHovered || !relatedEdges) && (
                  <g>
                    <rect x={tx-28} y={ty-9} width={56} height={14}
                          fill="#0D0D1A" opacity={0.75} rx={3} />
                    <text x={tx} y={ty+2} textAnchor="middle" fill={col}
                          fontSize="7.5" fontFamily="monospace" opacity={opacity + 0.1}>
                      {label.length > 18 ? label.slice(0,17)+"â€¦" : label}
                    </text>
                  </g>
                )}
              </g>
            );
          })}

          {/* NODES */}
          {Object.entries(N).map(([id, n]) => {
            const isHov = hoveredNode === id;
            const isDim = relatedEdges && !relatedEdges
              ? false
              : hoveredNode && hoveredNode !== id
                && !EDGES.some(([f,t]) => (f===hoveredNode&&t===id)||(t===hoveredNode&&f===id));
            const lines = n.label.split('\n');
            const subLines = n.sub ? n.sub.split('\n') : [];
            const lineH = 13, padding = 8, topPad = 14;
            return (
              <g key={id}
                 onMouseEnter={() => setHoveredNode(id)}
                 onMouseLeave={() => setHoveredNode(null)}
                 style={{ cursor:"pointer" }}
                 opacity={isDim ? 0.25 : 1}>
                {/* Glow effect on hover */}
                {isHov && (
                  <rect x={n.x-4} y={n.y-4} width={n.w+8} height={n.h+8}
                        fill="none" stroke="white" strokeWidth="2" rx={10} opacity={0.6} />
                )}
                {/* Main box */}
                <rect x={n.x} y={n.y} width={n.w} height={n.h}
                      fill={n.c}
                      stroke={isHov ? "white" : "rgba(255,255,255,0.18)"}
                      strokeWidth={isHov ? 1.5 : 0.8}
                      rx={7} />
                {/* Bold border for key files */}
                {n.bold && (
                  <rect x={n.x+2} y={n.y+2} width={n.w-4} height={n.h-4}
                        fill="none" stroke="rgba(255,255,255,0.35)" strokeWidth="1.5"
                        rx={5} strokeDasharray="4,3" />
                )}
                {/* Label lines */}
                {lines.map((line, li) => (
                  <text key={li}
                        x={n.x + n.w/2}
                        y={n.y + topPad + li * lineH}
                        textAnchor="middle"
                        fill="white"
                        fontSize={lines.length > 1 ? "9" : "9.5"}
                        fontWeight="700"
                        fontFamily="monospace">
                    {line}
                  </text>
                ))}
                {/* Sub-label lines */}
                {subLines.map((line, li) => (
                  <text key={li}
                        x={n.x + n.w/2}
                        y={n.y + topPad + lines.length * lineH + 2 + li * 11}
                        textAnchor="middle"
                        fill="rgba(255,255,255,0.58)"
                        fontSize="7.5"
                        fontFamily="monospace">
                    {line}
                  </text>
                ))}
              </g>
            );
          })}
        </svg>
      </div>

      {/* LÃ‰GENDE */}
      <div style={{ marginTop:"16px", display:"flex", gap:"32px", flexWrap:"wrap" }}>
        {/* Nodes */}
        <div>
          <p style={{ color:"#64B5F6", fontSize:"11px", fontWeight:"700", margin:"0 0 6px", textTransform:"uppercase", letterSpacing:"1px" }}>
            Types de nÅ“uds
          </p>
          <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:"4px 16px" }}>
            {LEGEND_NODES.map((l,i) => (
              <div key={i} style={{ display:"flex", alignItems:"center", gap:"6px" }}>
                <div style={{ width:14, height:14, background:l.c, borderRadius:3, flexShrink:0 }} />
                <span style={{ color:"#B0BEC5", fontSize:"10px" }}>{l.label}</span>
              </div>
            ))}
          </div>
        </div>
        {/* Edges */}
        <div>
          <p style={{ color:"#64B5F6", fontSize:"11px", fontWeight:"700", margin:"0 0 6px", textTransform:"uppercase", letterSpacing:"1px" }}>
            Types de flÃ¨ches
          </p>
          <div style={{ display:"grid", gridTemplateColumns:"1fr", gap:"4px" }}>
            {LEGEND_EDGES.map((l,i) => (
              <div key={i} style={{ display:"flex", alignItems:"center", gap:"8px" }}>
                <svg width={40} height={12}>
                  <defs>
                    <marker id={`leg-${i}`} markerWidth="6" markerHeight="6" refX="5" refY="2.5" orient="auto">
                      <path d="M0,0 L0,5 L6,2.5 z" fill={l.c} />
                    </marker>
                  </defs>
                  <line x1={2} y1={6} x2={34} y2={6} stroke={l.c} strokeWidth={2} markerEnd={`url(#leg-${i})`} />
                </svg>
                <span style={{ color:"#B0BEC5", fontSize:"10px" }}>{l.label}</span>
              </div>
            ))}
          </div>
        </div>
        {/* Instructions */}
        <div style={{ marginLeft:"auto" }}>
          <p style={{ color:"#64B5F6", fontSize:"11px", fontWeight:"700", margin:"0 0 6px", textTransform:"uppercase", letterSpacing:"1px" }}>
            Navigation
          </p>
          <p style={{ color:"#78909C", fontSize:"10px", margin:"0 0 3px" }}>ðŸ–± Survoler un nÅ“ud â†’ met en Ã©vidence ses dÃ©pendances</p>
          <p style={{ color:"#78909C", fontSize:"10px", margin:"0 0 3px" }}>ðŸ–± Survoler une flÃ¨che â†’ affiche le label</p>
          <p style={{ color:"#78909C", fontSize:"10px", margin:0 }}>â­ Bordure pointillÃ©e = fichiers pivot / piÃ¨ces maÃ®tresses</p>
        </div>
      </div>

      {/* INFO NODE */}
      {hoveredNode && N[hoveredNode] && (
        <div style={{ marginTop:"12px", background:"#1E2A38", border:"1px solid #1565C0", borderRadius:"8px", padding:"12px", maxWidth:"500px" }}>
          <p style={{ color:"#64B5F6", fontWeight:"700", margin:"0 0 6px", fontSize:"12px" }}>
            ðŸ“„ {hoveredNode}
          </p>
          <p style={{ color:"white", fontSize:"11px", margin:"0 0 4px", fontWeight:"600" }}>
            {N[hoveredNode].label.replace(/\n/g,' ')}
          </p>
          {N[hoveredNode].sub && (
            <p style={{ color:"#90CAF9", fontSize:"10px", margin:0 }}>
              {N[hoveredNode].sub.replace(/\n/g,' Â· ')}
            </p>
          )}
          <div style={{ marginTop:"8px", display:"flex", gap:"20px" }}>
            <div>
              <p style={{ color:"#81C784", fontSize:"10px", margin:"0 0 3px", fontWeight:"600" }}>DÃ©pend de :</p>
              {EDGES.filter(([,t]) => t===hoveredNode).map(([f,,l],i) => (
                <p key={i} style={{ color:"#B0BEC5", fontSize:"10px", margin:"1px 0" }}>
                  â† {f} <span style={{ color:"#546E7A" }}>({l})</span>
                </p>
              ))}
            </div>
            <div>
              <p style={{ color:"#FFB74D", fontSize:"10px", margin:"0 0 3px", fontWeight:"600" }}>Alimente :</p>
              {EDGES.filter(([f]) => f===hoveredNode).map(([,t,l],i) => (
                <p key={i} style={{ color:"#B0BEC5", fontSize:"10px", margin:"1px 0" }}>
                  â†’ {t} <span style={{ color:"#546E7A" }}>({l})</span>
                </p>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}