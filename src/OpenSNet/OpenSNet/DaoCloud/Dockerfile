FROM busybox:latest

ADD ./bin /opt/bin

ENV PORT 8080
ENV INTERVAL 180
ENV TARGET 115.239.134.167

EXPOSE 8080

ENTRYPOINT ["/opt/bin/entrypoint.sh"]
CMD ["/opt/bin/OpenSNet"]
