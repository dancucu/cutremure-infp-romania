"""Example automation configuration for Cutremure INFP integration."""

# Example 1: Simple notification when earthquake alert triggers
SIMPLE_NOTIFICATION = """
automation:
  - alias: "Cutremur - Notificare Simplă"
    description: "Trimite notificare la telefon când e cutremur"
    trigger:
      - platform: state
        entity_id: binary_sensor.earthquake_alert
        to: "on"
    action:
      - service: notify.mobile_app_<your_device_id>
        data:
          title: "🚨 CUTREMUR!"
          message: |
            Magnitudine: {{ state_attr('sensor.latest_earthquake', 'magnitude') }}
            Locație: {{ state_attr('sensor.latest_earthquake', 'location') }}
            Ora: {{ state_attr('sensor.latest_earthquake', 'time') }}
"""

# Example 2: Notification with magnitude threshold check
ADVANCED_NOTIFICATION = """
automation:
  - alias: "Cutremur - Notificare Avansată"
    description: "Notificare detaliată cu threshold configurable"
    trigger:
      - platform: state
        entity_id: sensor.earthquake_magnitude
        # Declanșează la orice schimbare de magnitudine
    condition:
      - condition: numeric_state
        entity_id: sensor.earthquake_magnitude
        above: 3.5  # Doar dacă magnitudinea e mai mare decât 3.5
    action:
      - service: notify.notify
        data:
          title: "⚠️ ALERTA CUTREMUR - MAGNITUDINE MARE"
          message: |
            🏘️ Locație: {{ state_attr('sensor.latest_earthquake', 'location') }}
            📊 Magnitudine: {{ states('sensor.earthquake_magnitude') }}
            📏 Profunzime: {{ states('sensor.earthquake_depth') }} km
            🕐 Ora: {{ state_attr('sensor.latest_earthquake', 'time') }}
            📍 Coordonate: {{ state_attr('sensor.latest_earthquake', 'latitude') }}, {{ state_attr('sensor.latest_earthquake', 'longitude') }}
"""

# Example 3: Multiple notification services
MULTI_CHANNEL = """
automation:
  - alias: "Cutremur - Notificări Multi-Canal"
    description: "Trimite pe mobile, email și text"
    trigger:
      - platform: state
        entity_id: binary_sensor.earthquake_alert
        to: "on"
    action:
      # Notificare pe telefon
      - service: notify.mobile_app_iphone
        data:
          title: "🚨 CUTREMUR DETECTAT!"
          message: >
            Magnitudine {{ states('sensor.earthquake_magnitude') }} în 
            {{ state_attr('sensor.latest_earthquake', 'location') }}
          data:
            push:
              sound: critical
      
      # Email
      - service: notify.email
        data:
          title: "Alerta Cutremur"
          message: |
            Cutremur cu magnitudine {{ states('sensor.earthquake_magnitude') }}
            Locație: {{ state_attr('sensor.latest_earthquake', 'location') }}
            Profunzime: {{ states('sensor.earthquake_depth') }} km
      
      # SMS (dacă ai integrat)
      - service: notify.twilio
        data:
          message: "ALERTA: Cutremur mag. {{ states('sensor.earthquake_magnitude') }}"
"""

# Example 4: Automation with persistent notification
PERSISTENT_NOTIFICATION = """
automation:
  - alias: "Cutremur - Notificare Persistentă"
    description: "Afișează notificare persistentă + popup"
    trigger:
      - platform: state
        entity_id: binary_sensor.earthquake_alert
        to: "on"
    action:
      # Notificare persistentă în Home Assistant
      - service: persistent_notification.create
        data:
          title: "🚨 CUTREMUR"
          message: |
            **Informații Cutremur**
            - Magnitudine: {{ states('sensor.earthquake_magnitude') }}
            - Locație: {{ state_attr('sensor.latest_earthquake', 'location') }}
            -Profunzime: {{ states('sensor.earthquake_depth') }} km
            - Ora: {{ state_attr('sensor.latest_earthquake', 'time') }}
          notification_id: "earthquake_alert"
      
      # Notificare mobil
      - service: notify.mobile_app_device
        data:
          title: "ALERTA CUTREMUR"
          message: "Magnitudine {{ states('sensor.earthquake_magnitude') }}"
          data:
            tag: earthquake
            persistent: true
"""

# Example 5: Selective notification by level
SEVERITY_BASED = """
automation:
  - alias: "Cutremur - Alerte pe Severitate"
    description: "Diferite mesaje după magnitudine"
    trigger:
      - platform: state
        entity_id: sensor.earthquake_magnitude
    action:
      - choose:
          # Alerte moderate
          - conditions:
              - condition: numeric_state
                entity_id: sensor.earthquake_magnitude
                above: 3.0
                below: 3.5
            sequence:
              - service: notify.mobile_app_iphone
                data:
                  title: "⚠️ Cutremur Moderat"
                  message: "Mag {{ states('sensor.earthquake_magnitude') }} în {{ state_attr('sensor.latest_earthquake', 'location') }}"
          
          # Alerte puternice
          - conditions:
              - condition: numeric_state
                entity_id: sensor.earthquake_magnitude
                above: 3.5
                below: 4.5
            sequence:
              - service: notify.mobile_app_iphone
                data:
                  title: "🔴 Cutremur Puternic!"
                  message: "Mag {{ states('sensor.earthquake_magnitude') }}! Locație: {{ state_attr('sensor.latest_earthquake', 'location') }}"
          
          # Alerte foarte puternice
          - conditions:
              - condition: numeric_state
                entity_id: sensor.earthquake_magnitude
                above: 4.5
            sequence:
              - service: notify.mobile_app_iphone
                data:
                  title: "🚨 CUTREMUR SEMNIFICATIV!"
                  message: "MAGNITUDINE {{ states('sensor.earthquake_magnitude') }}! {{ state_attr('sensor.latest_earthquake', 'location') }}"
"""

# Example 6: Automation with conditions and time-based restrictions
TIME_RESTRICTED = """
automation:
  - alias: "Cutremur - Notificări cu Restricții"
    description: "Notificări doar în anumite ore, doar pentru magnitudini mari"
    trigger:
      - platform: state
        entity_id: binary_sensor.earthquake_alert
        to: "on"
    condition:
      - condition: numeric_state
        entity_id: sensor.earthquake_magnitude
        above: 3.5
      - condition: time
        after: "08:00:00"
        before: "22:00:00"
    action:
      - service: notify.mobile_app_device
        data:
          title: "Alerta Cutremur"
          message: "Magnitudine {{ states('sensor.earthquake_magnitude') }}"
  
  # Notificare în orele de noapte DOAR pentru cutremure majore
  - alias: "Cutremur Night Alert"
    trigger:
      - platform: state
        entity_id: binary_sensor.earthquake_alert
        to: "on"
    condition:
      - condition: numeric_state
        entity_id: sensor.earthquake_magnitude
        above: 4.0
      - condition: time
        after: "22:00:00"
        before: "08:00:00"
    action:
      - service: notify.mobile_app_device
        data:
          title: "🚨 CUTREMUR MAJOR!"
          message: "ALERTA: Magnitudine {{ states('sensor.earthquake_magnitude') }}"
          data:
            push:
              sound: critical
"""

# Example 7: Script for complex earthquake alert workflow
SCRIPT_WORKFLOW = """
script:
  earthquake_alert_workflow:
    description: "Workflow complet pentru alerta cutremur"
    sequence:
      # 1. Trimite notificări
      - service: notify.mobile_app_iphone
        data:
          title: "🚨 CUTREMUR!"
          message: >
            Magnitudine: {{ states('sensor.earthquake_magnitude') }}
            Locație: {{ state_attr('sensor.latest_earthquake', 'location') }}
      
      # 2. Creează notificare persistentă
      - service: persistent_notification.create
        data:
          title: "Detalii Cutremur"
          message: |
            Magnitudine: {{ states('sensor.earthquake_magnitude') }}
            Adâncime: {{ states('sensor.earthquake_depth') }} km
            Coordonate: {{ state_attr('sensor.latest_earthquake', 'latitude') }}, {{ state_attr('sensor.latest_earthquake', 'longitude') }}
          notification_id: "earthquake_{{ now().timestamp() }}"
      
      # 3. Apelează alte automatizări (ex: apritoare ușă, becuri)
      - if:
          - condition: numeric_state
            entity_id: sensor.earthquake_magnitude
            above: 4.0
        then:
          - service: light.turn_on
            entity_id: light.living_room
            data:
              brightness: 255
"""

# Example 8: Input select for dynamic magnitude threshold
SELECTOR_CONFIGURATION = """
input_select:
  earthquake_notification_level:
    name: "Nivel Notificări Cutremur"
    description: "Alege la ce magnitudine vrei notificări"
    options:
      - "Doar majore (>4.0)"
      - "Puternice (>3.5)"
      - "Moderate (>3.0)"
      - "Inceput (>2.5)"
      - "Toate (>1.0)"
    initial: "Moderate (>3.0)"
    icon: mdi:gauge

automation:
  - alias: "Cutremur - Dynamic Threshold"
    trigger:
      - platform: state
        entity_id: binary_sensor.earthquake_alert
        to: "on"
    condition:
      - condition: template
        value_template: >
          {% set threshold_map = {
            'Doar majore (>4.0)': 4.0,
            'Puternice (>3.5)': 3.5,
            'Moderate (>3.0)': 3.0,
            'Inceput (>2.5)': 2.5,
            'Toate (>1.0)': 1.0
          } %}
          {{ states('sensor.earthquake_magnitude') | float(0) >= threshold_map[states('input_select.earthquake_notification_level')] }}
    action:
      - service: notify.mobile_app_device
        data:
          title: "Alerta Cutremur"
          message: "Mag {{ states('sensor.earthquake_magnitude') }}"
"""
