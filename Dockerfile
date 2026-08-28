FROM php:8.2-apache

# Install PDO MySQL and MySQLi extensions
RUN docker-php-ext-install pdo pdo_mysql mysqli

# Enable Apache mod_rewrite
RUN a2enmod rewrite

# Copy all project files to Apache web root
COPY . /var/www/html/

# Set DirectoryIndex so home.html is the default homepage
RUN echo "DirectoryIndex home.html index.php index.html" >> /etc/apache2/apache2.conf

# Ensure uploads directory exists and has proper permissions
RUN mkdir -p /var/www/html/uploads \
    && chown -R www-data:www-data /var/www/html/uploads \
    && chmod -R 775 /var/www/html/uploads

EXPOSE 80

CMD ["apache2-foreground"]
