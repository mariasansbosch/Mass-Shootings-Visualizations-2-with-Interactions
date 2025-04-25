# 📈 US Gun Violence Evolution – Interactive Dashboard with Altair & Streamlit

## 🧠 Project Overview

This project explores the **evolution of mass shootings in the United States** over time using data from the [Gun Violence Archive](https://www.gunviolencearchive.org/reports). Built with **Altair** and **Streamlit**, the dashboard presents a set of **interactive, linked visualizations** that allow users to compare trends across years, regions, states, and counties.

The core goal of this project is to deliver deeper insights by enabling user-driven exploration of how gun violence patterns have changed across US regions.

## 🔍 Key Questions Answered

1. **How has the number of mass shootings evolved across the 5 major US regions and individual states between any two selected years?**
2. **Given a year, how does the number of mass shootings per citizen in each region compare to the baseline year?**
3. **For a selected state, how has gun violence evolved across its counties?**

These questions are addressed through coordinated and interactive views that let users filter by region, state, year range, and drill down into county-level data.

## 🧹 Data Cleaning & Preparation

Annual mass shooting data was collected from the Gun Violence Archive and cleaned using OpenRefine and custom Python scripts. The data was:
- Aggregated by region, state, and county
- Normalized per capita using census data
- Augmented with geographic references for mapping

All transformation steps are documented for full reproducibility.

## 📊 Visualizations

Each question is supported by tailored charts and interactivity designed to improve usability and insight. Key visualization features include:
- **Multi-year comparison line charts**
- **Choropleth maps for per-capita comparisons**
- **Linked views for regional, state, and county selection**
- **Dropdown filters and sliders** to control year ranges and granularity

Each visualization includes a short written explanation (≤200 words) describing the design decisions, visual encoding choices, interaction mechanisms, and alternatives considered.

## 🧩 Final Visualization & Google Colab

A **final integrated dashboard** was created in **Google Colab** to demonstrate all visualizations in one coherent view. Charts were adjusted to:
- Ensure stylistic consistency (colors, fonts, axes)
- Enhance visual balance and responsiveness
- Improve comparative legibility

The final product was deployed as a **Streamlit app**, enabling intuitive user exploration.
