# Configuration

This guide covers all aspects of configuring Marzneshin for optimal performance and security.

## Basic Configuration

### Environment Variables

Marzneshin uses environment variables for configuration. The main configuration file is located at `/etc/opt/marzneshin/.env` for Docker installations.

```env
# Application Settings
UVICORN_HOST=0.0.0.0
UVICORN_PORT=8000
UVICORN_SSL_CERTFILE=/path/to/cert.pem
UVICORN_SSL_KEYFILE=/path/to/key.pem

# Database Configuration
SQLALCHEMY_DATABASE_URL=sqlite:///var/lib/marzneshin/db.sqlite3

# Authentication
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440
AUTH_GENERATION_ALGORITHM=xxh128

# Subscription Settings
CUSTOM_TEMPLATES_DIRECTORY=app/templates
CLASH_SUBSCRIPTION_TEMPLATE=clash/default
```

### Database Configuration

Marzneshin supports multiple database backends:

#### SQLite (Default)
```env
SQLALCHEMY_DATABASE_URL=sqlite:///var/lib/marzneshin/db.sqlite3
```

#### MariaDB (Recommended for Production)
```env
SQLALCHEMY_DATABASE_URL=mariadb+pymysql://username:password@localhost/marzneshin
```

#### MySQL
```env
SQLALCHEMY_DATABASE_URL=mysql+pymysql://username:password@localhost/marzneshin
```

#### PostgreSQL
```env
SQLALCHEMY_DATABASE_URL=postgresql://username:password@localhost/marzneshin
```

## User Management

### Creating Admin Users

Create your first admin user:

```bash
# For Docker installations
docker exec -it marzneshin marzneshin cli admin create --sudo

# For manual installations
marzneshin-cli admin create --sudo
```

### User Permissions

Marzneshin supports role-based access control:

- **Admin**: Full system access, can manage all users and settings
- **User**: Can only manage their own subscriptions and view stats
- **Read-only**: Can only view statistics and configurations

### User Quotas and Limits

Configure user limitations:

```yaml
user_defaults:
  data_limit: 50GB        # Monthly data limit
  expire_duration: 30     # Days until expiration
  connection_limit: 5     # Simultaneous connections
  protocols:
    - vmess
    - vless
    - trojan
```

## Proxy Protocols

### VLESS Configuration

VLESS is a lightweight protocol with enhanced performance:

```json
{
  "protocol": "vless",
  "settings": {
    "clients": [],
    "decryption": "none"
  },
  "streamSettings": {
    "network": "tcp",
    "security": "reality",
    "realitySettings": {
      "dest": "www.google.com:443",
      "serverNames": ["www.google.com"],
      "privateKey": "your-private-key",
      "shortIds": ["", "0123456789abcdef"]
    }
  }
}
```

### VMess Configuration

VMess provides balanced security and performance:

```json
{
  "protocol": "vmess",
  "settings": {
    "clients": []
  },
  "streamSettings": {
    "network": "ws",
    "wsSettings": {
      "path": "/vmess",
      "headers": {
        "Host": "your-domain.com"
      }
    },
    "security": "tls"
  }
}
```

### Trojan Configuration

Trojan disguises traffic as HTTPS:

```json
{
  "protocol": "trojan",
  "settings": {
    "clients": []
  },
  "streamSettings": {
    "network": "tcp",
    "security": "tls",
    "tlsSettings": {
      "certificates": [
        {
          "certificateFile": "/path/to/cert.pem",
          "keyFile": "/path/to/key.pem"
        }
      ]
    }
  }
}
```

### Hysteria Configuration

Hysteria uses QUIC for enhanced performance:

```yaml
listen: :443
cert: /path/to/cert.pem
key: /path/to/key.pem
auth:
  type: password
  password: your-password
masquerade:
  type: proxy
  proxy:
    url: https://news.ycombinator.com/
    rewriteHost: true
```

## Network Settings

### Port Configuration

Configure ports for different protocols:

```yaml
ports:
  vless: 443
  vmess: 8080
  trojan: 8443
  hysteria: 443
  shadowsocks: 8388
```

### Traffic Routing

Configure traffic routing rules:

```json
{
  "routing": {
    "rules": [
      {
        "type": "field",
        "ip": ["geoip:private"],
        "outboundTag": "direct"
      },
      {
        "type": "field",
        "domain": ["geosite:cn"],
        "outboundTag": "direct"
      }
    ]
  }
}
```

## Security Settings

### SSL/TLS Configuration

For production deployments, configure SSL:

```bash
# Generate self-signed certificate (testing only)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Use Let's Encrypt for production
certbot certonly --standalone -d your-domain.com
```

### Firewall Rules

Configure iptables for security:

```bash
# Allow SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow HTTP/HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Allow Marzneshin panel
iptables -A INPUT -p tcp --dport 8080 -j ACCEPT

# Block everything else
iptables -A INPUT -j DROP
```

### Rate Limiting

Configure rate limiting to prevent abuse:

```yaml
rate_limits:
  connections_per_minute: 60
  bandwidth_per_user: 100MB
  max_concurrent_connections: 10
```

## Monitoring and Logging

### Log Configuration

Configure logging levels and destinations:

```yaml
logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  handlers:
    - type: file
      filename: /var/log/marzneshin/app.log
      max_size: 10MB
      backup_count: 5
    - type: console
```

### Metrics and Statistics

Enable metrics collection:

```yaml
metrics:
  enabled: true
  prometheus:
    enabled: true
    port: 9090
  grafana:
    enabled: true
    port: 3000
```

### Health Checks

Configure health check endpoints:

```yaml
health_checks:
  enabled: true
  endpoint: /health
  interval: 30s
  timeout: 5s
```

## Backup and Restore

### Automated Backups

Set up automated backups:

```bash
#!/bin/bash
# backup-marzneshin.sh

BACKUP_DIR="/opt/backups/marzneshin"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
sqlite3 /var/lib/marzneshin/db.sqlite3 ".backup $BACKUP_DIR/db_$DATE.sqlite3"

# Backup configuration
cp -r /etc/opt/marzneshin $BACKUP_DIR/config_$DATE

# Compress backup
tar -czf $BACKUP_DIR/marzneshin_backup_$DATE.tar.gz -C $BACKUP_DIR db_$DATE.sqlite3 config_$DATE

# Clean up old backups (keep last 7 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

Add to crontab for daily backups:

```bash
# Run daily at 2 AM
0 2 * * * /opt/scripts/backup-marzneshin.sh
```

### Restore from Backup

To restore from backup:

```bash
# Stop services
systemctl stop marzneshin

# Restore database
cp backup/db_20240101_020000.sqlite3 /var/lib/marzneshin/db.sqlite3

# Restore configuration
cp -r backup/config_20240101_020000/* /etc/opt/marzneshin/

# Start services
systemctl start marzneshin
```

## Performance Optimization

### Multi-Core Optimization

Configure for multiple CPU cores:

```yaml
workers: 4                    # Number of worker processes
worker_connections: 1000      # Connections per worker
keepalive_timeout: 65        # Keep connections alive
```

### Memory Management

Optimize memory usage:

```yaml
memory:
  max_memory_usage: 1GB
  garbage_collection: aggressive
  cache_size: 256MB
```

### Database Optimization

For production databases:

```sql
-- MySQL/MariaDB optimization
SET innodb_buffer_pool_size = 1GB;
SET innodb_log_file_size = 256MB;
SET max_connections = 200;
```

## Advanced Configuration

### Custom Templates

Create custom subscription templates:

```yaml
# templates/custom_clash.yaml
mixed-port: 7890
allow-lan: true
mode: rule
log-level: info

proxies: {{proxies}}

proxy-groups:
  - name: "PROXY"
    type: select
    proxies: {{proxy_names}}

rules: {{rules}}
```

### API Configuration

Configure REST API settings:

```yaml
api:
  enabled: true
  host: 0.0.0.0
  port: 8001
  cors:
    origins: ["*"]
    methods: ["GET", "POST", "PUT", "DELETE"]
  rate_limit:
    requests_per_minute: 60
```

### Integration with External Services

Configure webhooks and notifications:

```yaml
notifications:
  telegram:
    enabled: true
    bot_token: "your-bot-token"
    chat_id: "your-chat-id"
  discord:
    enabled: true
    webhook_url: "your-webhook-url"
  email:
    enabled: true
    smtp_server: "smtp.gmail.com"
    smtp_port: 587
    username: "your-email@gmail.com"
    password: "your-app-password"
```

## Troubleshooting Configuration

### Common Configuration Issues

**Invalid database URL:**
```bash
# Test database connection
python -c "from sqlalchemy import create_engine; engine = create_engine('your-database-url'); print('Connection successful!')"
```

**SSL certificate problems:**
```bash
# Verify certificate
openssl x509 -in cert.pem -text -noout

# Test SSL connection
openssl s_client -connect your-domain.com:443
```

**Permission issues:**
```bash
# Fix file permissions
chown -R marzneshin:marzneshin /opt/marzneshin
chmod 600 /etc/opt/marzneshin/.env
```

### Configuration Validation

Validate your configuration:

```bash
# Check configuration syntax
marzneshin-cli config validate

# Test configuration
marzneshin-cli config test

# Show current configuration
marzneshin-cli config show
```

This comprehensive configuration guide should help you set up Marzneshin according to your specific needs and environment.