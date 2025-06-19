# KN02 - Infrastruktur Automatisierung

## Inhaltsverzeichnis
- [A) Cloud Computing](#a-cloud-computing)
- [B) Infrastructure as Code](#b-infrastructure-as-code)
- [C) Globale Cloud-Plattformen](#c-globale-cloud-plattformen)

## A) Cloud Computing

### Aufgabe 1
1. Hosting von virtuellen Maschinen. --> **IaaS**
2. Nutzung von Google Docs für die Textbearbeitung. --> **SaaS** 
3. Containerverwaltung mit Kubernetes. --> **CaaS**

### Aufgabe 2
**Was ist der Unterschied zwischen IaaS und PaaS?**

Bei IaaS werden Hardware-Ressourcen geboten. Also anstelle von einem eigenen Rechenzentrum mit Virtuellen Maschinen, befindet sich das Rechenzentrum an einem anderen Ort (in der Cloud). Amazon kümmert sich in dem Fall um die Hardware. Wartungsarbeiten oder ähnliches fallen dafür also weg.

Platform as a Service oder kurz PaaS bietet, wie der Name schon sagt, eine Plattform. Meistens wird PaaS in der Entwicklung verwendet. Entwickler können sich eine fertig eingerichtete Entwicklungsplattform anmieten und müssen sich weder um die Hardware, noch dem Betriebssystem und alles was auf derselben Ebene ist, kümmern.

## B) Infrastructure as Code 

### Aufgabe 1
- Warum ist es besser, IT-Systeme automatisch zu konfigurieren statt manuell?
    - Es wird Zeit gespart indem Systeme automatisiert konfiguriert oder gar aufgesetzt werden.

- Was bedeutet Infrastructure as Code (IaC)?
    - Infrastructure as Code bedeutet, dass wir anstelle einer manuellen Installation und Konfiguration mehrer Systeme, Konfigurationsdateien haben, die automatisch interpretiert und umgesetzt werden können.

### Aufgabe 2
- Befassen Sie sich mit zwei Tools, die bei IaC verwendet werden (z.B. Docker, Terraform) und erklären sie kurz, was diese tun.
    - Docker vereinfacht den ganzen Prozess, indem es Images unterstützt, die einfach zusammengestellt werden können.

- Recherchieren Sie die Begriffe Kubernetes und Container-Orchestrierung. Fassen Sie in Stichworten zusammen, was damit gemeint ist und was Sie darunter verstehen.
    - Kubernetes ist eine Plattform für Container Orchestrierung, welche die nötigen Mittel bereitstellt.
    - Conatiner Orchestrierung wird zur Automatisierung und Verwaltung von Aufgaben verwendet. Diese Aufgaben beinhalten: Deployment und Provisionierugn, Konfiguration und Planung, Ressourcenzuweisung, Containerverfügbarkeit und noch mehr.


## C) Globale Cloud-Plattformen

### Aufgabe 1
| Cloud-Anbieter | Regionen (aktiv) | Verfügbarkeitszonen (aktiv) |
| -------------- | ---------------- | --------------------------- |
| **AWS**        | 36               | 114                         |
| **Azure**      | 64               | 126                         |
| **GCP**        | 47               | 127                         |


### Aufgabe 2

| Merkmal                    | **AWS EC2**                                                                                         | **Azure Virtual Machines**                                                                                      | **Google Compute Engine (GCE)**                                                                                  |
|----------------------------|---------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| **Dienstname**             | Amazon Elastic Compute Cloud (EC2)                                                                | Azure Virtual Machines                                                                                        | Google Compute Engine                                                                                        |
| **Hypervisor**             | Xen und Nitro                                                                                    | Microsoft Hyper-V                                                                                            | KVM (Kernel-based Virtual Machine)                                                                           |
| **Instanztypen**           | Breites Spektrum: z. B. T3 (burstable), M5 (general purpose), C6g (compute-optimiert), P5 (GPU)  | Vielfältige VM-Serien: z. B. Dv5 (general purpose), Fsv2 (compute-optimiert), Ev5, NC-Serie (GPU)            | Standard-, High-Memory-, High-CPU-, Memory-Optimized- und GPU-Instanzen                                      |
| **Skalierbarkeit**         | Auto Scaling, EC2 Fleet, Elastic Load Balancing                                                  | Virtual Machine Scale Sets mit automatischer Skalierung und Lastverteilung                                   | Managed Instance Groups mit automatischer Skalierung und Load Balancing                                     |
| **Preismodelle**           | On-Demand, Reserved Instances, Spot Instances, Savings Plans                                     | Pay-as-you-go, Reserved Instances, Spot VMs                                                                   | On-Demand, Committed Use Discounts, Preemptible VMs                                                           |
| **Abrechnungseinheit**     | Sekundengenau mit einem Minimum von 60 Sekunden                                                  | Minutengenau                                                                                                  | Minutengenau mit 10-Minuten-Mindestabrechnung                                                                |
| **Speicheroptionen**       | Amazon EBS (persistent), Instance Store (ephemeral)                                               | Azure Managed Disks (Standard HDD/SSD, Premium SSD), Ephemeral OS Disks                                      | Persistent Disks (Standard/SSD), Local SSDs                                                                   |
| **Verfügbarkeit**          | 36 Regionen mit 114 Verfügbarkeitszonen                                                          | 64 Regionen mit 126 Verfügbarkeitszonen                                                                       | 47 Regionen mit 127 Verfügbarkeitszonen                                                                       |
| **Sicherheitsfunktionen**  | Sicherheitsgruppen, Netzwerk-ACLs, IAM-Rollen, Nitro-Sicherheitschip                            | Netzwerk-Sicherheitsgruppen, Azure Active Directory, rollenbasierte Zugriffskontrolle (RBAC)                 | Firewall-Regeln, IAM, VPC-Netzwerke, Verschlüsselung im Ruhezustand und während der Übertragung              |
| **Verwaltungstools**       | AWS Management Console, AWS CLI, SDKs, CloudFormation                                             | Azure Portal, Azure CLI, PowerShell, ARM Templates                                                            | Google Cloud Console, gcloud CLI, Deployment Manager                                                          |
