FROM php:8.2-apache

# Install MariaDB server and client utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    mariadb-server \
    mariadb-client \
    && rm -rf /var/lib/apt/lists/*

# Install PDO MySQL and MySQLi extensions
RUN docker-php-ext-install pdo pdo_mysql mysqli

# Enable Apache mod_rewrite
RUN a2enmod rewrite

# Copy all project files to Apache web root
COPY . /var/www/html/

# Set DirectoryIndex so home.html is the default homepage
RUN echo "DirectoryIndex home.html index.php index.html" > /etc/apache2/mods-enabled/dir.conf

# Setup permissions
RUN mkdir -p /var/www/html/uploads /var/run/mysqld /var/lib/mysql \
    && chown -R www-data:www-data /var/www/html/uploads \
    && chmod -R 775 /var/www/html/uploads \
    && chown -R mysql:mysql /var/lib/mysql /var/run/mysqld

# Copy entrypoint script and make it executable
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
