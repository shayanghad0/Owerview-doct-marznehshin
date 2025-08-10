# Getting Started

Welcome to Marzneshin! This guide will help you get up and running with your new proxy management system in just a few minutes.

## Quick Start

Once you have Marzneshin installed, follow these steps to get started:

### 1. First Login

After installation, open your web browser and navigate to:

```
http://your-server-ip:8080
```

Use the default credentials:
- **Username**: `admin`
- **Password**: `admin`

> ⚠️ **Security Note**: Change these credentials immediately after your first login!

### 2. Change Default Password

1. Click on your username in the top-right corner
2. Select "Profile Settings"
3. Change your password to something secure
4. Save the changes

### 3. Create Your First User

Let's create a user account that can connect to your proxy:

1. Navigate to **Users** in the sidebar
2. Click **Add User**
3. Fill in the user details:
   - **Username**: Choose a unique username
   - **Data Limit**: Set monthly bandwidth limit (e.g., 50GB)
   - **Expiry Date**: Set when the account expires
   - **Connection Limit**: Maximum simultaneous connections

4. Select **Protocols** the user can access:
   - VLESS (recommended for performance)
   - VMess (good compatibility)
   - Trojan (bypass DPI)

5. Click **Create User**

### 4. Configure Your First Inbound

Inbounds define how clients connect to your server:

1. Go to **System** → **Inbounds**
2. Click **Add Inbound**
3. Configure basic settings:
   - **Protocol**: VLESS (recommended)
   - **Port**: 443 (or any available port)
   - **Network**: TCP or WebSocket
   - **Security**: Reality or TLS

4. Click **Add** to create the inbound

### 5. Generate Subscription Links

Users need subscription links to configure their clients:

1. Go back to **Users**
2. Find your user and click the **Link** icon
3. Copy the subscription URL
4. Share this URL with your user

## Understanding the Dashboard

### Main Dashboard

The dashboard provides an overview of your system:

- **System Status**: CPU, memory, and disk usage
- **Traffic Statistics**: Real-time bandwidth usage
- **User Overview**: Active users and their status
- **Recent Activity**: Latest connections and events

### Users Management

- **Add Users**: Create new proxy accounts
- **Monitor Usage**: Track data consumption
- **Set Limits**: Configure bandwidth and time limits
- **Reset Passwords**: Help users with access issues

### System Configuration

- **Inbounds**: Configure how clients connect
- **Settings**: System-wide preferences
- **Logs**: Monitor system activity
- **Backup**: Protect your configuration

## Client Configuration

### Automatic Configuration (Recommended)

1. Install a compatible client on user devices:
   - **Android**: V2rayNG, Clash for Android
   - **iOS**: Shadowrocket, Quantumult X
   - **Windows**: V2rayN, Clash for Windows
   - **macOS**: ClashX, V2rayU
   - **Linux**: V2ray, Clash

2. Add subscription using the URL you generated
3. Update subscription to get latest configs
4. Select a server and connect

### Manual Configuration

If automatic configuration doesn't work, you can manually configure clients using the connection details from the user's configuration page.

## Basic Troubleshooting

### Users Can't Connect

1. **Check user status**: Ensure the user account is active
2. **Verify inbound**: Make sure the inbound is running
3. **Check firewall**: Ensure the port is open
4. **Test connectivity**: Try connecting from the server location

### Slow Connection Speeds

1. **Check server resources**: Monitor CPU and memory usage
2. **Optimize inbound settings**: Try different transport protocols
3. **Location matters**: Choose servers closer to users
4. **Check network quality**: Ensure good server connectivity

### Can't Access Web Panel

1. **Check service status**: `systemctl status marzneshin`
2. **Verify port**: Ensure port 8080 is accessible
3. **Check firewall**: Allow the management port
4. **Try different browser**: Clear cache or use incognito mode

## Security Best Practices

### For Administrators

1. **Change default credentials** immediately
2. **Use strong passwords** for all accounts
3. **Enable 2FA** if available
4. **Limit admin access** to trusted IPs only
5. **Regular backups** of configuration and data
6. **Keep system updated** with latest versions

### For Users

1. **Don't share accounts** between multiple people
2. **Use updated clients** for better security
3. **Verify subscription URLs** before using
4. **Report suspicious activity** to administrators

## Performance Optimization

### Server-Side

1. **Use SSD storage** for better I/O performance
2. **Adequate RAM** (4GB+ recommended)
3. **Good network connection** with low latency
4. **Multiple CPU cores** for concurrent connections
5. **Regular monitoring** of resource usage

### Protocol Selection

- **VLESS + Reality**: Best performance and security
- **VMess + WebSocket + TLS**: Good compatibility
- **Trojan**: Excellent for bypassing restrictions
- **Hysteria**: Best for high-latency connections

## Monitoring and Maintenance

### Daily Tasks

- Check system status and resource usage
- Review user activity and data consumption
- Monitor for any connection issues
- Backup important data

### Weekly Tasks

- Update system packages
- Review and analyze logs
- Check for software updates
- Optimize performance if needed

### Monthly Tasks

- Full system backup
- Security audit
- Capacity planning
- User account cleanup

## Getting Help

### Documentation

- Read the complete [configuration guide](configuration.md)
- Check the [troubleshooting section](troubleshooting.md)
- Review [API documentation](api-reference.md)

### Community Support

- **GitHub Issues**: Report bugs and feature requests
- **Telegram Group**: Get help from the community
- **Discord Server**: Real-time chat support
- **Documentation**: Comprehensive guides and tutorials

### Professional Support

For enterprise deployments or complex setups, consider:

- Managed hosting services
- Professional consultation
- Custom development
- Training and support packages

## Next Steps

Now that you have the basics working:

1. **Explore advanced features** in the configuration guide
2. **Set up monitoring** for production use
3. **Implement backup strategies** for data protection
4. **Optimize performance** based on your usage patterns
5. **Scale your deployment** as your needs grow

Congratulations! You now have a working Marzneshin installation. The system is designed to be intuitive, but don't hesitate to explore the documentation for advanced features and optimizations.

Remember to keep your system updated and monitor its performance regularly. Happy proxying!

## Frequently Asked Questions

### Can I run multiple instances?

Yes, you can run multiple Marzneshin instances on different servers or ports. Each instance operates independently with its own database and configuration.

### What's the difference between protocols?

- **VLESS**: Lightweight, fastest, best for performance
- **VMess**: Feature-rich, good compatibility, encryption built-in
- **Trojan**: Mimics HTTPS traffic, excellent for bypassing DPI
- **Hysteria**: Uses QUIC, best for unstable networks

### How many users can I support?

This depends on your server resources and bandwidth. A typical server can support:

- **Small setup**: 50-100 concurrent users
- **Medium setup**: 200-500 concurrent users  
- **Large setup**: 1000+ concurrent users with proper hardware

### Is it safe to use?

Marzneshin implements modern security protocols and encryption. However, security also depends on:

- Proper server configuration
- Regular updates
- Strong authentication
- Network security measures

### Can I migrate from other panels?

Migration tools are available for common panels. Check the documentation for specific migration guides and scripts to help you transition your existing setup.