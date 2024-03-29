# Dockerfile

FROM python:3.7-buster

# install nginx
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# copy source and install dependencies
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/ProgettoArduAlessio
COPY ProgettoArduAlessio/requirements.txt start-server.sh /opt/app/
COPY ProgettoArduAlessio /opt/app/ProgettoArduAlessio/
WORKDIR /opt/app
RUN pip install -r ProgettoArduAlessio/requirements.txt --cache-dir /opt/app/pip_cache
RUN chown -R www-data:www-data /opt/app
RUN ["chmod", "+x", "start-server.sh"]

# start server
EXPOSE 8020
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]