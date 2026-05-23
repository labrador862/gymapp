# gymapp

A data-driven fitness tracking platform with a focus on analytics (e.g., performance over time, fatigue tracking) aiming to assist intermediate lifters and beyond by helping them become more aware of their habits and long term performance trends.

## Overview

Most fitness tracking applications focus primarily on workout logging. gymapp is designed to go further by structuring workout data in a way that enables deeper analysis of training patterns, recovery, fatigue, and performance progression.

The long term goal of the project is to combine structured workout analytics with predictive modeling to provide users with personalized training insights and recovery recommendations.

---

## Core Goals

* Provide fast and intuitive workout tracking
* Store highly structured longitudinal training data
* Analyze user performance and recovery trends
* Estimate exercise and session fatigue to guide recommendations
* Build a scalable analytics-oriented backend architecture to support future predictive and recommendation systems

---

## Current Features

### Workout Tracking

* Create and manage workout sessions
* Log exercises, sets, reps, and weight
* Track exercise ordering within sessions
* Store timestamps for session analysis

### Exercise Database

* Canonical exercise naming system
* Exercise alias support to address inconsistent exercise names (e.g., bench press vs. barbell bench press)
* Weighted muscle activation mapping per exercise

### Analytics-Oriented Design

* Longitudinal performance tracking
* Session structure analysis
* Volume by muscle group
* Fatigue-oriented data modeling

---

## Planned Features

### Analytics

* Weekly volume analysis
* Fatigue trend visualization
* Recovery estimation
* Performance progression tracking

### Predictive Systems

* Personalized fatigue estimation
* Adaptive training recommendations
* Overtraining detection
* Recovery capacity modeling
* User-specific training response inference

---

## Database Design Philosophy

The database schema was intentionally designed around analytical flexibility and future scalability.

Examples include:

* canonical exercise normalization
* weighted muscle activation mapping
* ordered exercise/set tracking
* longitudinal performance storage

Additional design notes and schema documentation can be found in the `/docs` directory.

---

## Tech Stack

Current / Planned Technologies:

* Python
* Relational SQL database
* Git
* Data analytics tooling
* Future ML integration

---

## Motivation

As an intermediate bodybuilder myself, it has become increasingly more difficult for me to mentally manage all of the nuance that goes into my training. I wanted to create something easy to use with plenty of visualizations to do most of the thinking for me and help me better understand where I am making mistakes in my training in both the short and long term. Coincidentally this project has allowed me to explore how structured training data can be used to generate meaningful insights without knowing a user's exact situation.

A broader goal of mine is to investigate how analytics and machine learning systems could help users better understand their recovery, fatigue, and training performance over time.

---

## Future Direction

Potential future areas of exploration:

* recommendation systems
* predictive modeling
* personalized training analytics
* fatigue inference pipelines