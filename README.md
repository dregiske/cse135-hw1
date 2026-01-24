# CSE 135 - HOMEWORK 1

This is Andre Giske's LAMP application.

## Part 2 Section: Deploy from Github:

**Objective:** We want to keep our site in a repo at Github, and deploy automatically to Digital Ocean.

**High Level Overview (workflow):**
First I will walk you through the high-level workflow of this automation process.
(For context, I manually setup a webhook in Github which is connected specifically to andregiske.com/deploy.php)

```
Push to Github
-->
Github sends a POST request to the domain/deploy.php (in this case: https://andregiske.com/deploy.php)
-->
the deploy.php site recieves the webhook (the POST request)
-->
deploy.php verifies its origin (makes sure its from Github)
-->
deploy.php runs the deploy.sh script
-->
deploy.sh script does git pull for the latest code on the Github repo
-->
The website is updated with the latest code automatically!
```

What is a webhook?
A webhook is essentially a message that is sent from an app to another when an event happens. In this case, the event would be pushing code to the Github repo. When this event is triggered, the Github sends this message to the URL (deploy.php).

## Part 3 Section: Employ password protection:

**Login Information:**

user: grader

password: grader

## Part 3 Section: Compress Textual Content:

**Objective:** Install mod_gzip to compress pages.

**Summary:** After downloading enabling mod_gzip in Apache, the HTML, CSS, and JS files are automatically compressed before being sent to your browser.

Essentially, the browser (ex. some users computer) requests a file, then Apache will read the uncompressed file from disk, compress that file using the gzip encoding, and send that compressed version over the network. When the browser recieves this file, it decompresses it and dispays the contents on the page.

This can have many benefits as discussed in class, such as:

- Decreasing bandwidth usage
- Faster page loading times
- Decreasing bandwidth costs
- Better UX

The `Content-Encoding		gzip` as displayed in `compression-verify.jpg` tells us that the browser recieved a compressed file.

## Part 3 Section: Obscure server identity:

**Objective:** Change Server response header from default to "CSE135 Server".

**Methods Attempted:**

1. Set `ServerTokens Prod` and `ServerSignature Off` in apache2.conf and security.conf
2. Used mod_headers with multiple approaches:
   - `Header always set Server "CSE135 Server"`
   - `Header always unset Server` followed by `Header always set`
3. Configured at multiple levels: global (apache2.conf), conf.d (security.conf), and virtual host configs
4. Set `AllowOverride All` in apache2.conf for /var/www/
5. Verified mod_headers module is loaded and active

**Result:** After endless hours, I had successfully reduced server information disclosure from `Apache/2.4.58 (Ubuntu)` to `Apache`. While I hadn't completely changed the server name, it still removed the version and OS information, improving security through obscurity. Admittedly, I am stumped and couldn't figure out how to completely change the server name COMPLETELY.

## Extra Credit: Analytics Configuration

### Matomo Analytics

Installed Matomo to track website visitors and behavior.

**Installation Process:**

1. Installed required PHP extensions (curl, gd, xml, mbstring)
2. Created MySQL database and user for Matomo

```
CREATE DATABASE matomo;
CREATE USER 'matomo'@'localhost' IDENTIFIED BY 'matomo_password_123';
```

3. Downloaded and extracted Matomo to `/var/www/andregiske.com/public_html/matomo`
4. Ran web-based installer at https://andregiske.com/matomo
5. Filled out database connection and admin user
6. Added JavaScript tracking code to website pages (before the head tag ends)
7. Configured first website tracking for andregiske.com

**Access:**

- Dashboard: https://andregiske.com/matomo
- Username: `admin`
- Password: `admin_pass_1209`

The tracking code is embedded in the site's HTML and automatically collects visitor data.
