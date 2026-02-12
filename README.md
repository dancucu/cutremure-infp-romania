# Integrare Home Assistant - Cutremure INFP Romania

O integrare completă pentru **Home Assistant** care monitorizează cutremurele din Romania și trimite notificări automate bazate pe magnitudinea seismului.

## Caracteristici

✅ **Monitorizare în timp real** - Verifică cutremurele din API-ul INFP la intervale configurabile  
✅ **Senzori detaliați** - Oferă informații complete: locație, magnitudine, profunzime, coordonate  
✅ **Prag de magnitudine configurable** - Alege ce magnitudine déclanșează notificări  
✅ **Binary sensor pentru alerte** - Userul poate crea automatizări personalizate  
✅ **Configurație prin UI** - Nici o editare manuală de YAML necesară  

## Instalare

## Pre-release

- Ultimul pre-release disponibil: [v1.0.2-beta.1](https://github.com/dancucu/cutremure-infp-romania/releases/tag/v1.0.2-beta.1)

### 1. Co­piați directorul integrării

```bash
cp -r custom_components/cutremure_infp ~/.homeassistant/custom_components/
```

### 2. Reporniți Home Assistant

- Mergeți la **Settings → System → Restart**

### 3. Adăugați integrarea

1. Mergeți la **Settings → Devices & Services → Create Automation**
2. Apăsați **+ Create Integration**
3. Căutați **"Cutremure INFP"**
4. Selectați și configurați:
   - **Prag de magnitudine**: 3.0 (implicit) - Pentru notificare la cutremure cu magnitudine ≥ 3.0
   - **Interval de actualizare**: 60 secunde (implicit) - Cât de des să verifice API-ul

## Sensori disponibili

### Senzori normali:
- `sensor.latest_earthquake` - Ultimul cutremur (locație + magnitudine)
- `sensor.earthquake_magnitude` - Magnitudinea (valoare numerică)
- `sensor.earthquake_depth` - Profunzimea în km

### Binary sensor (pentru automatizări):
- `binary_sensor.earthquake_alert` - **ON** dacă magnitudinea ≥ prag, **OFF** altfel

### Atribute ale senzorilor:
```
location: Zona seismica Vrancea - Buzau
magnitude: 3.8
depth: 125.0
latitude: 45.5567
longitude: 26.4245
time: 2025-12-31 18:48:09
event_type: ACTUAL
```

## Creare automatizări

### Exemplu 1: Notificare automată pe mobil

```yaml
alias: "Alerta Cutremur"
description: "Notificare când cutremur puternic"
trigger:
  - platform: state
    entity_id: binary_sensor.earthquake_alert
    to: "on"
condition: []
action:
  - service: notify.notify
    data:
      title: "🚨 CUTREMUR!"
      message: |
        Locație: {{ state_attr('sensor.latest_earthquake', 'location') }}
        Magnitudine: {{ state_attr('sensor.latest_earthquake', 'magnitude') }}
        Profunzime: {{ state_attr('sensor.latest_earthquake', 'depth') }} km
        Ora: {{ state_attr('sensor.latest_earthquake', 'time') }}
mode: single
```

### Exemplu 2: Determinarti pragul cu selector

```yaml
alias: "Actualizare prag cutremur"
description: "Schimbă pragul de magnitudine"
trigger:
  - platform: state
    entity_id: input_select.earthquake_threshold
action:
  - service: homeassistant.reload_config_entry
    target:
      entity_id: sensor.latest_earthquake
mode: single
```

### Exemplu 3: Mesaj text custom

```yaml
alias: "Alerta detaliată cutremur"
trigger:
  - platform: state
    entity_id: binary_sensor.earthquake_alert
    to: "on"
action:
  - service: notify.mobile_app_<telefon>
    data:
      title: "⚡ CUTREMUR DETECTAT!"
      message: >
        Magnitudine: {{ states('sensor.earthquake_magnitude') }} 
        Adâncime: {{ states('sensor.earthquake_depth') }} km
        Locație: {{ state_attr('sensor.latest_earthquake', 'location') }}
      data:
        tag: "earthquake_alert"
        persistent: true
mode: single
```

## Configurare avansată

### Selectorul pentru prag de magnitudine

Adăugați în `configuration.yaml`:

```yaml
input_select:
  earthquake_threshold:
    name: "Prag cutremur (magnitudine)"
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
    icon: mdi:gauge
```

### Script pentru notificare multi-canal

```yaml
script:
  earthquake_alert:
    description: "Alerta cutremur - multi-canal"
    sequence:
      - service: notify.email
        data:
          title: "Cutremur detectat!"
          message: >
            Magnitudine: {{ states('sensor.earthquake_magnitude') }}
      - service: notify.mobile_app_telefon
        data:
          title: "🚨 ALERTA CUTREMUR"
          message: >
            Locație: {{ state_attr('sensor.latest_earthquake', 'location') }}
            Mag: {{ states('sensor.earthquake_magnitude') }}
```

## Variabile de mediu

### Schimbă intervalul de actualizare

În Home Assistant UI:
1. **Settings → Devices & Services**
2. Selectați integrarea **Cutremure INFP**
3. Apăsați **Options** și modificați **Interval de actualizare**

## Structure fișierelor

```
custom_components/cutremure_infp/
├── __init__.py              # Logica principală
├── manifest.json            # Metadate integrare
├── const.py                 # Constante
├── config_flow.py           # UI de configurare
├── sensor.py                # Senzori
├── binary_sensor.py         # Binary sensor pentru notificări
└── strings.json             # Texte localizate
```

## API Source

**Endpoint:** `https://fastapi.infp.ro/v1/?product=shakemap4`

**Response format:**
```json
[
  {
    "id": "1770752251",
    "time": "2026-02-10 19:37:31",
    "locstring": "Zona seismica Vrancea - Buzau",
    "lat": "45.497000",
    "lon": "26.395700",
    "mag": "3.0",
    "depth": "122.00",
    "event_type": "ACTUAL",
    "netid": "RO",
    "network": "RO"
  }
]
```

## Troubleshooting

### Senzorul nu se actualizează

1. Verificați loguri: **Settings → System → Logs**
2. Asigurați-vă că API-ul este accesibil: `curl https://fastapi.infp.ro/v1/?product=shakemap4`
3. Reastarturi Home Assistant și reîncărcați integrarea

### Binary sensor rămâne OFF

- Verificați că pragul de magnitudine este setat corect
- Controlați atributul `magnitude_threshold` din `binary_sensor.earthquake_alert`

### Notificări duplicate

- Asigurați-vă că o singură automatizare declanșează pe `binary_sensor.earthquake_alert`
- Utilizați `mode: single` pentru a evita execuții paralele

## Licență

Proiect open-source - Simt liber să-l modifici și să contribui!

## Contact

Pentru probleme, sugestii sau contribuții: [GitHub Issues](https://github.com/yourusername/cutremure-infp-romania)

---

**Creat cu ❤️ pentru monitorizarea seismeității din Romania**
