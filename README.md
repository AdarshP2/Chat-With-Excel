# Excel Analysis Chat & Forecasting System

Welcome to the **Excel Analysis Chat & Forecasting System** – a dynamic, interactive Streamlit application that empowers you to seamlessly upload Excel/CSV data, perform natural language queries on your data, and generate AI-based forecasts.

---

## Features

- **Data Upload:**  
  Easily upload Excel or CSV files and automatically convert them into a SQLite database for analysis.

- **Chat Interface:**  
  Interact with your data through a conversational UI powered by SQLDatabaseChain and HuggingFace's Falcon 7B Instruct model.

- **AI Forecasting:**  
  Generate accurate forecasts using AutoARIMA (via pmdarima) and evaluate performance with Mean Absolute Percentage Error (MAPE).

- **User-Friendly Experience:**  
  Navigate effortlessly between data upload and chat interfaces with an intuitive Streamlit-based UI.

---

## Tech Stack

- **Frontend:** Streamlit  
- **Backend:** Python, Pandas, SQLAlchemy, SQLite  
- **AI/ML Libraries:** pmdarima, LangChain, HuggingFaceHub  
- **Environment Management:** dotenv

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your_username/excel-analysis-chat.git
   cd excel-analysis-chat
