FROM nginx
COPY . /frontend
ENV NGINX_ROOT_PREFIX=""
RUN mkdir /logs && \
    mkdir /logs/nginx && \
    cat /frontend/etc/nginx-template.conf | envsubst > /frontend/etc/nginx.conf
EXPOSE 80
ENTRYPOINT ["nginx", "-c", "/frontend/etc/nginx.conf"]
