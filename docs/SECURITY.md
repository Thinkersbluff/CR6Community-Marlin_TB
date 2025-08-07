# Security Guidelines

## GPG Key Management

This project uses Docker for containerized builds, which requires proper GPG key management for package verification.

### Current Key Requirements

- **Docker Repository Keys**: Automatically managed by Docker installation
- **Microsoft Repository Keys**: Required for VS Code integration (if used)

### Key Locations

Keys are stored in standard Linux locations:
- `/etc/apt/keyrings/` - Modern keyring location
- `/etc/apt/trusted.gpg.d/` - Legacy but still used location

### Verification

To verify installed keys:
```bash
# List all trusted keys
ls -la /etc/apt/trusted.gpg.d/

# Check specific key details
gpg --show-keys /etc/apt/trusted.gpg.d/packages.microsoft.gpg
```

### Key Sources

All keys should be obtained from official sources:
- **Docker**: `https://download.docker.com/linux/ubuntu/gpg`
- **Microsoft**: `https://packages.microsoft.com/keys/microsoft.asc`

### Best Practices

1. **Never commit private keys** to the repository
2. **Verify key fingerprints** against official documentation
3. **Use containerized builds** to isolate key requirements
4. **Document key sources** and verification steps

### Troubleshooting

Common GPG-related issues:
- **"NO_PUBKEY" errors**: Missing GPG key for repository
- **"signatures couldn't be verified"**: Key not in trusted keyring
- **Permission issues**: Incorrect key file permissions

See [BUILD_AND_TEST.md](BUILD_AND_TEST.md) for setup instructions.
