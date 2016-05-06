FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /var/www
WORKDIR /var/www
ADD ./provision/data/bashrc /root
RUN /bin/bash -c "source /root/.bashrc"
ADD ./requirements.txt /var/www
#ADD ./requirements-dev.txt /var/www
RUN pip install -r requirements.txt
ADD ./ /var/www

#LOG
RUN mkdir /var/log/rede_gsti/
RUN touch /var/log/rede_gsti/error.log


# SSH
RUN apt-get update && apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN echo 'root:docker' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

# Ugettext
RUN apt-get install -y gettext

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]