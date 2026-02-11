"""Installation and setup guide for Home Assistant integration."""

INSTALLATION_STEPS = """
╔══════════════════════════════════════════════════════════════╗
║        INSTALARE INTEGRARE CUTREMURE INFP - HOME ASSISTANT   ║
╚══════════════════════════════════════════════════════════════╝

## OPȚIUNEA 1: Instalare Manuală (Recomandată)

### Pasul 1: Copiați directorul integrării
```bash
# Navigați la directorul Home Assistant
cd ~/.homeassistant

# Copiați integrarea
cp -r /path/to/cutremure_infp custom_components/

# Verificare
ls -la custom_components/cutremure_infp/
```

### Pasul 2: Reporniți Home Assistant
- Mergeți la: Settings → System → Restart Home Assistant
- Așteptați 2-3 minute să se restarteze

### Pasul 3: Adăugați integrarea din UI
1. Settings → Devices & Services
2. Apăsați "Create Integration" (sau scanuți QR code dacă apare)
3. Căutați "Cutremure INFP"
4. Configurați parametrii:
   - Prag magnitudine: 3.0 (poate fi schimbat depois)
   - Interval update: 60 secunde

## OPȚIUNEA 2: Instalare prin HACS (Dacă ai HACS instalat)

### Pasul 1: Adăugați repository
1. HACS → Custom repositories
2. URL: https://github.com/yourusername/cutremure-infp-romania
3. Category: Integration
4. Creează

### Pasul 2: Instalați
1. HACS → Integrations
2. Căutați "Cutremure INFP"
3. Install → Restart

## Verificare Instalare

### Check 1: Existența fișierelor
```bash
ls -la ~/.homeassistant/custom_components/cutremure_infp/
```

Ar trebui să vedeti:
```
__init__.py
manifest.json
const.py
config_flow.py
sensor.py
binary_sensor.py
strings.json
```

### Check 2: Loguri Home Assistant
Settings → System → Logs

Căutați mesaje cu "cutremure_infp" - nu ar trebui să fie erori

### Check 3: Verificare entități create
Settings → Devices & Services → Entities

Ar trebui să vedeți:
- sensor.latest_earthquake
- sensor.earthquake_magnitude
- sensor.earthquake_depth
- binary_sensor.earthquake_alert

## Configurare Selectoare (Optional)

### Pentru a schimba pragul de magnitudine în UI:

Adăugați în configuration.yaml:
```yaml
input_select:
  earthquake_threshold:
    name: "Prag Magnitudine Cutremur"
    options:
      - "1.0"
      - "2.0"
      - "2.5"
      - "3.0"
      - "3.5"
      - "4.0"
      - "4.5"
      - "5.0"
    initial: "3.0"

input_number:
  earthquake_update_interval:
    name: "Interval Actualizare (sec)"
    min: 10
    max: 3600
    step: 10
    unit_of_measurement: "sec"
    initial: 60
```

După aceasta, restartați Home Assistant.

## Troubleshooting

### 1. Integrarea nu apare în "Create Integration"
- Verificați file structure (trebuie __init__.py în directorul integrării)
- Restartați Home Assistant complet (nu doar reload)
- Ștergeți cache: `.homeassistant/__pycache__`

### 2. Eroare: "No module named 'homeassistant'"
- Trebuie să instalezi dependențele Home Assistant
- Mergi în directorul Home Assistant și execut: `pip install homeassistant`

### 3. Senzorul rămâne "unavailable"
- Verifică logurile Home Assistant pentru erori API
- Testează manual API-ul: 
  ```bash
  curl "https://fastapi.infp.ro/v1/?product=shakemap4" | head -100
  ```
- Asigură-te că ai internet connection

### 4. Binary sensor nu se activează
- Verifică că pragul de magnitudine e setat corect
- Asteapta un cutremur cu magnitudinea mai mare decât pragul
- Verifica atributul 'magnitude_threshold' din sensor

## Resetare Integrare

Dacă ceva merge prost:

### Opțiunea A: Soft Reset
1. Settings → Devices & Services
2. Selectează "Cutremure INFP"
3. Apasă trei puncte → Delete
4. Restartează Home Assistant
5. Readă integrarea

### Opțiunea B: Hard Reset
```bash
# Șterge directorul integrării
rm -rf ~/.homeassistant/custom_components/cutremure_infp/

# Șterge fișiere de configurare
rm -f ~/.homeassistant/custom_components/.storage/cutremure_infp*

# Restartează Home Assistant
```

## Verificare Finală

După instalare, ar trebui să:
1. ✅ Vezi 3 senzori și 1 binary sensor
2. ✅ Primești notificări pe telefon
3. ✅ Poți vedea date cutremur în History
4. ✅ Poți crea automatizări personalizate

Dacă totul e OK - Gata! Integrarea funcționează! 🎉
"""

DOCKER_INSTALLATION = """
## INSTALARE ÎN HOME ASSISTANT DOCKER

Dacă rulezi Home Assistant în Docker:

### Pasul 1: Copy custom_components
```bash
docker cp custom_components/cutremure_infp \
  <container_id>:/config/custom_components/
```

### Pasul 2: Schimbă ownership
```bash
docker exec <container_id> \
  chown -R 1000:1000 /config/custom_components/cutremure_infp
```

### Pasul 3: Restartează container
```bash
docker restart <container_id>
```

### Verific
```bash
docker exec <container_id> \
  ls -la /config/custom_components/cutremure_infp/
```
"""

DEVELOPMENT_SETUP = """
## SETUP PENTRU DEVELOPMENT

### Instalează dependențe
```bash
pip install homeassistant
pip install pytest-homeassistant-custom-component
```

### Rulează teste
```bash
pytest custom_components/cutremure_infp/
```

### Simulează integrarea
```bash
# În custom_component director
python -m homeassistant --debug --config ./config
```
"""
