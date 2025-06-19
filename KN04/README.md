# KN04 - Containers in Action & Orchestration

## Inhaltsverzeichnis
- [A) Docker Image aufsetzen, in Registry ablegen und deployen - OCI: BASIC WORKFLOW](#a-docker-image-aufsetzen-in-registry-ablegen-und-deployen---oci-basic-workflow)
- [Docker Compose - Container Orchestrierung mit mehreren Services - CONTAINER MANAGEMENT: ENTRY-LEVEL](#b-docker-compose---container-orchestrierung-mit-mehreren-services---container-management-entry-level)
- [C) Docker Swarm Cluster aufsetzen - SETUP HIGH AVAILABILITY PLATFORM](#c-docker-swarm-cluster-aufsetzen---setup-high-availability-platform)
- [D) Docker Swarm Imperativ - CONTAINER ORCHESTRATION: ENTRY-LEVEL](#d-docker-swarm-imperativ---container-orchestration-entry-level)
- [E) Docker Swarm Deklarativ - CONTAINER ORCHESTRATION: ADVANCED-LEVEL](#e-docker-swarm-deklarativ---container-orchestration-advanced-level)

## A) Docker Image aufsetzen, in Registry ablegen und deployen - OCI: BASIC WORKFLOW
Damit ich mein Image von Lokal ins Repo hochladen kann, muss ich zuerst ein PAT für meinen Github-Account erstellen.

Damit kann ich das Docker-Login mit meiner Github Container-Registry verbinden.

Ich habe damit begonnen, indem ich das Repo geklont habe. An den Dateien ändere ich vorerst nichts. Dafür erstelle ich das Image aus den Dateien:
![image](/images/29_image_erstellen_aus_template.png)

Das hat funktioniert. Also habe ich das Image in mein Github hochgeladen und gleich gestartet:
![image](/images/30_container_gestartet_getestet.png)

Das hat auch wunderbar funktioniert. Um zu testen ob die App wirklich in meiner Registry ist, muss ich das Image und den Container lokal löschen und den run Befehl nochmals ausführen:
![image](/images/31_container_gelöscht_neu_gepullt.png)

Das hat ebenfalls funktioniert. Als nächstes muss ich die Anpassungen durchführen. Beginnen wir mit der Hintergrundfarbe:
![image](/images/32_farbe_html_angepasst.png)

Danach habe ich den Pfad zum neuen Bild abgeändert:
![image](/images/33_bild_geändert.png)

Zusätzlich habe ich im Dockerfile ```EXPOSE``` den neuen Port hinzugefügt, sowie den Port im app.js abgeändert:
![image](/images/35_dockerfile_angepasst.png)

Damit wir auf den Webserver mit dem neuen Port zugreifen können, müssen wir die Security-Group ergänzen:
![image](/images/36_security_group_angepasst.png)

Es sind alle Änderungen durch, also erstellen wir das neue Image mit dem richtigen Namen und publishen ihn in unserem Github. Wenn das funktioniert hat, löschen wir das lokale Image und den Container und erstellen den Container neu, jetzt mit dem Code aus der Registry:
![image](/images/37_image_neuerstellt.png)

Die Änderungen wurden übernommen!
![image](/images/38_aenderungen_uebernommen.png)


## B) Docker Compose - Container Orchestrierung mit mehreren Services - CONTAINER MANAGEMENT: ENTRY-LEVEL



## C) Docker Swarm Cluster aufsetzen - SETUP HIGH AVAILABILITY PLATFORM



## D) Docker Swarm Imperativ - CONTAINER ORCHESTRATION: ENTRY-LEVEL



## E) Docker Swarm Deklarativ - CONTAINER ORCHESTRATION: ADVANCED-LEVEL
