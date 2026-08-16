# 🧠 Smart Digital Addiction Analyzer

An AI-powered digital wellness system that analyzes smartphone usage patterns to evaluate digital addiction risk, Digital Wellness Score, productivity, and behavioral trends.

## 📌 Overview

The **Smart Digital Addiction Analyzer** is a digital wellness platform developed using **C programming and Python Machine Learning**.

The system analyzes smartphone usage behavior and generates meaningful insights instead of simply displaying screen-time statistics.

It provides:

- 📊 Digital Wellness Score
- 🧠 Digital Addiction Risk Prediction
- ⚡ Productivity Analysis
- 📱 Application Classification
- 📈 Behavioral Trend Prediction
- 💡 Personalized Recommendations
- 📊 Interactive Dashboard

---

## 🎯 Problem Statement

Excessive smartphone usage can negatively affect health, sleep, focus, and productivity.

Traditional screen-time applications mainly provide usage statistics without analyzing the user's overall digital behavior.

This project aims to analyze smartphone usage patterns using Machine Learning and provide personalized insights that can help users develop healthier digital habits.

---

## 🚀 Objectives

- Monitor smartphone usage patterns
- Classify applications into different categories
- Predict digital addiction risk
- Calculate Digital Wellness Score
- Analyze productivity
- Analyze user behavior
- Provide personalized recommendations
- Forecast future digital behavior trends
- Display insights through an interactive dashboard

---

## ✨ Key Features

### 1. Digital Addiction Prediction

Machine Learning models analyze user behavior and estimate the user's digital addiction risk.

### 2. Digital Wellness Score

The system calculates a wellness score based on analyzed digital behavior.

### 3. Productivity Analysis

User activity is analyzed to determine productivity levels.

### 4. Application Classification

Applications can be categorized based on their usage and behavioral characteristics.

### 5. Behavioral Trend Prediction

The system predicts whether the user's digital behavior is:

- Improving
- Stable
- Declining
- Critical

### 6. Personalized Recommendations

The system generates recommendations based on the user's digital behavior.

### 7. Interactive Dashboard

A Flask-based dashboard presents the analysis in an easy-to-understand format.

---

## 🏗️ System Architecture

```text
                 Smartphone Usage Data
                          │
                          ▼
                 ┌─────────────────┐
                 │ C Data Collection│
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Data Preprocessing│
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Machine Learning │
                 │    Analysis      │
                 └────────┬────────┘
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
        Addiction     Wellness     Productivity
        Prediction      Score        Analysis
             │            │            │
             └────────────┼────────────┘
                          ▼
                 Behavioral Analysis
                          │
                          ▼
                 Personalized Insights
                          │
                          ▼
                 Flask Web Dashboard
