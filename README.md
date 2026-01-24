# CSE 135 - HOMEWORK 1
This is Andre Giske's LAMP application.

## Server Header Obfuscation

**Objective:** Change Server response header from default to "CSE135 Server"

**Methods Attempted:**
1. Set `ServerTokens Prod` and `ServerSignature Off` in apache2.conf and security.conf
2. Used mod_headers with multiple approaches:
   - `Header always set Server "CSE135 Server"`
   - `Header always unset Server` followed by `Header always set`
   - `Header always edit Server` with regex patterns
3. Configured at multiple levels: global (apache2.conf), conf.d (security.conf), and virtual host configs
4. Set `AllowOverride All` in apache2.conf for /var/www/
5. Verified mod_headers module is loaded and active

**Result:** Successfully reduced server information disclosure from `Apache/2.4.58 (Ubuntu)` to `Apache` using ServerTokens Prod. This removes version and OS information, improving security through obscurity.

**Note:** Complete custom header override requires either:
- Compiling Apache from source with modifications
- Using a reverse proxy (nginx/HAProxy) in front of Apache
- Apache module like mod_security with SecServerSignature directive

The achieved result still provides security benefits by hiding specific version information.
