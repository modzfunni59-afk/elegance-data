#!/usr/bin/env python3
"""Fabrique data/index.json à partir des fichiers du dossier data.

Lancé automatiquement par GitHub à chaque fois qu'un fichier de data change.
Format identique à celui du script PowerShell, pour que les deux voies
produisent exactement le même index.
"""

import hashlib
import json
import os
from datetime import datetime, timezone

DOSSIER = "data"
EXCLUS = {"index.json", "noms.json"}


def main() -> int:
    if not os.path.isdir(DOSSIER):
        print(f"Dossier {DOSSIER} introuvable.")
        return 1

    fichiers = []

    for nom in sorted(os.listdir(DOSSIER)):
        if not nom.endswith(".json") or nom in EXCLUS:
            continue

        chemin = os.path.join(DOSSIER, nom)
        octets = open(chemin, "rb").read()

        fichiers.append({
            "nom": nom,
            "taille": len(octets),
            "empreinte": hashlib.sha256(octets).hexdigest().upper(),
        })

        print(f"  {nom:<30} {len(octets) // 1024:>6} Ko")

    if not fichiers:
        print("Aucun fichier de données.")
        return 1

    index = {
        "genere_le": datetime.now(timezone.utc).isoformat(),
        "nombre": len(fichiers),
        "fichiers": fichiers,
    }

    # UTF-8 sans BOM : le lecteur JSON de .NET refuse un fichier qui en a un.
    with open(os.path.join(DOSSIER, "index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=1)
        f.write("\n")

    print(f"\nindex.json écrit — {len(fichiers)} fichiers référencés.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
