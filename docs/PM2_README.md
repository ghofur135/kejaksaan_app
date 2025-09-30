# Quick PM2 Setup - Kejaksaan App

## 🚀 Quick Start

```bash
# Start aplikasi dengan PM2 (recommended)
./pm2-manager.sh start-direct

# Check status
./pm2-manager.sh status

# View logs
./pm2-manager.sh logs-direct
```

## 📁 Files Created

- `ecosystem.config.json` - PM2 config untuk bash script
- `ecosystem-direct.config.json` - PM2 config untuk gunicorn langsung
- `pm2-manager.sh` - Helper script untuk manage PM2
- `logs/` - Directory untuk log files

## 🔧 PM2 Commands

| Command | Description |
|---------|-------------|
| `./pm2-manager.sh start` | Start dengan bash script |
| `./pm2-manager.sh start-direct` | Start langsung dengan gunicorn (recommended) |
| `./pm2-manager.sh stop` | Stop aplikasi |
| `./pm2-manager.sh restart` | Restart aplikasi |
| `./pm2-manager.sh status` | Check status PM2 |
| `./pm2-manager.sh logs` | View logs |

## 📊 Monitoring

```bash
# Real-time monitoring dashboard
pm2 monit

# Check memory dan CPU usage
pm2 show kejaksaan-flask-app
```

Read full documentation: `PM2_GUIDE.md`