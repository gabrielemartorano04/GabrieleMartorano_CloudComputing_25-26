# 🚗 NGSIM Vehicle Trajectory Scenario Extraction

This project processes vehicle trajectory data from the **NGSIM (US-101)** dataset to automatically detect and classify common highway driving scenarios: **Lane Changes**, **Car-Following**, and **Cut-Ins**. 

The project was developed in two distinct phases for the *SOFE 4630U: Cloud Computing* course, demonstrating the evolution of a data processing pipeline from a localized monolithic application to a scalable, cloud-native microservices architecture.

* **University:** Ontario Tech University — Canada
* **Course:** Cloud Computing (SOFE 4630U)
* **Professor:** Prof. Mohamed El-Darieby
* **Authors:** Ishmeet Kaur, Brandon Ho, Gabriele Martorano and Anuj Shukla 

> ⚠️ **Note on Codebase:** The source code currently available in this repository implements the **Phase 1 (Monolithic)** architecture. The **Phase 2 (Microservices)** design is fully detailed in the accompanying documentation to illustrate how the system scales in a cloud environment.

---

## 📊 Dataset Overview

The project utilizes the widely-recognized NGSIM US-101 vehicle trajectory dataset (`trajectories-0820am-0835am.csv`), which contains detailed frame-by-frame tracking of vehicles on a highway segment.

> 📥 **Action Required:** Due to its large size, the raw dataset is not tracked in the main branch. Please download it directly from the **[GitHub Releases]** page of this repository and place it in the `data/` directory before running the code.

---

## 🧠 Scenario Detection Logic

Regardless of the underlying architecture (Phase 1 or Phase 2), the system analyzes continuous 5-second windows of traffic data to identify specific vehicle interactions:

* 🔄 **Lane Change:** Detected when a vehicle's `Lane_ID` changes within the observation time window.
* 🚙 **Car-Following:** Detected when two vehicles share the same lane, remain within 30 meters of each other, and maintain a velocity difference of less than `5 m/s`.
* ✂️ **Cut-In:** Detected when a vehicle starts in a different lane, ends in the ego vehicle's lane, and positions itself less than 30 meters directly ahead of the ego vehicle.

---

## 🏗️ Phase 1: Monolithic Implementation (Code Available)

In Phase 1, the system is designed as a modular but monolithic data pipeline meant to be executed locally or on a single Virtual Machine.

### Pipeline Workflow
1. **Data Ingestion:** Loads the heavy CSV dataset into memory using `pandas`.
2. **Preprocessing:** Cleans the data and sorts vehicle observations strictly by frame order.
3. **Window Segmentation:** Slices the data into overlapping sliding windows of 50 rows (representing approximately 5 seconds of traffic at 10 FPS).
4. **Scenario Detection:** Applies the algorithmic detection logic to each data window.
5. **Output:** Generates a summary CSV file with labeled scenarios and dynamic GIF visualizations tracking the ego vehicle.

### 🚀 How to Run (Phase 1)
Ensure you have Python 3.10+ installed on your machine.

1. Clone the repository and navigate to the extractor folder:
   ```bash
   cd "Phase 1 - Monolithic System/ngsim-scenario-extractor"


### 🚀 How to Run (Phase 1)
Ensure you have Python 3.10+ installed.

1. Clone the repository and navigate to the extractor folder:
   ```bash
   cd "Phase 1 - Monolithic System"/ngsim-scenario-extractor
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute the main data pipeline script:
   ```bash
   python main.py
   ```
4. **Results:** The output dataset (`scenario_output.csv`) and the generated visualizations (`Car_Following.gif`, `Lane_Change.gif`, `Cut-In.gif`) will be automatically saved in your working directory.

## ☁️ Phase 2: Microservices Architecture (Design & Evolution)

To overcome the inherent limitations of the monolithic approach (such as memory bottlenecks and rigid row-based segmentation), Phase 2 re-architects the system into a distributed, event-driven pipeline deployed on **Google Cloud Platform (GCP)**.

### Cloud Components & Scalability

- 🪣 **Cloud Storage (Input):** Hosts the raw NGSIM dataset, decoupling heavy storage from compute instances.
- 📨 **Data Ingestion Service:** Reads the data from Cloud Storage and streams it row-by-row into a Pub/Sub topic.
- 🚦 **Google Cloud Pub/Sub:** Acts as an asynchronous message queue, buffering incoming data streams to ensure fault tolerance.
- ⚙️ **Google Cloud Dataflow (Apache Beam):** Replaces the single-thread Pandas logic. It dynamically scales worker nodes to process the stream in parallel. Crucially, it replaces the rigid 50-row chunking with native time-based windowing (`beam.window.FixedWindows(5)`) using the `Global_Time` timestamp, seamlessly handling any dropped frames.
- 🗄️ **Cloud Storage (Output):** Stores the detected scenarios as highly structured JSON files for downstream analytics or dashboarding.

> 📄 **Deep Dive:** For a comprehensive breakdown of the Phase 2 implementation, deployment steps, and architectural comparisons, please refer to the Phase 2.pdf document included in this repository.
