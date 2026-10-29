# 🚗 NGSIM Vehicle Trajectory Scenario Extraction

## 📌 Project Overview
This project processes vehicle trajectory data from the **NGSIM (US-101)** dataset to automatically detect and classify common highway driving scenarios: **Lane Changes**, **Car-Following**, and **Cut-Ins**. 

The project was developed in two distinct phases for the *SOFE 4630U: Cloud Computing* course, demonstrating the evolution from a monolithic application to a cloud-native microservices architecture.

**Group 12 Members:**
* Anuj Shukla
* Ishmeet Kaur
* Brandon Ho
* Gabriele Martorano

> **Note on Codebase:** The source code currently available in this repository implements the **Phase 1 (Monolithic)** architecture. The **Phase 2 (Microservices)** design is fully detailed in the accompanying documentation to illustrate how the system scales in a cloud environment.

## 📊 Dataset
The project utilizes the NGSIM US-101 vehicle trajectory dataset (`trajectories-0820am-0835am.csv`). 
* **Important:** Due to its large size, the raw dataset is not tracked in the main branch. Please download it directly from the **[GitHub Releases]** page and place it in the appropriate `data/` directory before running the code.

## 🚗 Scenario Detection Logic
Regardless of the architecture, the system analyzes 5-second windows of traffic data to identify interactions:
* **Lane Change:** Detected when a vehicle's `Lane_ID` changes within the time window.
* **Car-Following:** Detected when two vehicles share the same lane, remain within 30 meters of each other, and maintain a velocity difference of less than $5 m/s$.
* **Cut-In:** Detected when a vehicle starts in a different lane, ends in the ego vehicle's lane, and positions itself less than 30 meters directly ahead of the ego vehicle.

---

## 🏗️ Phase 1: Monolithic Implementation
In Phase 1, the system is designed as a modular but monolithic data pipeline executed on a single Virtual Machine. 

### Workflow
1. **Data Ingestion:** Loads the CSV dataset into memory using Pandas.
2. **Preprocessing:** Cleans data and sorts vehicle observations by frame order.
3. **Window Segmentation:** Slices the data into overlapping sliding windows of 50 rows (representing approximately 5 seconds of traffic at 10 FPS).
4. **Scenario Detection:** Applies the detection logic to each window.
5. **Output:** Generates a summary CSV file with labeled scenarios and dynamic GIF visualizations tracking the ego vehicle.

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
3. Run the main script:
   ```bash
   python3 main.py
   ```
4. The output CSV (`scenario_output.csv`) and generated GIFs (`Car_Following.gif`, `Lane_Change.gif`, `Cut-In.gif`) will be saved in the working directory.

## ☁️ Phase 2: Microservices Architecture (Design & Evolution)

To overcome the limitations of the monolithic approach (such as memory constraints and row-based segmentation), Phase 2 re-architects the system into a distributed, event-driven pipeline on Google Cloud Platform (GCP).

### Cloud Components

* **Cloud Storage (Input):** Hosts the raw NGSIM dataset, decoupling storage from compute.
* **Data Ingestion Service:** Reads the data from Cloud Storage and streams it row-by-row into a Pub/Sub topic.
* **Google Cloud Pub/Sub:** Acts as an asynchronous message queue, buffering data to ensure fault tolerance.
* **Google Cloud Dataflow (Apache Beam):** Replaces the single-thread Pandas logic. It dynamically scales worker nodes to process the stream in parallel. Crucially, it replaces the rigid 50-row chunking with native time-based windowing (`beam.window.FixedWindows(5)`) using the `Global_Time` timestamp, seamlessly handling any dropped frames.
* **Cloud Storage (Output):** Stores the detected scenarios as highly structured JSON files for downstream analytics.

*(For a detailed breakdown of the Phase 2 implementation, deployment steps, and architectural comparisons, please refer to the `Phase 2.pdf` document included in this repository).*

