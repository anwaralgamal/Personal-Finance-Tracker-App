# Personal Finance Tracker

A personal finance management application built using **Flask** and **SQLAlchemy** to help users track their income, expenses, manage budgets, and visualize their spending habits.

![Dashboard Screenshot](path_to_dashboard_screenshot.png)

## Features

- **User Authentication**: Register, login, and manage your account.
- **Income & Expense Tracking**: Add, categorize, and manage your financial transactions (income and expenses).
- **Budget Management**: Set and manage your monthly budget and track how much is left after expenses.
- **Spending Visualization**: Graphical breakdown of your spending by category.
- **Spending Recommendations**: Receive personalized recommendations based on your spending patterns.
- **Responsive Dashboard**: Get an overview of your financial summary with clean and intuitive UI.
  
## Tech Stack

- **Backend**: Flask
- **Database**: SQLite using SQLAlchemy ORM
- **Frontend**: HTML5, CSS3
- **Visualization**: Matplotlib

## How to Run Locally

### Prerequisites

- Python 3.x
- Flask
- SQLAlchemy
- Matplotlib

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/personal-finance-tracker.git
    ```

2. **Navigate into the directory**:

    ```bash
    cd personal-finance-tracker
    ```

3. **Install dependencies**:

    It's recommended to create a virtual environment first:
    
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

    Then, install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application**:

    ```bash
    python app.py
    ```

5. Open your browser and navigate to `http://localhost:5000`.

## Usage

1. Register or log in to your account.
2. Set your monthly budget and begin adding transactions (income/expenses).
3. View an overview of your financial activity on the dashboard.
4. See personalized spending recommendations based on your habits.
5. Adjust your budget as needed.

## Demo

### Add Transactions:
- Add your expenses or income easily, and categorize them for better tracking.
  
### Spending Breakdown:
- Visualize your spending with an intuitive bar chart broken down by categories like food, entertainment, etc.

### Recommendations:
- Get insights and recommendations like overspending warnings and suggestions to cut costs in certain areas.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

Feel free to reach out for any issues or contributions:

- **Email**: your-email@example.com
- **GitHub**: [Your GitHub Username](https://github.com/yourusername)
