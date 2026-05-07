Smart Budget Tool

1. Introduction

1.1 Purpose and Objectives of the Application
The “Smart Budget” application helps users manage their money in a simple and organized way. The main objectives are:
- Track income, expenses, and savings
- Help users understand their financial habits
- Provide financial summaries and charts
- Demonstrate Object-Oriented Programming concepts using Python and Streamlit

1.2 Brief Overview of the Project
The project is a web-based budgeting tool created using Python and Streamlit. Users can log in with their name and manage their finances through different sections such as Dashboard, Income, Expense, Savings, and Summary.

The application allows users to:
- Add income and expenses
- Track savings
- Create savings boxes for goals
- View charts and summaries
- Monitor balance and spending habits



2. Problem Definition and Requirements
3. 
2.1 Problem the Application Solves
Many people struggle to manage their money and track spending. This application helps users organize their finances in one place and gives a clear overview of their income, expenses, and savings.
The savings boxes feature also helps users save money for specific goals such as travel, shopping, or emergencies.

2.2 Functional and Non-Functional Requirements

Functional Requirements
- Users can add income, expenses, and savings
- Users can create savings boxes
- The system calculates totals and balance
- The application displays charts and summaries
- Users can view recent activity

Non-Functional Requirements
- The interface should be simple and user-friendly
- The system should run smoothly
- The code should be easy to maintain
- The application should handle invalid inputs properly



3. Design and Implementation

3.1 Object-Oriented Design Principles Used
Encapsulation
Financial data is stored inside the User class and managed using methods such as add_income() and add_expense().
Abstraction
Complex calculations are simplified through methods like balance() and savings_rate().
Polymorphism
Income, expenses, and savings are handled in a similar way using shared structures and methods.

3.2 Class Structure

+------------------+
| User             |
+------------------+
| - incomes        |
| - expenses       |
| - savings        |
| - savings_boxes  |
+------------------+
| + add_income()   |
| + add_expense()  |
| + add_savings()  |
| + balance()      |
+------------------+


User
The main class of the application. It stores all financial data and performs calculations for balance, savings, and summaries.

3.3 Key Algorithms and Data Structures
Data Structures Used

- Lists store income, expense, and savings entries
- Dictionaries store transaction details such as amount, note, and date
- Pandas DataFrames display tables

Algorithms Used
Balance Calculation
balance = total_income - total_expenses
Savings Rate Calculation
savings_rate = (total_savings / total_income) * 100
The system also filters monthly data and generates charts using Matplotlib.



4. Development Process

4.1 Tools and Environment
- Programming Language: Python
- Framework: Streamlit
- Libraries: Pandas, Matplotlib
- IDE: VS Code
- Version Control: GitHub

4.2 Development Steps
1. Planned the application structure and features
2. Created the User class and financial methods
3. Designed the Streamlit interface
4. Added charts and summaries
5. Tested the application and fixed bugs
6. Improved the design using custom CSS styling



5. Results and Demonstration

5.1 Application Features
- Dashboard with financial overview
- Income and expense tracking
- Savings management
- Savings boxes for goals
- Charts and summaries
- Recent activity section
- Modern responsive interface



6. Testing and Validation

6.1 Testing Procedures
- Tested income and expense calculations
- Tested savings box functionality
- Checked charts and summaries
- Tested invalid inputs such as negative values

6.2 Issues Resolved
Issue 1
Balance was incorrect when invalid numbers were entered.
Solution: Added input validation.
Issue 2
Charts were not updating properly after adding data.
Solution: Used st.rerun() to refresh the application.


7. Conclusion and Future Work

7.1 Summary of Achievements
The Smart Budget application successfully helps users manage income, expenses, and savings in a simple way. The project demonstrates Object-Oriented Programming concepts and practical Python development using Streamlit.

7.2 Future Improvements
- Add user authentication
- Add cloud database storage
- Create mobile support
- Add AI-based spending recommendations
- Improve charts and analytics
