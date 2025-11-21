#!/bin/bash

# PM2 Management Script untuk Kejaksaan App
echo "Kejaksaan App - PM2 Management Script"
echo "====================================="

case "$1" in
    start)
        echo "Starting Kejaksaan App with PM2..."
        pm2 start ecosystem.config.json
        ;;
    start-direct)
        echo "Starting Kejaksaan App (Direct Python) with PM2..."
        pm2 start ecosystem-direct.config.json
        ;;
    stop)
        echo "Stopping Kejaksaan App..."
        pm2 stop kejaksaan-app
        ;;
    stop-direct)
        echo "Stopping Kejaksaan App (Direct Python)..."
        pm2 stop kejaksaan-flask-app
        ;;
    restart)
        echo "Restarting Kejaksaan App..."
        pm2 restart kejaksaan-app
        ;;
    restart-direct)
        echo "Restarting Kejaksaan App (Direct Python)..."
        pm2 restart kejaksaan-flask-app
        ;;
    status)
        echo "PM2 Status:"
        pm2 status
        ;;
    logs)
        echo "Showing logs for Kejaksaan App..."
        pm2 logs kejaksaan-app
        ;;
    logs-direct)
        echo "Showing logs for Kejaksaan App (Direct Python)..."
        pm2 logs kejaksaan-flask-app
        ;;
    delete)
        echo "Deleting Kejaksaan App from PM2..."
        pm2 delete kejaksaan-app
        ;;
    delete-direct)
        echo "Deleting Kejaksaan App (Direct Python) from PM2..."
        pm2 delete kejaksaan-flask-app
        ;;
    install-pm2)
        echo "Installing PM2..."
        npm install -g pm2
        ;;
    *)
        echo "Usage: $0 {start|start-direct|stop|stop-direct|restart|restart-direct|status|logs|logs-direct|delete|delete-direct|install-pm2}"
        echo ""
        echo "Commands:"
        echo "  start         - Start app using bash script (ecosystem.config.json)"
        echo "  start-direct  - Start app directly with gunicorn (ecosystem-direct.config.json)"
        echo "  stop          - Stop the bash script version"
        echo "  stop-direct   - Stop the direct gunicorn version"
        echo "  restart       - Restart the bash script version"
        echo "  restart-direct- Restart the direct gunicorn version"
        echo "  status        - Show PM2 status"
        echo "  logs          - Show logs for bash script version"
        echo "  logs-direct   - Show logs for direct gunicorn version"
        echo "  delete        - Remove bash script version from PM2"
        echo "  delete-direct - Remove direct gunicorn version from PM2"
        echo "  install-pm2   - Install PM2 globally"
        echo ""
        echo "Recommended: Use 'start-direct' for better performance"
        exit 1
        ;;
esac