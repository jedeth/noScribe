# PROMPT POUR CLAUDE CODE - INSTALLATION AUTOMATIQUE OPENVINO

Copier-coller ce prompt dans Claude Code après avoir cloné le dépôt noScribe.

---

## 🎯 MISSION : Installation Complète et Autonome d'OpenVINO pour noScribe

Tu es un expert en installation et configuration de systèmes d'IA. Ta mission est d'installer et configurer OpenVINO pour noScribe de manière **100% autonome** afin d'obtenir des transcriptions **2-6x plus rapides** sur mon processeur Intel.

### CONTEXTE
- Je viens de cloner le dépôt noScribe sur mon PC
- J'ai un processeur Intel (Core, Ultra, ou Xeon)
- Je veux transcrire des fichiers audio longs (10h+) le plus rapidement possible
- Je veux que tu gères TOUT : détection, installation, configuration, tests

### TON RÔLE
Tu es le **chef d'orchestre** de l'installation. Tu dois :
1. ✅ **Détecter** automatiquement mon environnement (OS, CPU, GPU)
2. ✅ **Installer** toutes les dépendances OpenVINO
3. ✅ **Configurer** noScribe pour les meilleures performances
4. ✅ **Tester** que tout fonctionne correctement
5. ✅ **Reporter** les résultats avec instructions finales

### ÉTAPES À SUIVRE (autonome, sans me demander de confirmation sauf si erreur critique)

#### PHASE 1 : DÉTECTION DE L'ENVIRONNEMENT (2 min)

1. **Détecte mon système d'exploitation**
   - Linux / Windows / macOS
   - Architecture (x86_64, ARM, etc.)

2. **Détecte mon processeur**
   - Est-ce un Intel ? (obligatoire pour OpenVINO)
   - Modèle exact (Core i5/i7/i9, Ultra, Xeon, etc.)
   - Nombre de cœurs P et E (si applicable)

3. **Détecte mon GPU Intel (si présent)**
   - iGPU Intel (Iris Xe, UHD Graphics, Arc)
   - Drivers installés ou non

4. **Vérifie Python**
   - Version (doit être 3.8+)
   - Environnement virtuel actif ou non
   - Packages actuels (pip freeze)

**ACTION :** Crée un rapport détaillé de mon système et affiche-le.

#### PHASE 2 : INSTALLATION DES DÉPENDANCES (5-10 min)

5. **Sauvegarde l'état actuel**
   - Backup des packages pip actuels
   - Backup de config.yml (si existe)

6. **Installe les dépendances OpenVINO**
   - Utilise le fichier requirements approprié :
     - Linux → `environments/requirements_linux.txt`
     - Windows → `environments/requirements_win_cpu.txt`
     - macOS Intel → `environments/requirements_macOS_x86_64.txt`

   **Commande :** `pip install -r <fichier_requirements>`

7. **Vérifie l'installation**
   - Teste : `python -c "import openvino; import openvino_genai; print('OK')"`
   - Teste : `python -c "from whisper_openvino import WhisperOpenVINO; print('OK')"`
   - Si échec → réessaye avec `pip install --upgrade openvino openvino-genai`

**ACTION :** Affiche un rapport d'installation (succès/échec pour chaque module).

#### PHASE 3 : DÉTECTION DES DEVICES OPENVINO (2 min)

8. **Liste les devices OpenVINO disponibles**
   ```python
   from openvino.runtime import Core
   core = Core()
   devices = core.available_devices
   print(f"Devices: {devices}")
   ```

9. **Détermine le meilleur device**
   - GPU Intel détecté ? → Utiliser GPU (4-6x speedup)
   - Sinon CPU Intel → Utiliser CPU (2-3x speedup)

10. **Affiche les capacités**
    - Pour chaque device, affiche le nom complet
    - Indique le device qui sera utilisé par défaut

**ACTION :** Affiche un rapport des devices avec recommandation.

#### PHASE 4 : CONFIGURATION OPTIMALE (3 min)

11. **Localise le fichier config.yml**
    - Linux : `~/.config/noScribe/config.yml`
    - Windows : `%APPDATA%\noScribe\config.yml`
    - macOS : `~/Library/Application Support/noScribe/config.yml`

    Si absent → informe que la config sera créée au premier lancement de noScribe

12. **Si config.yml existe, optimise-le**
    - Backup config.yml actuel
    - Applique la configuration "Balanced" (recommandée) :
      ```yaml
      whisper_compute_type: int8
      whisper_beam_size: 5
      whisper_temperature: 0.0
      voice_activity_detection_threshold: 0.5
      ```
    - Sauvegarde le nouveau config.yml

13. **Crée un script de test personnalisé**
    - Génère `my_openvino_test.py` avec :
      - Test des imports
      - Détection CPU/GPU
      - Liste des devices
      - Simulation de charge WhisperOpenVINO

**ACTION :** Affiche les modifications appliquées à config.yml.

#### PHASE 5 : TESTS COMPLETS (3 min)

14. **Exécute le script de test**
    - Lance `python my_openvino_test.py`
    - Capture et affiche les résultats

15. **Vérifie l'intégration noScribe**
    - Vérifie que `whisper_openvino.py` est présent
    - Vérifie que `noScribe.py` contient l'import OpenVINO (ligne ~53-60)
    - Confirme que `should_use_openvino()` retourne True

16. **Test de simulation (optionnel si pas de fichier audio)**
    - Si un fichier audio court existe dans le dépôt, teste une transcription
    - Sinon, skip et indique que l'utilisateur devra tester manuellement

**ACTION :** Affiche un rapport de tests avec statut (✅ ou ❌) pour chaque test.

#### PHASE 6 : RAPPORT FINAL ET INSTRUCTIONS (1 min)

17. **Génère un rapport complet d'installation**
    - Résumé de la détection hardware
    - Liste des packages installés (versions)
    - Device OpenVINO qui sera utilisé
    - Configuration appliquée
    - Résultats des tests
    - Performance attendue pour 10h d'audio

18. **Donne les instructions finales**
    - Comment lancer noScribe : `python noScribe.py`
    - Ce qu'il faut chercher dans les logs : `🚀 Intel hardware detected`
    - Avertissement première transcription (conversion 5-10 min)
    - Où trouver la documentation : `GUIDE_INSTALLATION_RAPIDE.md`

19. **Crée un fichier récapitulatif**
    - Génère `INSTALLATION_REPORT_<date>.txt` avec tout le rapport
    - Sauvegarde dans le répertoire noScribe

**ACTION :** Affiche le rapport final en couleurs/emojis pour clarté.

### RÈGLES IMPORTANTES

1. **AUTONOMIE MAXIMALE**
   - Ne me demande PAS de confirmation à chaque étape
   - Exécute TOUTES les commandes automatiquement
   - Affiche seulement les résultats importants

2. **GESTION DES ERREURS**
   - Si une étape échoue, essaye une solution alternative
   - Si échec critique, STOP et explique clairement le problème
   - Propose des solutions pour que je corrige

3. **COMMUNICATION CLAIRE**
   - Utilise des emojis pour les statuts : ✅ ❌ ⚠️ 🚀 📊
   - Affiche la progression : "PHASE 1/6 : Détection..."
   - Résume chaque phase avant de passer à la suivante

4. **PERFORMANCE D'ABORD**
   - L'objectif est d'obtenir le **maximum de vitesse**
   - Privilégie GPU > CPU si disponible
   - Applique INT8 quantization par défaut
   - Configure beam_size=5 (bon équilibre)

5. **DOCUMENTATION**
   - À chaque étape, indique où trouver plus d'infos
   - Référence les fichiers : `GUIDE_INSTALLATION_RAPIDE.md`, etc.
   - Crée des logs détaillés pour debug si nécessaire

### FORMAT DE SORTIE ATTENDU

```
═══════════════════════════════════════════════════════════════
 INSTALLATION AUTOMATIQUE OPENVINO POUR NOSCRIBE
 Chef d'orchestre : Claude Code
═══════════════════════════════════════════════════════════════

📋 PHASE 1/6 : Détection de l'environnement
  ✅ Système : Linux x86_64
  ✅ Processeur : Intel Core Ultra 7 155H (16 cores: 6P+8E+2LP)
  ✅ GPU Intel : Iris Xe Graphics (iGPU détecté)
  ✅ Python : 3.11.5
  ⚠️  Pas d'environnement virtuel (recommandé mais OK)

🔧 PHASE 2/6 : Installation des dépendances
  ✅ Backup créé : /tmp/packages_backup_20250105.txt
  ✅ openvino 2025.0 installé
  ✅ openvino-genai installé
  ✅ optimum[openvino] installé
  ✅ nncf 2.8.0 installé
  ✅ whisper_openvino.py importé avec succès

📊 PHASE 3/6 : Détection devices OpenVINO
  ✅ Devices disponibles : ['CPU', 'GPU.0']
  ✅ GPU.0 : Intel Iris Xe Graphics (Gen12)
  🚀 Device sélectionné : GPU.0 (speedup 4-6x attendu)

⚙️  PHASE 4/6 : Configuration optimale
  ✅ Config trouvé : ~/.config/noScribe/config.yml
  ✅ Backup créé : config.yml.backup_20250105_143022
  ✅ whisper_compute_type: default → int8
  ✅ whisper_beam_size: 1 → 5
  ✅ whisper_temperature: 0.0 (déjà OK)

🧪 PHASE 5/6 : Tests complets
  ✅ Import openvino : OK
  ✅ Import whisper_openvino : OK
  ✅ Détection Intel : OK
  ✅ should_use_openvino() : True
  ✅ Test simulation charge : OK

📝 PHASE 6/6 : Rapport final
  ✅ Installation réussie à 100%
  ✅ Rapport sauvegardé : INSTALLATION_REPORT_20250105.txt

═══════════════════════════════════════════════════════════════
 INSTALLATION TERMINÉE AVEC SUCCÈS ! 🎉
═══════════════════════════════════════════════════════════════

🚀 PERFORMANCE ATTENDUE (pour 10h d'audio) :
  • Avant (faster-whisper) : ~20 heures
  • Après (OpenVINO iGPU) : ~3-5 heures (4-6x plus rapide !)

📖 PROCHAINES ÉTAPES :

  1. Lancez noScribe :
     python noScribe.py

  2. Vérifiez dans les logs :
     "🚀 Intel hardware detected - using OpenVINO"

  3. Première transcription (important !) :
     - Utilisez un fichier court (5-10 min) pour tester
     - La première fois prend 5-10 min (conversion du modèle)
     - Les transcriptions suivantes seront ultra-rapides

  4. Lancez votre transcription 10h :
     - Sélectionnez le modèle : large-v3
     - Attendu : 3-5 heures au lieu de 20h !

📚 DOCUMENTATION :
  • Guide rapide : cat GUIDE_INSTALLATION_RAPIDE.md
  • Troubleshooting : cat OPENVINO_OPTIMIZATION.md
  • Rapport détaillé : cat INSTALLATION_REPORT_20250105.txt

🆘 PROBLÈME ?
  • Relancez les tests : python my_openvino_test.py
  • Consultez le rapport : INSTALLATION_REPORT_20250105.txt
  • Documentation : GUIDE_INSTALLATION_RAPIDE.md

Bonne transcription ultra-rapide ! 🎊
```

### CE QUE JE NE VEUX PAS

❌ Me demander à chaque étape si je veux continuer
❌ Me demander de taper des commandes manuellement
❌ T'arrêter pour des warnings non critiques
❌ Des explications trop longues pendant l'installation

### CE QUE JE VEUX

✅ Exécution automatique de bout en bout
✅ Affichage clair de la progression
✅ Rapport final avec toutes les infos importantes
✅ Instructions claires pour utiliser noScribe
✅ Gestion intelligente des erreurs

### DÉMARRAGE

**Commence MAINTENANT l'installation !**

Je suis dans le répertoire du dépôt cloné. Lance la Phase 1 : Détection de l'environnement.

Utilise l'outil TodoWrite pour suivre ta progression à travers les 6 phases.

GO ! 🚀
