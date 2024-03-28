FROM python:3.9-buster

# install nginx
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends

# Copy the workspace
# TODO: clone from git
RUN mkdir -p /tax_assistant
ADD . /tax_assistant
WORKDIR /tax_assistant

# configure nginx
RUN cp /tax_assistant/deployment/nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# Install dependencies
RUN pip install -r requirements.txt
RUN chown -R www-data:www-data /tax_assistant

# start server
EXPOSE 8020
STOPSIGNAL SIGTERM
CMD ["/tax_assistant/deployment/startup.sh"]