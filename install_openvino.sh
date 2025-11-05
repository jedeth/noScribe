#!/bin/bash
# Script d'installation OpenVINO pour noScribe
# Optimisation Intel CPU/GPU pour transcription 2-6x plus rapide

set -e  # Exit on error

echo "=================================================="
echo "  Installation OpenVINO pour noScribe"
echo "  Optimisation Intel CPU/GPU"
echo "=================================================="
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    REQUIREMENTS="environments/requirements_linux.txt"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    OS="windows"
    REQUIREMENTS="environments/requirements_win_cpu.txt"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    # Check if Intel Mac
    ARCH=$(uname -m)
    if [[ "$ARCH" == "x86_64" ]]; then
        REQUIREMENTS="environments/requirements_macOS_x86_64.txt"
        echo "✓ Mac Intel détecté"
    else
        echo "❌ ERREUR: OpenVINO ne fonctionne que sur Mac Intel, pas Apple Silicon"
        echo "   Votre Mac utilise Apple Silicon ($ARCH)"
        exit 1
    fi
else
    echo "❌ Système d'exploitation non supporté: $OSTYPE"
    exit 1
fi

echo "Système détecté: $OS"
echo "Fichier requirements: $REQUIREMENTS"
echo ""

# Check if running on Intel CPU
echo "Vérification du processeur..."
if [[ "$OS" == "linux" ]]; then
    CPU_INFO=$(cat /proc/cpuinfo | grep "model name" | head -1)
    if echo "$CPU_INFO" | grep -qi "intel"; then
        echo "✓ Processeur Intel détecté:"
        echo "  $CPU_INFO"
    else
        echo "⚠ ATTENTION: Processeur non-Intel détecté"
        echo "  $CPU_INFO"
        echo "  OpenVINO fonctionnera mais sans optimisations Intel"
        read -p "Continuer quand même ? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
elif [[ "$OS" == "macos" ]]; then
    CPU_INFO=$(sysctl -n machdep.cpu.brand_string)
    echo "✓ Processeur: $CPU_INFO"
fi
echo ""

# Check Python version
echo "Vérification de Python..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [[ $PYTHON_MAJOR -eq 3 ]] && [[ $PYTHON_MINOR -ge 8 ]]; then
    echo "✓ Python $PYTHON_VERSION (compatible)"
else
    echo "❌ Python 3.8+ requis, version actuelle: $PYTHON_VERSION"
    exit 1
fi
echo ""

# Check if virtual environment is active
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠ ATTENTION: Aucun environnement virtuel Python détecté"
    echo "  Il est recommandé d'utiliser un venv pour éviter les conflits"
    read -p "Continuer sans venv ? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "Pour créer et activer un venv:"
        echo "  python3 -m venv venv"
        echo "  source venv/bin/activate  # Linux/Mac"
        echo "  venv\\Scripts\\activate     # Windows"
        echo ""
        exit 1
    fi
else
    echo "✓ Environnement virtuel actif: $VIRTUAL_ENV"
fi
echo ""

# Backup existing installation
echo "Sauvegarde de la configuration actuelle..."
pip freeze > /tmp/noScribe_packages_backup_$(date +%Y%m%d_%H%M%S).txt
echo "✓ Backup créé dans /tmp/"
echo ""

# Install/upgrade pip
echo "Mise à jour de pip..."
python3 -m pip install --upgrade pip
echo ""

# Install requirements
echo "=================================================="
echo "  Installation des dépendances"
echo "  Cela peut prendre 5-10 minutes..."
echo "=================================================="
echo ""

if pip install -r "$REQUIREMENTS"; then
    echo ""
    echo "✓ Dépendances installées avec succès"
else
    echo ""
    echo "❌ Erreur lors de l'installation des dépendances"
    echo "   Consultez les messages d'erreur ci-dessus"
    exit 1
fi
echo ""

# Verify OpenVINO installation
echo "Vérification de l'installation OpenVINO..."
if python3 -c "import openvino; import openvino_genai; from optimum.intel import OVModelForSpeechSeq2Seq; import nncf; print('OpenVINO OK')" 2>/dev/null; then
    echo "✓ OpenVINO correctement installé"
else
    echo "❌ Erreur: OpenVINO non installé correctement"
    echo "   Essayez d'installer manuellement:"
    echo "   pip install openvino openvino-genai optimum[openvino] nncf"
    exit 1
fi
echo ""

# Check for GPU support (Linux only)
if [[ "$OS" == "linux" ]]; then
    echo "Vérification du support GPU Intel..."
    if python3 -c "from openvino.runtime import Core; core = Core(); devices = core.available_devices; print('GPU' if any('GPU' in d for d in devices) else 'NO_GPU')" 2>/dev/null | grep -q "GPU"; then
        echo "✓ GPU Intel détecté et supporté par OpenVINO"
        echo "  Vous bénéficierez de l'accélération iGPU (4-6x speedup)"
    else
        echo "⚠ Aucun GPU Intel détecté ou drivers manquants"
        echo "  Vous utiliserez le CPU (2-3x speedup, toujours excellent)"
        echo ""
        echo "  Pour activer le GPU Intel (optionnel):"
        echo "  - Installez les drivers Intel Graphics: https://www.intel.com/content/www/us/en/download/785597/"
        echo "  - Redémarrez votre système"
    fi
fi
echo ""

# Create test script
echo "Création du script de test..."
cat > test_openvino.py << 'EOTEST'
#!/usr/bin/env python3
# Test script for OpenVINO installation

import sys
import platform

print("=" * 60)
print("  Test de l'installation OpenVINO")
print("=" * 60)
print()

# Test 1: Import modules
print("Test 1: Import des modules...")
try:
    import openvino
    print(f"  ✓ openvino {openvino.__version__}")
except ImportError as e:
    print(f"  ❌ openvino: {e}")
    sys.exit(1)

try:
    import openvino_genai
    print(f"  ✓ openvino-genai")
except ImportError as e:
    print(f"  ❌ openvino-genai: {e}")
    sys.exit(1)

try:
    from optimum.intel import OVModelForSpeechSeq2Seq
    print(f"  ✓ optimum-intel")
except ImportError as e:
    print(f"  ❌ optimum-intel: {e}")
    sys.exit(1)

try:
    import nncf
    print(f"  ✓ nncf {nncf.__version__}")
except ImportError as e:
    print(f"  ❌ nncf: {e}")
    sys.exit(1)

print()

# Test 2: Check CPU
print("Test 2: Détection processeur...")
if platform.system() == "Linux":
    with open("/proc/cpuinfo", "r") as f:
        for line in f:
            if "model name" in line:
                cpu_name = line.split(":")[1].strip()
                print(f"  CPU: {cpu_name}")
                if "Intel" in cpu_name:
                    print(f"  ✓ Processeur Intel détecté")
                break
elif platform.system() == "Darwin":
    import subprocess
    cpu_name = subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"]).decode().strip()
    print(f"  CPU: {cpu_name}")
    if "Intel" in cpu_name:
        print(f"  ✓ Processeur Intel détecté")

print()

# Test 3: Check OpenVINO devices
print("Test 3: Périphériques OpenVINO disponibles...")
try:
    from openvino.runtime import Core
    core = Core()
    devices = core.available_devices

    print(f"  Périphériques détectés: {devices}")

    has_gpu = any("GPU" in d for d in devices)
    has_cpu = "CPU" in devices

    if has_gpu:
        print(f"  ✓ GPU Intel disponible - Accélération iGPU activée (4-6x speedup)")
        for device in [d for d in devices if "GPU" in d]:
            try:
                gpu_name = core.get_property(device, "FULL_DEVICE_NAME")
                print(f"    {device}: {gpu_name}")
            except:
                pass

    if has_cpu:
        print(f"  ✓ CPU disponible - Optimisations Intel actives (2-3x speedup)")

    if not has_gpu and not has_cpu:
        print(f"  ⚠ Aucun périphérique détecté")

except Exception as e:
    print(f"  ❌ Erreur: {e}")

print()

# Test 4: Check whisper_openvino module
print("Test 4: Module whisper_openvino...")
try:
    from whisper_openvino import WhisperOpenVINO, should_use_openvino, is_intel_hardware
    print(f"  ✓ Module whisper_openvino importé")

    if is_intel_hardware():
        print(f"  ✓ Hardware Intel détecté")
    else:
        print(f"  ⚠ Hardware non-Intel")

    if should_use_openvino():
        print(f"  ✓ OpenVINO sera utilisé automatiquement")
    else:
        print(f"  ⚠ OpenVINO ne sera pas utilisé (dépendances manquantes?)")

except ImportError as e:
    print(f"  ❌ Erreur: {e}")
    print(f"     Assurez-vous que whisper_openvino.py est dans le répertoire noScribe")

print()
print("=" * 60)
print("  Test terminé")
print("=" * 60)
print()

if should_use_openvino():
    print("✓ Installation réussie ! OpenVINO est prêt à l'emploi.")
    print()
    print("Prochaines étapes:")
    print("  1. Lancez noScribe normalement")
    print("  2. Cherchez '🚀 Intel hardware detected' dans les logs")
    print("  3. Première transcription: modèle sera converti (5-10 min)")
    print("  4. Transcriptions suivantes: profitez du speedup 2-6x!")
else:
    print("⚠ OpenVINO installé mais ne sera pas utilisé automatiquement")
    print("  Vérifiez que vous êtes sur hardware Intel")
EOTEST

chmod +x test_openvino.py
echo "✓ Script de test créé: test_openvino.py"
echo ""

# Run test
echo "=================================================="
echo "  Exécution du test..."
echo "=================================================="
echo ""

python3 test_openvino.py

echo ""
echo "=================================================="
echo "  Installation terminée !"
echo "=================================================="
echo ""
echo "Prochaines étapes:"
echo "  1. Configurez config.yml (voir ci-dessous)"
echo "  2. Lancez noScribe"
echo "  3. Vérifiez les logs pour '🚀 Intel hardware detected'"
echo ""
echo "Configuration recommandée pour 10h d'audio:"
echo "  whisper_model: large-v3"
echo "  whisper_compute_type: int8"
echo "  whisper_beam_size: 5"
echo "  whisper_temperature: 0.0"
echo ""
echo "Pour aide: cat OPENVINO_OPTIMIZATION.md"
echo ""
