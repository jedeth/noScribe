#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de configuration automatique pour transcriptions rapides
Optimise config.yml pour les meilleurs performances avec OpenVINO
"""

import os
import sys
import yaml
from pathlib import Path

def find_config_file():
    """Find the config.yml file"""
    # Try user config directory first
    if sys.platform == 'linux':
        config_dir = Path.home() / '.config' / 'noScribe'
    elif sys.platform == 'win32':
        config_dir = Path(os.getenv('APPDATA')) / 'noScribe'
    elif sys.platform == 'darwin':
        config_dir = Path.home() / 'Library' / 'Application Support' / 'noScribe'
    else:
        config_dir = None

    if config_dir and (config_dir / 'config.yml').exists():
        return config_dir / 'config.yml'

    # Fallback to current directory
    if Path('config.yml').exists():
        return Path('config.yml')

    return None

def backup_config(config_path):
    """Create backup of current config"""
    import shutil
    from datetime import datetime

    backup_path = config_path.parent / f"config.yml.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(config_path, backup_path)
    print(f"✓ Backup créé: {backup_path}")
    return backup_path

def configure_for_speed(preset='balanced'):
    """
    Configure noScribe for optimal speed

    Presets:
    - 'ultra_fast': Maximum speed, lower quality (good for drafts)
    - 'balanced': Good balance of speed and quality (recommended)
    - 'quality': Best quality, still faster than default
    """

    print("=" * 70)
    print("  Configuration OpenVINO pour noScribe")
    print("  Optimisation pour transcriptions rapides")
    print("=" * 70)
    print()

    # Find config
    config_path = find_config_file()

    if not config_path:
        print("❌ Fichier config.yml introuvable")
        print()
        print("Le fichier devrait être dans:")
        if sys.platform == 'linux':
            print(f"  ~/.config/noScribe/config.yml")
        elif sys.platform == 'win32':
            print(f"  %APPDATA%\\noScribe\\config.yml")
        elif sys.platform == 'darwin':
            print(f"  ~/Library/Application Support/noScribe/config.yml")
        print()
        print("Lancez noScribe une fois pour créer le fichier de configuration")
        sys.exit(1)

    print(f"✓ Config trouvé: {config_path}")
    print()

    # Load current config
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}
    except Exception as e:
        print(f"❌ Erreur lecture config: {e}")
        sys.exit(1)

    # Backup
    backup_path = backup_config(config_path)
    print()

    # Define presets
    presets = {
        'ultra_fast': {
            'name': 'Ultra Rapide',
            'description': 'Vitesse maximum, qualité correcte (brouillons)',
            'settings': {
                'whisper_compute_type': 'int8',
                'whisper_beam_size': 1,
                'whisper_temperature': 0.0,
                'voice_activity_detection_threshold': 0.5,
            },
            'model_recommendation': 'medium ou small'
        },
        'balanced': {
            'name': 'Équilibré',
            'description': 'Bon équilibre vitesse/qualité (recommandé)',
            'settings': {
                'whisper_compute_type': 'int8',
                'whisper_beam_size': 5,
                'whisper_temperature': 0.0,
                'voice_activity_detection_threshold': 0.5,
            },
            'model_recommendation': 'large-v3 ou large-v2'
        },
        'quality': {
            'name': 'Qualité',
            'description': 'Meilleure qualité, toujours rapide',
            'settings': {
                'whisper_compute_type': 'int8',
                'whisper_beam_size': 10,
                'whisper_temperature': 0.0,
                'voice_activity_detection_threshold': 0.3,
            },
            'model_recommendation': 'large-v3'
        }
    }

    # Show current settings
    print("Configuration actuelle:")
    print(f"  whisper_compute_type: {config.get('whisper_compute_type', 'default')}")
    print(f"  whisper_beam_size: {config.get('whisper_beam_size', 1)}")
    print(f"  whisper_temperature: {config.get('whisper_temperature', 0.0)}")
    print(f"  VAD threshold: {config.get('voice_activity_detection_threshold', 0.5)}")
    print()

    # Select preset
    print("Presets disponibles:")
    print()
    for i, (key, preset_info) in enumerate(presets.items(), 1):
        print(f"{i}. {preset_info['name']} - {preset_info['description']}")
        print(f"   Modèle recommandé: {preset_info['model_recommendation']}")
        print()

    if preset not in presets:
        try:
            choice = int(input("Choisissez un preset (1-3) [2]: ").strip() or "2")
            preset = list(presets.keys())[choice - 1]
        except (ValueError, IndexError):
            preset = 'balanced'
            print(f"Utilisation du preset par défaut: {presets[preset]['name']}")

    selected_preset = presets[preset]
    print()
    print(f"✓ Preset sélectionné: {selected_preset['name']}")
    print(f"  {selected_preset['description']}")
    print()

    # Apply settings
    print("Application des paramètres...")
    for key, value in selected_preset['settings'].items():
        old_value = config.get(key)
        config[key] = value
        if old_value != value:
            print(f"  {key}: {old_value} → {value}")

    print()

    # Save config
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        print(f"✓ Configuration sauvegardée: {config_path}")
    except Exception as e:
        print(f"❌ Erreur sauvegarde: {e}")
        print(f"   Restaurez le backup: {backup_path}")
        sys.exit(1)

    print()
    print("=" * 70)
    print("  Configuration terminée !")
    print("=" * 70)
    print()

    # Show recommendations
    print("Recommandations pour transcriptions 10h:")
    print()
    print(f"1. Modèle Whisper: {selected_preset['model_recommendation']}")
    print(f"   (Changez dans l'interface noScribe)")
    print()
    print("2. Configuration appliquée:")
    for key, value in selected_preset['settings'].items():
        print(f"   - {key}: {value}")
    print()
    print("3. Performance attendue avec OpenVINO:")
    if preset == 'ultra_fast':
        print(f"   - CPU Intel: ~5-8h pour 10h d'audio (2-2.5x)")
        print(f"   - iGPU Intel: ~2-4h pour 10h d'audio (3-5x)")
    elif preset == 'balanced':
        print(f"   - CPU Intel: ~7-10h pour 10h d'audio (2-3x)")
        print(f"   - iGPU Intel: ~3-5h pour 10h d'audio (4-6x)")
    elif preset == 'quality':
        print(f"   - CPU Intel: ~10-15h pour 10h d'audio (1.5-2x)")
        print(f"   - iGPU Intel: ~5-8h pour 10h d'audio (2.5-4x)")
    print()
    print("4. Prochaines étapes:")
    print("   - Lancez noScribe")
    print("   - Sélectionnez le modèle Whisper recommandé")
    print("   - Vérifiez '🚀 Intel hardware detected' dans les logs")
    print("   - Première transcription: conversion du modèle (5-10 min)")
    print("   - Transcriptions suivantes: profitez du speedup!")
    print()
    print(f"Backup de l'ancienne config: {backup_path}")
    print()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Configure noScribe pour transcriptions rapides avec OpenVINO'
    )
    parser.add_argument(
        '--preset',
        choices=['ultra_fast', 'balanced', 'quality'],
        default='balanced',
        help='Preset de configuration (default: balanced)'
    )

    args = parser.parse_args()

    try:
        configure_for_speed(preset=args.preset)
    except KeyboardInterrupt:
        print()
        print("Annulé par l'utilisateur")
        sys.exit(1)
