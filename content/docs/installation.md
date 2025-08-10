# Installation

This comprehensive guide will walk you through installing Marzneshin on your system, from basic setup to advanced configurations.

## System Requirements

Before installing Marzneshin, ensure your system meets these requirements:

### Minimum Requirements
- **Operating System**: Linux (Ubuntu 20.04+, Debian 11+, CentOS 8+)
- **RAM**: 1GB minimum (2GB recommended)
- **Storage**: 10GB free space
- **CPU**: 1 core (2+ cores recommended for better performance)
- **Network**: Stable internet connection

### Recommended Requirements
- **RAM**: 4GB or more
- **CPU**: 4+ cores for optimal multi-core performance
- **Storage**: 20GB+ SSD storage
- **Network**: High-bandwidth connection for proxy services

## Installation Methods

### Quick Install (Recommended)

The fastest way to get Marzneshin running is using our automated installer:

```bash
# Download and run the installation script
sudo bash -c "$(curl -sL https://github.com/marzneshin/marzneshin/raw/main/install.sh)"
```

This script will:
- Install Docker and Docker Compose
- Download Marzneshin
- Set up initial configuration
- Start all services

### Docker Installation

If you prefer manual Docker setup:

```bash
# Create project directory
mkdir marzneshin && cd marzneshin

# Download docker-compose file
wget -N https://raw.githubusercontent.com/marzneshin/marzneshin/main/docker-compose.yml

# Start services
docker-compose up -d
```

### Manual Installation

For advanced users who want full control:

#### 1. Install Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx
```

**CentOS/RHEL:**
```bash
sudo yum update
sudo yum install -y python3 python3-pip nginx
```

#### 2. Create User and Directory

```bash
# Create marzneshin user
sudo useradd -r -s /bin/false marzneshin

# Create application directory
sudo mkdir /opt/marzneshin
sudo chown marzneshin:marzneshin /opt/marzneshin
```

#### 3. Download and Setup

```bash
# Switch to marzneshin user
sudo -u marzneshin -s

# Navigate to directory
cd /opt/marzneshin

# Clone repository
git clone https://github.com/marzneshin/marzneshin.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

#### 4. Configuration

```bash
# Copy configuration template
cp config.example.yml config.yml

# Edit configuration (see Configuration section)
nano config.yml
```

#### 5. Install Xray Core

```bash
# Download and install Xray
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install
```

#### 6. Create Systemd Service

Create `/etc/systemd/system/marzneshin.service`:

```ini
[Unit]
Description=Marzneshin Proxy Manager
After=network.target

[Service]
Type=simple
User=marzneshin
WorkingDirectory=/opt/marzneshin
ExecStart=/opt/marzneshin/venv/bin/python -m marzneshin
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable marzneshin
sudo systemctl start marzneshin
```

## Post-Installation Setup

### 1. First Login

After installation, access the web panel:

```
http://your-server-ip:8080
```

Default credentials:
- **Username**: `admin`
- **Password**: `admin`

> ⚠️ **Important**: Change the default password immediately after first login!

### 2. SSL Certificate (Recommended)

For production use, set up SSL:

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 3. Firewall Configuration

Configure firewall to allow necessary ports:

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw allow 8080/tcp    # Marzneshin panel
sudo ufw enable

# Or iptables
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
```

## Verification

Check if installation was successful:

```bash
# Check service status
sudo systemctl status marzneshin

# Check logs
sudo journalctl -u marzneshin -f

# Test web panel
curl -I http://localhost:8080
```

## Troubleshooting

### Common Issues

**Service won't start:**
```bash
# Check logs for errors
sudo journalctl -u marzneshin --no-pager

# Check configuration
sudo -u marzneshin /opt/marzneshin/venv/bin/python -m marzneshin --check-config
```

**Can't access web panel:**
- Check firewall settings
- Verify port 8080 is not blocked
- Check if service is running: `sudo systemctl status marzneshin`

**Database connection errors:**
- Ensure database service is running
- Check database credentials in config.yml
- Verify network connectivity

### Getting Help

If you encounter issues:

1. Check the [troubleshooting guide](troubleshooting.md)
2. Search [GitHub issues](https://github.com/marzneshin/marzneshin/issues)
3. Join our [community channels](about.md#community)
4. Create a new issue with detailed logs

## Next Steps

After successful installation:

1. [Configure your first user](configuration.md#user-management)
2. [Set up proxy protocols](configuration.md#protocols)
3. [Configure monitoring](configuration.md#monitoring)
4. [Set up backups](configuration.md#backup-restore)

Congratulations! Marzneshin is now installed and ready to use.