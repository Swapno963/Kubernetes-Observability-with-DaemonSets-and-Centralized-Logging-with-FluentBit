# Kubernetes Logging Architecture: Sidecar vs DaemonSet

## 🚀 Overview

This project explores **two production-grade logging patterns in Kubernetes** — **sidecar-based log collection** and **DaemonSet-based node-level aggregation** — using Fluent Bit.

**Problem Solved:**
In distributed microservices, logs are fragmented across containers and nodes, making debugging, monitoring, and incident response difficult. This project demonstrates **how to design log collection pipelines that are scalable, decoupled, and production-ready**.

**Why this architecture:**

* **Sidecar pattern** ensures tight coupling with application logs (fine-grained control).
* **DaemonSet pattern** provides cluster-wide log collection with minimal overhead.
* Combining both highlights **trade-offs between isolation vs efficiency**, a critical decision in real-world systems.

---

## 🏗️ Architecture

```text
                ┌──────────────────────┐
                │      Client          │
                └─────────┬────────────┘
                          │
                  ┌───────▼────────┐
                  │  API Gateway   │
                  └───────┬────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                                   │
┌───────▼────────┐                 ┌────────▼────────┐
│ Order Service  │                 │ Payment Service │
└───────┬────────┘                 └────────┬────────┘
        │                                   │
   ┌────▼────┐                         ┌────▼────┐
   │Sidecar  │                         │Sidecar  │
   │FluentBit│                         │FluentBit│
   └────┬────┘                         └────┬────┘
        │                                   │
        └──────────────┬────────────────────┘
                       │
             ┌─────────▼─────────┐
             │  DaemonSet (FB)   │
             │ Node-level logs   │
             └─────────┬─────────┘
                       │
               ┌───────▼────────┐
               │ Log Aggregator │
               └────────────────┘
```

**Key Design Decisions:**

* **Dual logging strategy:** Demonstrates both pod-level and node-level log collection.
* **Volume sharing:** Uses `emptyDir` for intra-pod communication and `hostPath` for node-level access.
* **ConfigMaps for configuration:** Avoids rebuilding images for log pipeline changes.

**Trade-offs:**

* **Sidecar pattern**

  * ✅ Precise control over application logs
  * ❌ Increased resource usage (one collector per pod)
* **DaemonSet pattern**

  * ✅ Efficient (one collector per node)
  * ❌ Less context awareness of individual applications

---

## ⚙️ Tech Stack

**Microservices:**

* FastAPI (API Gateway, Order Service, Payment Service)

**Logging & Observability:**

* Fluent Bit (log collection and forwarding)

**Infrastructure:**

* Kubernetes (Deployments, DaemonSets, Services)
* Docker (containerization)

**Configuration Management:**

* ConfigMaps (Fluent Bit configuration)

---

## 📦 Services / Components

* **API Gateway**

  * Entry point for all external requests
  * Routes traffic to backend services

* **Order Service**

  * Handles order creation and processing
  * Generates structured application logs

* **Payment Service**

  * Simulates payment processing
  * Produces transaction logs

* **Fluent Bit (Sidecar)**

  * Runs alongside each service container
  * Collects logs from `/app/logs`

* **Fluent Bit (DaemonSet)**

  * Runs one pod per node
  * Collects container runtime logs via `hostPath`

---

## 🔄 Request Flow

1. Client sends request to API Gateway.
2. Gateway routes request to Order or Payment service.
3. Application writes logs to `/app/logs`.
4. Sidecar Fluent Bit reads logs via shared `emptyDir` volume.
5. DaemonSet Fluent Bit collects container-level logs from node filesystem.
6. Logs are forwarded to a central aggregation system.

**Key Insight:**
This dual-path logging ensures both **application-level visibility** and **infrastructure-level observability**.

---

## 🛠️ Setup & Installation

```bash
# Clone repository
git clone <repo-url>
cd k8s-logging-architecture

# Apply ConfigMaps
kubectl apply -f k8s/configmaps/

# Deploy microservices with sidecars
kubectl apply -f k8s/deployments/

# Deploy Fluent Bit DaemonSet
kubectl apply -f k8s/daemonset/

# Verify
kubectl get pods -o wide
kubectl get daemonsets
```

---

## 🧪 Key DevOps Concepts Demonstrated

* **Sidecar Pattern**

  * Log collectors tightly coupled with application lifecycle

* **DaemonSet Pattern**

  * One pod per node for system-level log collection

* **Volume Design**

  * `emptyDir`: ephemeral, pod-scoped log sharing
  * `hostPath`: node-level log access

* **Configuration Decoupling**

  * ConfigMaps for dynamic log pipeline updates

* **Observability Design**

  * Separation of application vs infrastructure logging

---

## 🔐 Production Considerations

* **Scalability**

  * Sidecars scale with pods → predictable but costly
  * DaemonSets scale with nodes → efficient baseline

* **Security**

  * Restrict `hostPath` access (potential node-level risk)
  * Apply RBAC for logging components

* **Observability**

  * Integrate with centralized systems (ELK, Loki, etc.)
  * Use structured logging (JSON) for query efficiency

* **Failure Handling**

  * Ensure log buffering to avoid data loss
  * Monitor Fluent Bit health and backpressure

---

## 🚧 Challenges & Learnings

* **Log duplication risk**

  * Both sidecar and DaemonSet can collect overlapping logs
  * Solution: Clearly separate sources (file vs container logs)

* **Volume misconfiguration**

  * Incorrect `emptyDir` usage prevented sidecar from accessing logs
  * Fixed by aligning mount paths across containers

* **DaemonSet permissions**

  * `hostPath` required proper access rights to read node logs

* **Mental Model Shift (Important):**

  * **Junior approach:** “Logs = stdout, Kubernetes handles it”
  * **Production reality:**

    * Logs have **multiple sources (app, container, node)**
    * Collection strategy must match **debugging needs and scale constraints**

---

## 📌 Future Improvements

* Replace Fluent Bit output with real backend (Elasticsearch / Loki)
* Add log enrichment (metadata, correlation IDs)
* Introduce distributed tracing (OpenTelemetry)
* Implement log sampling to reduce cost at scale
* Add alerting based on log patterns

---

## 📸 Diagram (Simplified)

```text
[App Container] ---> /app/logs ---> [Sidecar Fluent Bit]
         │
         └──────── stdout ────────> [DaemonSet Fluent Bit]

Both → Central Log Storage
```

