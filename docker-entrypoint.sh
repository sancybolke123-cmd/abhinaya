#!/bin/bash
set -e

# If DB_HOST is empty or points to localhost, start MariaDB server internally
if [ -z "$DB_HOST" ] || [ "$DB_HOST" = "127.0.0.1" ] || [ "$DB_HOST" = "localhost" ]; then
    echo "==> Starting internal MariaDB server..."
    
    mkdir -p /var/run/mysqld /var/lib/mysql
    chown -R mysql:mysql /var/run/mysqld /var/lib/mysql

    # Initialize data dir if empty
    if [ ! -d "/var/lib/mysql/mysql" ]; then
        mysql_install_db --user=mysql --datadir=/var/lib/mysql > /dev/null 2>&1 || true
    fi
    
    # Start MariaDB service
    service mariadb start || /etc/init.d/mariadb start || true
    
    # Wait for MariaDB to start up (up to 20 seconds)
    for i in {1..20}; do
        if mysqladmin ping --silent > /dev/null 2>&1; then
            echo "==> MariaDB is ready!"
            break
        fi
        sleep 1
    done
    
    # Setup database and user
    mysql -e "CREATE DATABASE IF NOT EXISTS abhinaya_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" || true
    mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' IDENTIFIED BY '' WITH GRANT OPTION; FLUSH PRIVILEGES;" || true
    mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'127.0.0.1' IDENTIFIED BY '' WITH GRANT OPTION; FLUSH PRIVILEGES;" || true
    
    # Import schema if database.sql exists
    if [ -f "/var/www/html/database.sql" ]; then
        mysql abhinaya_db < /var/www/html/database.sql || true
        echo "==> Imported database.sql successfully!"
    fi
fi

# Ensure uploads directory is writable
mkdir -p /var/www/html/uploads
chmod -R 777 /var/www/html/uploads || true

echo "==> Starting Apache web server on port 80..."
exec apache2-foreground
