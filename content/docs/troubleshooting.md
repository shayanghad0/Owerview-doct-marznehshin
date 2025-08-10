# Troubleshooting

This guide helps you resolve common issues when using Marzneshin.

## Common Installation Issues

### Docker Installation Problems

**Error: Cannot connect to Docker daemon**
```bash
# Solution: Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in for changes to take effect
```

**Error: Permission denied while trying to connect to Docker**
```bash
# Fix Docker socket permissions
sudo chmod 666 /var/run/docker.sock
# Or restart Docker service
sudo systemctl restart docker
```

**Error: Port already in use**
```bash
# Check what's using the port
sudo netstat -tulpn | grep :8080

# Kill the process using the port
sudo kill -9 <process_id>

# Or change the port in docker-compose.yml
```

### Installation Script Failures

**Error: Command not found after installation**
```bash
# Reload your shell configuration
source ~/.bashrc
# Or
source ~/.zshrc

# Check if path is correctly set
echo $PATH
```

**Error: Database connection failed**
```bash
# Check database service status
systemctl status mariadb
# Or for MySQL
systemctl status mysql

# Restart database service
sudo systemctl restart mariadb
```

## Configuration Issues

### Environment Variables

**Error: Invalid configuration file**
```bash
# Validate .env file syntax
# Check for missing quotes around values with spaces
SQLALCHEMY_DATABASE_URL="mysql://user:pass@localhost/db"

# Verify file permissions
chmod 600 /etc/opt/marzneshin/.env
```

**Error: Database URL malformed**
```bash
# Correct format examples:
# SQLite
SQLALCHEMY_DATABASE_URL=sqlite:///var/lib/marzneshin/db.sqlite3

# MySQL/MariaDB
SQLALCHEMY_DATABASE_URL=mysql+pymysql://user:password@localhost/marzneshin

# PostgreSQL
SQLALCHEMY_DATABASE_URL=postgresql://user:password@localhost/marzneshin
```

### SSL Certificate Issues

**Error: SSL certificate verification failed**
```bash
# Check certificate validity
openssl x509 -in /path/to/cert.pem -text -noout

# Verify certificate chain
openssl verify -CAfile /path/to/ca.pem /path/to/cert.pem

# Test SSL connection
openssl s_client -connect your-domain.com:443
```

**Error: Certificate file not found**
```bash
# Check file paths in configuration
ls -la /path/to/cert.pem
ls -la /path/to/key.pem

# Verify file permissions
chmod 644 /path/to/cert.pem
chmod 600 /path/to/key.pem
```

## Runtime Issues

### Service Won't Start

**Check service status**
```bash
# For Docker installations
docker ps -a
docker logs marzneshin

# For manual installations
systemctl status marzneshin
journalctl -u marzneshin -f
```

**Common service startup failures:**

1. **Port binding errors**
   ```bash
   # Change port in configuration
   nano /etc/opt/marzneshin/.env
   # Update UVICORN_PORT=8001
   ```

2. **Database connection errors**
   ```bash
   # Test database connection
   mysql -u username -p -h localhost marzneshin
   # Or for PostgreSQL
   psql -U username -h localhost -d marzneshin
   ```

3. **Permission errors**
   ```bash
   # Fix file ownership
   sudo chown -R marzneshin:marzneshin /opt/marzneshin
   sudo chown -R marzneshin:marzneshin /var/lib/marzneshin
   ```

### Performance Issues

**High CPU usage**
```bash
# Check running processes
htop
# Or
ps aux | grep marzneshin

# Monitor resource usage
docker stats  # For Docker installations
```

**Memory leaks**
```bash
# Monitor memory usage over time
free -h
# Check swap usage
swapon --show

# Restart service to clear memory
systemctl restart marzneshin
```

**Slow database queries**
```bash
# For MySQL/MariaDB, enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;

# Analyze slow queries
mysqldumpslow /var/log/mysql/slow.log
```

## Network and Connectivity Issues

### Can't Access Web Panel

**Check firewall settings**
```bash
# UFW (Ubuntu)
sudo ufw status
sudo ufw allow 8080

# iptables
sudo iptables -L
sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
```

**Check if service is listening**
```bash
# Check if port is open
sudo netstat -tulpn | grep :8080
# Or
sudo ss -tulpn | grep :8080
```

**Test local connectivity**
```bash
# Test from server
curl -I http://localhost:8080

# Test specific IP
curl -I http://your-server-ip:8080
```

### Proxy Connection Issues

**VLESS connection failures**
```bash
# Check Xray logs
journalctl -u xray -f

# Verify Xray configuration
xray -test -config /etc/xray/config.json
```

**VMess connection problems**
```bash
# Check WebSocket path configuration
# Ensure path matches in both server and client

# Verify TLS certificate if using TLS
openssl s_client -servername your-domain.com -connect your-domain.com:443
```

**Trojan connection issues**
```bash
# Check certificate configuration
# Trojan requires valid TLS certificates

# Verify certificate matches domain
openssl x509 -in cert.pem -noout -subject
```

## User Management Issues

### Can't Create Admin User

**Permission errors**
```bash
# Run with proper permissions
sudo -u marzneshin marzneshin-cli admin create --sudo

# For Docker
docker exec -it marzneshin marzneshin cli admin create --sudo
```

**Database access errors**
```bash
# Check database permissions
GRANT ALL PRIVILEGES ON marzneshin.* TO 'username'@'localhost';
FLUSH PRIVILEGES;
```

### User Authentication Problems

**JWT token issues**
```bash
# Check token expiration settings in .env
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Clear browser cache and cookies
# Try incognito/private browsing mode
```

**Password reset problems**
```bash
# Reset admin password via CLI
marzneshin-cli admin reset-password username

# For Docker
docker exec -it marzneshin marzneshin cli admin reset-password username
```

## Backup and Recovery Issues

### Backup Failures

**Database backup errors**
```bash
# Check database connection
mysql -u username -p -e "SHOW DATABASES;"

# Verify backup directory permissions
ls -la /opt/backups/
sudo chown marzneshin:marzneshin /opt/backups/
```

**File permission errors**
```bash
# Fix backup script permissions
chmod +x /opt/scripts/backup-marzneshin.sh

# Check cron job logs
grep CRON /var/log/syslog
```

### Recovery Problems

**Database restore failures**
```bash
# Stop service before restore
systemctl stop marzneshin

# Restore with proper user
sudo -u marzneshin mysql -u username -p marzneshin < backup.sql

# Restart service
systemctl start marzneshin
```

## Monitoring and Logging

### Log Analysis

**Enable debug logging**
```bash
# Add to .env file
LOG_LEVEL=DEBUG

# Restart service
systemctl restart marzneshin
```

**Check different log sources**
```bash
# Application logs
journalctl -u marzneshin -f

# Docker logs
docker logs -f marzneshin

# System logs
tail -f /var/log/syslog

# Nginx logs (if using reverse proxy)
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Health Check Issues

**Health endpoint not responding**
```bash
# Test health endpoint
curl http://localhost:8080/health

# Check if health checks are enabled in configuration
grep -i health /etc/opt/marzneshin/.env
```

## Getting Help

### Gathering Information for Support

When seeking help, please provide:

1. **System information**
   ```bash
   uname -a
   cat /etc/os-release
   docker --version  # If using Docker
   ```

2. **Service status**
   ```bash
   systemctl status marzneshin
   docker ps -a  # If using Docker
   ```

3. **Log excerpts**
   ```bash
   journalctl -u marzneshin --since "1 hour ago"
   ```

4. **Configuration (redacted)**
   ```bash
   # Remove sensitive information before sharing
   cat /etc/opt/marzneshin/.env | sed 's/password.*/password=REDACTED/'
   ```

### Community Resources

- **GitHub Issues**: [marzneshin/marzneshin/issues](https://github.com/marzneshin/marzneshin/issues)
- **Documentation**: [docs.marzneshin.org](https://docs.marzneshin.org)
- **Telegram Group**: [t.me/marzneshin](https://t.me/marzneshin)
- **Discord Server**: [discord.gg/marzneshin](https://discord.gg/marzneshin)

### Reporting Bugs

When reporting bugs, include:

1. **Expected behavior**: What should happen
2. **Actual behavior**: What actually happens
3. **Steps to reproduce**: Detailed steps to reproduce the issue
4. **Environment**: OS, version, installation method
5. **Logs**: Relevant log excerpts
6. **Configuration**: Sanitized configuration files

Remember to remove sensitive information like passwords, tokens, and private keys before sharing configuration files or logs.

## Emergency Recovery

### Complete System Recovery

If your Marzneshin installation is completely broken:

1. **Stop all services**
   ```bash
   systemctl stop marzneshin
   docker-compose down  # If using Docker
   ```

2. **Backup current state**
   ```bash
   cp -r /etc/opt/marzneshin /tmp/marzneshin-backup
   cp /var/lib/marzneshin/db.sqlite3 /tmp/db-backup.sqlite3
   ```

3. **Reinstall from scratch**
   ```bash
   # Remove current installation
   rm -rf /opt/marzneshin
   
   # Run fresh installation
   sudo bash -c "$(curl -sL https://github.com/marzneshin/marzneshin/raw/main/install.sh)"
   ```

4. **Restore data**
   ```bash
   # Stop new service
   systemctl stop marzneshin
   
   # Restore database
   cp /tmp/db-backup.sqlite3 /var/lib/marzneshin/db.sqlite3
   
   # Restore configuration (review before restoring)
   cp /tmp/marzneshin-backup/.env /etc/opt/marzneshin/
   
   # Start service
   systemctl start marzneshin
   ```

This emergency recovery process should get you back to a working state while preserving your data and configuration.