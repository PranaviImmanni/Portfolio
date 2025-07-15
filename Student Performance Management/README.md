# 📊 Student Performance Management

## 📑 Table of Contents
- [Abstract](#abstract)  
- [Project Motivation & Dataset Description](#project-motivation--dataset-description)  
- [Research Questions](#research-questions)  
- [Object-Oriented Programming Approach](#object-oriented-programming-approach)  
- [UML Design](#uml-design)  
- [Data Visualization and Key Analysis](#data-visualization-and-key-analysis)  
- [Statistical Significance Testing](#statistical-significance-testing)  
- [Conclusion](#conclusion)  
- [References](#references)  

---

## 🧠 Abstract  
The purpose of this project is to analyze student academic performance using real-world data and identify patterns that may help educators better understand student needs. The dataset used for this project is called **“StudentsPerformance.csv”**, created by Rashida Nasrin, and hosted on GitHub. It includes test scores for 1,000 students, along with demographic attributes such as gender, parental education level, lunch type, race/ethnicity, and participation in test preparation courses. I built a reusable data analysis system in Python using Google Colab, leveraging libraries like pandas, seaborn, and matplotlib to generate visualizations and insights.

---

## 🎯 Project Motivation & Dataset Description  
I chose this project because educators often lack intuitive tools to assess when a student may need additional support. These gaps can prevent students from reaching their full potential. As a student myself, I wanted to explore how data science could offer insights to help teachers better identify at-risk students or understand patterns behind success. By analyzing this dataset, I aimed to understand the effect of various factors on student outcomes and use visualizations to support decision-making in academic environments.

---

## ❓ Research Questions  

- Does gender influence academic performance across core subjects?  
- How does parental education relate to student achievements?  
- Do different racial/ethnic groups perform differently?  
- What common traits do the top 10 students share?  
- Does completing test prep significantly improve scores?  
- Is there a strong correlation between math, reading, and writing scores?

---

## 🔧 Object-Oriented Programming Approach  

I designed a `Student` class to store individual student attributes and calculate average scores. This object-oriented design made the code more reusable, organized, and scalable. Each object held values for gender, parental education, test prep, and scores, among others. The project also allowed me to apply functional and object-oriented concepts while gaining practical experience with data cleaning, visualization, and statistical analysis. Google Colab was used as the development environment.

### My workflow:
- Renaming and formatting column names  
- Computing summary statistics  
- Creating new features like `average_score`  
- Building visualizations  
- Applying hypothesis testing  

---

## 📐 UML Design  
A UML diagram was created to represent the design of the `Student` class used in the project. It outlines the class structure, key attributes, and methods for calculating average scores.

---

## 📊 Data Visualization and Key Analysis  

After cleaning and verifying the dataset, I created a new column, `average_score`, to calculate each student's mean score across math, reading, and writing.

### Key insights:
- **Gender:** Female students scored higher in reading and writing; male students performed slightly better in math.  
- **Test Prep:** Students who completed prep courses achieved higher scores across all subjects.  
- **Parental Education:** Students with parents holding bachelor’s or master’s degrees scored higher.  
- **Lunch Type:** Free/reduced-price lunch students had lower scores, indicating a socioeconomic impact.  
- **Correlation:** Strong interrelation was found between math, reading, and writing scores.

---

## 🧪 Statistical Significance Testing  

I used:
- **T-tests** to compare gender-based performance  
- **ANOVA** for performance differences across racial/ethnic groups  
- **Visualizations** like boxplots and heatmaps  

Low p-values confirmed significant differences, validating trends observed in the data.

---

## ✅ Conclusion  

This student performance analytics system helped analyze and visualize educational data, highlighting factors that influence academic success. These insights can guide targeted interventions and improve student support. The project could be expanded using predictive modeling or dashboards. This experience strengthened my skills in data science, visualization, and analytical problem solving.

---

## 🔗 References  
- Dataset: [StudentsPerformance.csv by Rashida Nasrin](https://github.com/rashida048/Datasets/blob/master/StudentsPerformance.csv)  
- Notebook Reference: [Student Performance Analytics](https://github.com/sharmaroshan/Students-Performance-Analytics/blob/master/Student_Performance.ipynb)

