# KN03 - OCI Images & Container

## Inhaltsverzeichnis
- [A) Aufsetzen der EC2-Instanz mit IaC-Code - AWS LEARNER LAB](#a-aufsetzen-der-ec2-instanz-mit-iac-code---aws-learner-lab)
- [B) OCI-Images, Container und Registry - BASICS](#b-oci-images-container-und-registry---basics)
- [C) OCI-Images mit Docker - RUN & ADMINISTRATION](#c-oci-images-mit-docker---run--administration)
- [D) OCI-Images mit Docker - BUILD & CUSTOMIZATION](#d-oci-images-mit-docker---build--customization)
- [E) Container Netzwerk - VERTIEFUNG](#e-container-netzwerk---vertiefung)

## A) Aufsetzen der EC2-Instanz mit IaC-Code - AWS LEARNER LAB
Das Erstellen der Instanz war relativ einfach. Wir mussten bereits in mehreren Modulen mit AWS arbeiten. Daher sind wir uns das gewöhnt und können solch eine Instanz schnell erstellen.

Ich habe vor der Erstellung der Instanz eine Security Group erstellt. So sieht das aus:

![image](/images/07_security_group_1.png)

Im Auftrag ist IaC zu finden, welche man als **user data**, der Instanz hinzufügen muss:

```
#cloud-config

packages:
  - apt-transport-https
  - ca-certificates
  - curl
  - gnupg-agent
  - software-properties-common

# Sorgt dafür, dass auf dem Zielsystem das IPv4-Forwarding aktiviert wird, was häufig auf Routern oder in Netzwerkkonfigurationen benötigt wird, die als Gateway dienen
write_files:
  - path: /etc/sysctl.d/enabled_ipv4_forwarding.conf
    content: |
      net.ipv4.conf.all.forwarding=1

groups:
  - docker

# Install Docker and Podman: fixieren auf stabile Versionen
runcmd:
  - curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
  - add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
  - apt-get update -y
  - apt-get install -y docker-ce docker-ce-cli containerd.io
  - systemctl start docker
  - systemctl enable docker
  - apt-get install podman -y
  - systemctl start podman
  - systemctl enable podman
  - usermod -aG docker ubuntu
```

Dieses Cloud-Init Script stellt sicher, dass bei der Initalisierung der Instanz Docker und Podman installiert und mit den aktuellsten Versionen versehen wird.


Als es soweit war und ich mich verbinden konnte, habe ich sicher gestellt, dass das Script funktioniert hat.

![image](/images/08_checking_podman_docker.png)

Herausgefunden habe ich, dass Podman gar nicht läuft, was es aber sollte. Das liegt daran, dass Podman eine sogenannte **Socket-Aktivierung** nutzt. Somit läuft Podman nur, wenn man etwas damit macht. Sei es ein Image aufzusetzen oder etwas anderes. Sobald man einen Befehl eingibt, merkt der Daemon das und startet den Service automatisch.

## B) OCI-Images, Container und Registry - BASICS
In dieser Challenge mussten wir mit Docker einen **NGINX** Webserver erstellen und mittels der richtigen "Firewall-Regeln", die Webpage auf unserem Notebook aufrufen.

![image](/images/09_edited_security_group_8080.png)

![image](/images/10_started_nginx_docker.png)

Erst nach Anpassung der Security-Group können wir auf die Webseite zugreifen. Das liegt daran, dass wir der Instanz erlauben müssen, auf sich selbst HTTP einsehen zu können.

## C) OCI-Images mit Docker - RUN & ADMINISTRATION
**Schritt 1: Vorbereitungen (Prerequisites)**

- Als SQL-Client habe ich mich hier für MySQL Workbench entschieden, weil ich es bereits kenne.
- Zuerst ein Image heruntergeladen und einen Container gestartet. Dabei wurde nur Port-Forwarding zusätzlich angegeben (kein Volume).
- Security-Group ergänzt mit einer Inbound Regel für den Port 3306. Für den Zugriff von aussen.

![image](/images/14_security_group_3306.png)

- Sichergestellt, dass der Zugriff durch Workbench funktioniert.

![image](/images/11_mariadb_workbench.png)


**Schritt 2: Datenbank erstellen**

Die Datenbank habe ich bequem über Workbench erstellt: 

```create schema ... ;```

Die Datenbank finden wir ebenfalls im Docker:

![image](/images/12_mariadb_database_pet.png)

Wenn ich jetzt den Container stoppe, lösche und neu erstelle, wird diese Datenbank gelöscht sein. Aus dem Grund lohnt es sich ein Volume zu erstellen, wodurch der Speicher **persistent** wird.

![image](/images/15_created_volume.png)

Um den Speicher testen zu können, löschen wir den Container:

```
$ docker ps
$ docker stop [Container-ID] 
$ docker rm [Container-ID] 
```

Nun erstellen wir den Container erneut aber hängen das eben erstelle Volume an:

```
docker run --detach --name some-mariadb --env MARIADB_ROOT_PASSWORD=my-secret-pw -v mydbstore:/var/lib/mysql -p 3306:3306 mariadb:latest
```

Zuerst erstellen wir die Datenbank erneut auf dem Server. Danach löschen wir den Container und erstellen ihn neu mit dem erstellten Volume. Verbinde dich mittels Client wieder auf den Server und siehe da! Die Datenbank ist nachwievor vorhanden.

## D) OCI-Images mit Docker - BUILD & CUSTOMIZATION
**Variante 1: Manuelle Anpassung und Commit eines Containers**

Ein Image manuell anzupassen ist sehr einfach.

Zuerst starten wir einen Container aus einem bestehenden Image und installieren manuell die beiden Programme "Cowsay" und "Fortune". Natürlich updaten wir vorher unser Paket-Tool.
![image](/images/17_docker_starten_updaten.png)

Nachdem wir diese Schritte durchgeführt haben, konnten wir die Programme testen:
![image](/images/18_manual_install_cowsay.png)


Nun können wir den Container verlassen und den bestehenden Container als Image speichern:
![image](/images/19_checked_image_history.png) 

Mithilfe von ```docker history [IMAGE ID/NAME]``` können wir die Versionierung nachvollziehen.

Wir erstellen also unseren neuen Container aus diesem Image und testen gleich, ob Fortune und Cowsay installiert sind:
![image](/images/20_check_new_image.png)

So einfach ist es, ein Image von Hand zu updaten, patchen etc. 

**Variante 2: Automatisierte Image-Erstellung mit einem Dockerfile**

Variante Nummer 2 ist ein wenig komplexer, dafür sehr effektiv.

Nun arbeiten wir mit einem **Dockerfile** und eine **index.html** Datei. Die index.html Datei brauchen wir für unseren Webserver und mithilfe des Dockerfiles, wird unser Image erstellt.
![image](/images/21_variant-2_1.png)

**Dockerfile**

```
FROM ubuntu
RUN apt-get update && apt-get install -y cowsay fortune apache2
COPY index.html /var/www/html
CMD ["apachectl", "-D", "FOREGROUND"]
EXPOSE 80
```

Durch das Dockerfile wird ein Container mit dem Basis-Image **Ubuntu** erstellt und updated. Zusätzlich wird Cowsay, Fortune und Apache2 (Webserver) installiert.

Wir builden das neue Image und nennen es **df/cowsay**. 

Als nächstes lösche ich den Container und starte ihn erneut mit Port 80. Der Befehl lief ohne Fehler durch und die Webseite war erreichbar:
![image](/images/23_variant-2_3.png)

Ich habe das HTML-File angepasst und das Image neugebaut, sowie den Container gestartet:
![image](/images/26_variant-2_6.png)

Ebenfalls wurde das Dockerfile angepasst mit dem **ENTRYPOINT:** /usr/games/cowsay.

Das können wir mit dem History Befehl nachvollziehen:
![image](/images/25_variant-2_5.png)


## E) Container Netzwerk - VERTIEFUNG
In dieser Übung haben wir uns mit Docker Networks auseinandergesetzt. Zur Übung habe ich selbst eins erstellt und analysiert:
![image](/images/27_network_erstellt_analysiert.png)

In der **Config** sieht man die Subnetzmaske und den Gateway dieses Subnetzes.

Wenn ich einen Server erstelle und in das Netzwerk stelle, sehe ich das mit ```docker inspect pet-mynetwork```:
![image](/images/28_container_erstellt_mit_network.png)


**Befehl um unbenutzte Docker Netzwerke zu löschen:**

```
docker network prune
```