# Inventory Policy Simulation & Analysis

An interactive **Inventory Policy Simulation and Analysis** application built with **Python and Streamlit** to evaluate and compare different inventory replenishment policies under deterministic and stochastic demand.

> **Project Note:** This project is an **extension of the inventory simulation work developed by [@Samir Saci](https://github.com/samirsaci)**, with additional inventory policies, EOQ-based ordering, stochastic demand, safety stock, reorder-point logic, and multi-policy comparison developed on top of the original concept.

---

## Overview

Inventory management requires balancing product availability, replenishment timing, inventory levels, and inventory-related costs.

This project provides an interactive simulation environment where users can enter inventory parameters and evaluate different replenishment policies over a selected planning horizon.

The application is designed to make inventory policy analysis accessible to both technical and non-technical users through a simple Streamlit interface.

The application simulates six different inventory scenarios and compares their:

- Demand
- Replenishment orders
- Inventory levels
- Stockout days
- Minimum inventory
- Average inventory

---

## Application

The Streamlit application allows users to enter business-level inventory parameters through a sidebar and run all six inventory simulations.

The application provides:

- Three-panel visual analysis
- Inventory policy comparison
- Stockout analysis
- KPI comparison
- EOQ calculation
- Safety stock calculation
- Reorder point calculation

The three main visualizations are:

1. **Demand**
2. **Orders**
3. **Inventory Level**

---

## Application Access

### Local Application

When running the application locally:

```text
http://localhost:8501
