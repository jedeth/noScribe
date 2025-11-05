# 🚀 Guide d'Installation Rapide - OpenVINO pour Intel

## Pour transcriptions 10h : 20h → 3-5h ! (4-6x plus rapide)

Ce guide vous aide à installer et configurer OpenVINO pour **maximiser la vitesse** de transcription sur votre processeur Intel Ultra.

---

## ✅ Étape 1 : Installation Automatique

### Linux / macOS

```bash
# Rendez le script exécutable
chmod +x install_openvino.sh

# Lancez l'installation
./install_openvino.sh
```

### Windows

```powershell
# Ouvrez PowerShell dans le dossier noScribe
# Installez les dépendances
pip install -r environments\requirements_win_cpu.txt

# Testez l'installation
python test_openvino.py
```

**⏱️ Temps estimé : 5-10 minutes**

Le script va :
- ✅ Vérifier que vous avez un processeur Intel
- ✅ Installer OpenVINO et toutes les dépendances
- ✅ Détecter votre GPU Intel (iGPU) si disponible
- ✅ Tester que tout fonctionne

---

## ✅ Étape 2 : Configuration Optimale

```bash
# Lancez le configurateur
python3 configure_for_speed.py
```

**Choisissez un preset :**

1. **Ultra Rapide** : Vitesse maximum (pour brouillons)
   - 10h audio → ~2-4h traitement (iGPU) ou ~5-8h (CPU)

2. **Équilibré** ⭐ **RECOMMANDÉ**
   - 10h audio → ~3-5h traitement (iGPU) ou ~7-10h (CPU)
   - Excellente qualité

3. **Qualité** : Maximum qualité, toujours rapide
   - 10h audio → ~5-8h traitement (iGPU) ou ~10-15h (CPU)

**💡 Conseil :** Commencez par "Équilibré" (option 2)

---

## ✅ Étape 3 : Premier Test

### 3.1 Lancez noScribe

```bash
python3 noScribe.py
```

### 3.2 Vérifiez les logs

**Cherchez cette ligne dans l'interface :**

```
🚀 Intel hardware detected - using OpenVINO for 2-6x speedup
```

**Si vous voyez ça : PARFAIT ! ✅**

Si vous voyez `faster-whisper model loaded` à la place :
- OpenVINO n'est pas activé
- Relancez `./install_openvino.sh`
- Vérifiez `python test_openvino.py`

### 3.3 Test sur fichier court (5-10 min)

1. **Importez un fichier audio court** (5-10 minutes)
2. **Sélectionnez le modèle** : `large-v3` (ou `medium` pour plus de vitesse)
3. **Lancez la transcription**

**⚠️ PREMIÈRE FOIS = LENT (5-10 min)**
- Le modèle Whisper est converti en OpenVINO
- Modèle sauvegardé dans `~/.cache/noScribe/openvino_models/`

**✅ FOIS SUIVANTES = RAPIDE !**
- Le modèle converti est en cache
- Vous profitez du speedup 2-6x

---

## ✅ Étape 4 : Votre Transcription 10h

Une fois le test réussi :

1. **Importez votre fichier 10h**
2. **Vérifiez la config** :
   - Modèle : `large-v3` (ou `medium` pour vitesse max)
   - Les autres paramètres sont déjà optimisés par `configure_for_speed.py`
3. **Lancez !**

### Performance attendue

| Votre hardware | Temps de traitement | Speedup |
|----------------|---------------------|---------|
| Intel Ultra + iGPU | **3-5 heures** | **4-6x** ⭐ |
| Intel CPU moderne | **7-10 heures** | **2-3x** |
| Ancien Intel CPU | **10-15 heures** | **1.5-2x** |

*Comparer à 20h+ avec faster-whisper standard*

---

## 🔧 Résolution de Problèmes

### ❌ "OpenVINO not found"

```bash
# Réinstallez
pip install --upgrade openvino openvino-genai optimum[openvino] nncf

# Testez
python3 test_openvino.py
```

### ❌ "faster-whisper model loaded" (au lieu d'OpenVINO)

**Causes possibles :**

1. **Dépendances manquantes**
   ```bash
   python3 -c "import openvino; print('OK')"
   ```
   Si erreur → réinstallez

2. **Pas de processeur Intel**
   ```bash
   # Linux
   cat /proc/cpuinfo | grep "Intel"

   # Windows
   wmic cpu get name
   ```

3. **CUDA activé** (OpenVINO ne remplace pas CUDA)
   - Si vous avez une carte NVIDIA, gardez CUDA (déjà optimisé)

### ❌ Première transcription très lente

**NORMAL !** La conversion du modèle prend 5-10 min.

Vous verrez :
```
Converting Whisper model to OpenVINO format...
Downloading and converting from HuggingFace...
```

**Patience !** Les transcriptions suivantes seront **beaucoup plus rapides**.

### ❌ "Model conversion failed"

**Solutions :**

1. **Vérifiez l'espace disque** : Besoin de 2-4 GB
   ```bash
   df -h ~
   ```

2. **Vérifiez internet** : Premier téléchargement depuis HuggingFace
   ```bash
   ping huggingface.co
   ```

3. **Essayez un modèle plus petit**
   - Utilisez `medium` au lieu de `large-v3`

4. **Vérifiez les logs** pour l'erreur exacte

### ❌ Performance pas aussi rapide qu'attendu

**Checklist :**

- [ ] `whisper_compute_type: int8` dans config.yml
- [ ] Logs montrent "Using device 'GPU'" ou "Using device 'CPU'"
- [ ] Drivers Intel Graphics à jour (pour iGPU)
- [ ] Aucune autre app gourmande en arrière-plan
- [ ] Ordinateur branché (pas sur batterie)

---

## 📊 Benchmark Votre Système

Partagez vos résultats pour aider la communauté !

```bash
# Testez sur 1h d'audio
# Notez :
# - Processeur : Intel Core Ultra 7
# - Temps traitement : 15 minutes
# - Modèle : large-v3
# - Device : GPU.0 (iGPU)
# - Config : balanced (beam_size=5, int8)
```

**Partagez sur :** https://github.com/kaixxx/noScribe/issues

---

## 🎯 Configurations Recommandées

### Pour Vitesse Maximum (brouillons)

```yaml
whisper_model: medium
whisper_compute_type: int8
whisper_beam_size: 1
whisper_temperature: 0.0
```

**→ 10h audio en ~2-4h (iGPU)**

### Pour Équilibre (recommandé) ⭐

```yaml
whisper_model: large-v3
whisper_compute_type: int8
whisper_beam_size: 5
whisper_temperature: 0.0
```

**→ 10h audio en ~3-5h (iGPU)**

### Pour Qualité Maximum

```yaml
whisper_model: large-v3
whisper_compute_type: int8
whisper_beam_size: 10
whisper_temperature: 0.0
```

**→ 10h audio en ~5-8h (iGPU)**

---

## 📚 Ressources

- **Documentation complète** : `OPENVINO_OPTIMIZATION.md`
- **Test installation** : `python test_openvino.py`
- **Configuration** : `python configure_for_speed.py`
- **Support noScribe** : https://github.com/kaixxx/noScribe/issues
- **OpenVINO docs** : https://docs.openvino.ai/

---

## ✨ C'est Tout !

**En résumé :**

```bash
# 1. Installation (5-10 min)
./install_openvino.sh

# 2. Configuration (2 min)
python3 configure_for_speed.py

# 3. Test (5-10 min première fois)
python3 noScribe.py
# → Testez sur fichier court

# 4. Go ! (3-5h pour 10h audio)
# → Lancez votre transcription 10h
```

**Profitez du speedup 2-6x ! 🚀**

---

**Questions ?** Ouvrez une issue : https://github.com/kaixxx/noScribe/issues
