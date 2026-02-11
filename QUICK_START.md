"""Quick Start Guide - Pornire Rapidă"""

QUICK_START = """
╔═══════════════════════════════════════════════════════════════╗
║         PORNIRE RAPIDĂ - CUTREMURE INFP INTEGRATION           ║
╚═══════════════════════════════════════════════════════════════╝

## ⚡ În 5 minute - Setup complet

### 1️⃣ Instalare (1 min)
```bash
cd ~/.homeassistant/custom_components
cp -r /path/to/cutremure_infp .
```

### 2️⃣ Restart (2 min)
Settings → System → Restart Home Assistant
(Așteptați ca sistemul să se restarteze)

### 3️⃣ Adăugare Integrare (1 min)
- Settings → Devices & Services
- + Create Integration
- Căutați "Cutremure INFP"
- Setați Prag Magnitudine: 3.0 (puteți schimba depois)
- Setați Interval: 60 secunde

### 4️⃣ Verificare (1 min)
- Settings → Devices & Services → Entities
- Căutați "earthquake" - ar trebui să vedeți 4 entități

🎉 Gata! Integrarea e live!

---

## 📋 Entități disponibile

### Senzori
- `sensor.latest_earthquake` - Locație + mag
- `sensor.earthquake_magnitude` - Doar magnitudinea (număr)
- `sensor.earthquake_depth` - Profunzimea în km

### Binary Sensor (pentru notificări)
- `binary_sensor.earthquake_alert` - ON/OFF bazat pe prag

---

## 🔔 Crează prima notificare

### Opțiunea A: Mobile App (Recomandată)

Settings → Automations → Create New Automation

**"New Automation"**

```
Name: "Alerta Cutremur"
Trigger: Entity State
  Entity: binary_sensor.earthquake_alert
  To: "on"

Action: Call Service
  Service: notify.mobile_app_<YOUR_DEVICE>
  Title: "🚨 CUTREMUR!"
  Message: "Mag {{ states('sensor.earthquake_magnitude') }}"
```

Apasă "Create Automation" ✅

### Opțiunea B: Notificare în Home Assistant

```
Trigger: Entity State
  Entity: binary_sensor.earthquake_alert
  To: "on"

Action: Call Service
  Service: persistent_notification.create
  Title: "ALERTA CUTREMUR"
  Message: "Magnitudine: {{ states('sensor.earthquake_magnitude') }}"
```

---

## 🎚️ Schimbare Prag de Magnitudine

**În UI (Ușor):**
1. Settings → Devices & Services
2. Selectează "Cutremure INFP"
3. Apasă "Options"
4. Schimbă "Prag de Magnitudine"
5. Salvează

**După schimbare, notificările se vor trimite pentru cutremure ≥ pragul setat**

---

## 📊 Vizualizare Date

### Dashboard Card - Pe tablou Home Assistant

```yaml
type: entities
title: Informații Cutremur
entities:
  - entity: sensor.latest_earthquake
  - entity: sensor.earthquake_magnitude
  - entity: sensor.earthquake_depth
  - entity: binary_sensor.earthquake_alert
```

Adăugați card cu drag-and-drop pe dashboard.

---

## 🚨 Apel Urgent - Notificări Multiple

Creați automation mai complex:

1. Duplicate notificarea de mai sus
2. Adăugați mai mulți destinatari:

```
Action 1: notify.mobile_app_iphone
Action 2: notify.mobile_app_android  
Action 3: notify.email
Action 4: persistent_notification.create
```

---

## ✅ Checklist Setup

- [ ] Directorul custom_components copiat
- [ ] Home Assistant restartată
- [ ] Integrare adăugată
- [ ] 4 entități vizibile
- [ ] Prag magnitudine setat
- [ ] Automatizare creată
- [ ] Test: Așteptați un cutremur SAU verific manual senzor

---

## ⚙️ Setări Avansate (Optional)

### Schimbă Interval Actualizare
Default: 60 secunde (verific API la fiecare minut)

**Pentru actualizări mai rapide:** 30 secunde
**Pentru mai puține interogări:** 300 secunde (5 min)

Modifică în Options de integrare.

### Filtreze după Locație
(Necesită automatizare custom)
```yaml
condition: template
value_template: >
  "Vrancea" in state_attr('sensor.latest_earthquake', 'location')
```

---

## 🆘 Probleme Comune

### "Entități nu apar"
- Restart complet Home Assistant (nu reload)
- Verifică loguri: Settings → System → Logs

### "Binary sensor rămâne OFF"
- Cutremur trebuie să aibă magnitudinea ≥ prag
- Acceptă doar cutremurele noi (nu retrăiesc vechi)

### "Notificare nu se trimite"
- Verific că device_id e corect în automation
- Test manual: Services → notify.mobile_app_X → Call

---

## 📚 Documente Suplimentare

- **README.md** - Descriere completă
- **INSTALLATION.md** - Instalare detaliată
- **examples.py** - Exemple de cod
- **API Source** - https://fastapi.infp.ro/v1/?product=shakemap4

---

## 💡 Sfaturi Pro

1. **Prag mai mare în noapte**: Crea 2 automatizări cu condiții de oră
2. **Notificare detaliată**: Adaugă atribute (profunzime, coordonate)
3. **Alerte colorate**: Pe mobile app, diferiți culori pentru magnitudini
4. **Logare**: Creează sensor care să salveze istoric cutremurelor

---

**Succes! 🎉 Acum ești gata să primești notificări instantanee pentru cutremure!**
"""

TESTING_MANUAL = """
## Testing Manual - Verificare Funcționalitate

### Test 1: Verific dacă API funcționează
```bash
# În terminal
curl "https://fastapi.infp.ro/v1/?product=shakemap4" | python -m json.tool | head -50
```

Ar trebui să vadă un array JSON cu cutremure.

### Test 2: Verific entități în Home Assistant
1. Settings → Developer Tools → States
2. Căutând "earthquake"
3. Ar trebui să vedeți 4 entități cu state și atribute

### Test 3: Forțare actualizare manual
```yaml
# În Developer Tools → Services
Service: homeassistant.reload_config_entry
Target: Cutremure INFP
```

### Test 4: Simulare trigger notificare
```yaml
# Developer Tools → Services
Service: notify.mobile_app_<device>
Data:
  title: "TEST"
  message: "Test notificare"
```

Dacă primești notificare - notificările funcționează!

---

## Logging & Debug

### Activare Debug Mode
```yaml
# configuration.yaml
logger:
  logs:
    cutremure_infp: debug
```

După restart, Settings → System → Logs va arăta mai mult detalii.
"""
