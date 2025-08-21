# Multi-Agent System Monitoring Dashboard

Ein professionelles Echtzeit-Dashboard zur Überwachung von Multi-Agenten-Systemen mit Dark Mode und Corporate Identity Design.

## 🚀 Features

### 📊 Core Metrics
- **Task Completion Rate (TCR)** - Erfolgsrate der Aufgaben
- **System Velocity** - Geschwindigkeit der Aufgabenverarbeitung
- **Coordination Score** - Bewertung der Agent-Kollaboration
- **Resource Efficiency** - CPU/Memory-Nutzung
- **Message Throughput** - WebSocket-Messages/Sekunde
- **Collective Intelligence Coefficient** - Emergenz-Indikator

### 🔄 Development Pipeline
- **Requirements Management** (REQ-001 bis REQ-004)
- **Kanban Task Board** mit 4 Spalten
- **Test Suite Monitoring** (Unit, Integration, System, Performance)
- **CI/CD Pipeline Visualization** (Source → Build → Test → Deploy → Verify)
- **Component Health Status** mit interaktiven Komponenten
- **Documentation Status** Tracking

### 🎨 Design
- **Dark Mode** mit professionellem Farbschema
- **JetBrains Mono Font** (PyCharm-Style)
- **Corporate Identity** Design
- **Responsive Layout** für alle Bildschirmgrößen
- **Smooth Animations** und Hover-Effekte
- **Real-time Updates** (WebSocket-ready)

## 📦 Installation

```bash
# Repository klonen
git clone https://github.com/YOUR_USERNAME/multi-agent-dashboard.git
cd multi-agent-dashboard

# Dependencies installieren
npm install

# Development Server starten
npm run dev
```

## 🏗️ Projektstruktur

```
multi-agent-dashboard/
├── index.html          # Haupt-HTML Datei
├── css/
│   └── styles.css      # Alle CSS Styles
├── js/
│   ├── dashboard.js    # Haupt-Dashboard-Logik
│   ├── charts.js       # Chart-Visualisierungen
│   └── realtime-updates.js # WebSocket & Echtzeit-Updates
├── assets/            # Icons und Bilder (optional)
├── package.json       # NPM Konfiguration
├── README.md          # Diese Datei
└── .gitignore        # Git ignore Regeln
```

## 🖥️ Verwendung

### Development Mode
```bash
npm run dev
```
Startet einen Live-Server auf Port 8080 mit automatischem Reload bei Änderungen.

### Production
Das Dashboard kann als statische Website deployed werden:
```bash
npm run build
```

### Mit Python Server
```bash
python3 -m http.server 8000
```

## 📊 Metriken Erklärung

### Standardisierte KPIs
- **TCR (Task Completion Rate)**: 
  - Normal: > 85%
  - Kritisch: > 95%
- **Message Throughput**: 
  - High-Frequency Trading: 1000+ msg/s
  - Robotics: 10-100 msg/s
  - IoT: 0.1-10 msg/s
- **Coordination Score**: 
  - 4.0+ zeigt reife Kollaboration
- **Collective Intelligence**: 
  - > 1.0 = positive Emergenz
  - > 1.5 = exzellente Swarm Intelligence

## 🔌 WebSocket Integration

Das Dashboard ist vorbereitet für WebSocket-Verbindungen:

```javascript
// Beispiel WebSocket Setup
const ws = new WebSocket('ws://localhost:8080/metrics');

ws.onmessage = (event) => {
    const metrics = JSON.parse(event.data);
    updateDashboard(metrics);
};
```

### Datenformat
```javascript
{
  "metrics": {
    "tcr": 94.8,
    "velocity": 1247,
    "throughput": 42700,
    "efficiency": 87.2
  },
  "agents": {
    "total": 256,
    "active": 248,
    "idle": 8
  },
  "pipeline": {
    "stage": "testing",
    "progress": 65
  }
}
```

## 🛠️ Technologie-Stack

- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Fonts**: JetBrains Mono (Google Fonts)
- **Charts**: SVG-basierte Visualisierungen
- **Updates**: Simulierte Real-time Updates (WebSocket-ready)
- **Server**: Live-Server für Development

## 🎨 Anpassungen

### Farben ändern
Die Farben können in `css/styles.css` angepasst werden:

```css
:root {
    --bg-primary: #0a0e1a;      /* Haupthintergrund */
    --accent-primary: #3b82f6;   /* Primäre Akzentfarbe */
    --accent-success: #10b981;   /* Erfolg/Grün */
    --accent-warning: #f59e0b;   /* Warnung/Gelb */
    --accent-danger: #ef4444;    /* Fehler/Rot */
}
```

### Metriken erweitern
Neue Metriken können in `js/dashboard.js` hinzugefügt werden:

```javascript
function addCustomMetric(id, label, value) {
    const metricsGrid = document.querySelector('.metrics-grid');
    const metricCard = createMetricCard(id, label, value);
    metricsGrid.appendChild(metricCard);
}
```

## 🚀 Deployment

### GitHub Pages
```bash
# Build erstellen
npm run build

# Zu GitHub pushen
git add .
git commit -m "Deploy dashboard"
git push origin main

# In GitHub Settings → Pages → Source: main branch
```

### Docker
```dockerfile
FROM nginx:alpine
COPY . /usr/share/nginx/html
EXPOSE 80
```

```bash
docker build -t multi-agent-dashboard .
docker run -p 8080:80 multi-agent-dashboard
```

## 📱 Browser-Kompatibilität

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🤝 Contributing

1. Fork das Repository
2. Erstelle einen Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Committe deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

## 📄 Lizenz

MIT License - siehe [LICENSE](LICENSE) für Details

## 🙏 Credits

- Design inspiriert von modernen DevOps Dashboards
- JetBrains Mono Font von JetBrains
- Icons von Emoji

## 📞 Support

Bei Fragen oder Problemen:
- Öffne ein [Issue](https://github.com/YOUR_USERNAME/multi-agent-dashboard/issues)
- Kontakt: your.email@example.com

---

Made with ❤️ for Multi-Agent Systems
