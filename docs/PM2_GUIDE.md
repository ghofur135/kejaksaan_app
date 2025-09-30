# PM2 Configuration Guide - Kejaksaan App

## Prerequisites

### 1. Install Node.js dan PM2
```bash
# Install Node.js (jika belum ada)
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PM2 globally
npm install -g pm2
```

Atau gunakan script helper:
```bash
./pm2-manager.sh install-pm2
```

## Configuration Files

### 1. `ecosystem.config.json` 
Menggunakan bash script `run_production.sh`
- **Pros**: Menggunakan existing script, semua environment setup otomatis
- **Cons**: Sedikit overhead karena melalui bash

### 2. `ecosystem-direct.config.json`
Menjalankan gunicorn langsung
- **Pros**: Performa lebih baik, direct execution  
- **Cons**: Perlu setup environment manual

## Usage

### Menggunakan PM2 Manager Script (Recommended)

```bash
# Start aplikasi (menggunakan bash script)
./pm2-manager.sh start

# Start aplikasi (langsung dengan gunicorn) - RECOMMENDED
./pm2-manager.sh start-direct

# Check status
./pm2-manager.sh status

# View logs
./pm2-manager.sh logs
./pm2-manager.sh logs-direct

# Restart aplikasi
./pm2-manager.sh restart
./pm2-manager.sh restart-direct

# Stop aplikasi
./pm2-manager.sh stop
./pm2-manager.sh stop-direct

# Remove dari PM2
./pm2-manager.sh delete
./pm2-manager.sh delete-direct
```

### Menggunakan PM2 Commands Langsung

```bash
# Start dengan bash script
pm2 start ecosystem.config.json

# Start dengan gunicorn langsung
pm2 start ecosystem-direct.config.json

# Monitor aplikasi
pm2 monit

# Check status
pm2 status

# View logs
pm2 logs kejaksaan-app
pm2 logs kejaksaan-flask-app

# Restart
pm2 restart kejaksaan-app
pm2 restart kejaksaan-flask-app

# Stop
pm2 stop kejaksaan-app
pm2 stop kejaksaan-flask-app

# Delete
pm2 delete kejaksaan-app
pm2 delete kejaksaan-flask-app
```

## Configuration Details

### ecosystem.config.json (Bash Script Mode)
```json
{
  "name": "kejaksaan-app",
  "script": "./run_production.sh",
  "interpreter": "/bin/bash",
  "autorestart": true,
  "max_memory_restart": "1G"
}
```

### ecosystem-direct.config.json (Direct Mode)
```json
{
  "name": "kejaksaan-flask-app", 
  "script": "gunicorn",
  "args": "--bind 0.0.0.0:5001 --workers 4 app_with_db:app",
  "interpreter": "python3",
  "autorestart": true,
  "max_memory_restart": "1G"
}
```

## Log Management

Logs disimpan di direktori `./logs/`:
- `kejaksaan-app.log` - Combined logs (bash script mode)
- `kejaksaan-app-out.log` - Output logs (bash script mode)
- `kejaksaan-app-error.log` - Error logs (bash script mode)
- `kejaksaan-flask-app.log` - Combined logs (direct mode)
- `kejaksaan-flask-app-out.log` - Output logs (direct mode)
- `kejaksaan-flask-app-error.log` - Error logs (direct mode)

## Best Practices

### 1. Use Direct Mode for Production
```bash
./pm2-manager.sh start-direct
```

### 2. Auto-start on Boot
```bash
# Save current PM2 processes
pm2 save

# Generate startup script
pm2 startup

# Follow the instructions given by PM2
```

### 3. Monitor Resource Usage
```bash
# Real-time monitoring
pm2 monit

# Check memory usage
pm2 show kejaksaan-flask-app
```

### 4. Log Rotation
```bash
# Install PM2 log rotate module
pm2 install pm2-logrotate

# Configure log rotation (optional)
pm2 set pm2-logrotate:max_size 10M
pm2 set pm2-logrotate:retain 7
```

## Troubleshooting

### 1. Application Not Starting
```bash
# Check PM2 logs
pm2 logs kejaksaan-flask-app

# Check if dependencies are installed
pip3 list | grep -E "(Flask|gunicorn)"

# Check if port is available
netstat -tlnp | grep 5001
```

### 2. Memory Issues
```bash
# Check memory usage
pm2 show kejaksaan-flask-app

# Adjust max_memory_restart in config file
```

### 3. Permission Issues
```bash
# Make sure scripts are executable
chmod +x run_production.sh
chmod +x pm2-manager.sh
```

## Recommended Workflow

1. **Development**: Use `./run_app.sh`
2. **Testing Production**: Use `./run_production.sh`
3. **Production Deployment**: Use `./pm2-manager.sh start-direct`
4. **Monitoring**: Use `pm2 monit` and `pm2 logs`

## Security Notes

- Aplikasi akan bind ke `0.0.0.0:5001` (accessible dari network)
- Gunakan reverse proxy (nginx) untuk production
- Set proper firewall rules
- Monitor logs untuk suspicious activity