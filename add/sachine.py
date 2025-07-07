import sqlite3
import pandas as pd

# Connect to in-memory SQLite database
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Create department table
cursor.execute("""
CREATE TABLE dept (
    dept_id INTEGER PRIMARY KEY,
    dept_name TEXT
)
""")

# Create employee table
cursor.execute("""
CREATE TABLE emp (
    emp_id INTEGER PRIMARY KEY,
    emp_name TEXT,
    salary INTEGER,
    dept_id INTEGER,
    FOREIGN KEY (dept_id) REFERENCES dept(dept_id)
)
""")

# Insert sample data into dept
cursor.executemany("""
INSERT INTO dept (dept_id, dept_name) VALUES (?, ?)
""", [
    (1, 'HR'),
    (2, 'Engineering'),
    (3, 'Marketing')
])

# Insert sample data into emp
cursor.executemany("""
INSERT INTO emp (emp_id, emp_name, salary, dept_id) VALUES (?, ?, ?, ?)
""", [
    (101, 'Alice', 60000, 1),
    (102, 'Bob', 75000, 2),
    (103, 'Charlie', 50000, 3),
    (104, 'David', 85000, 2),
    (105, 'Eve', 75000, None)  # Employee with no department
])

# LEFT JOIN emp with dept
query = """
SELECT e.emp_id, e.emp_name, e.salary, d.dept_name
FROM emp e
LEFT JOIN dept d ON e.dept_id = d.dept_id
"""
df = pd.read_sql_query(query, conn)
print("👥 All Employees with Departments (LEFT JOIN):")
print(df)

# Get second highest salary employee(s)
second_salary_query = """
SELECT emp_id, emp_name, salary
FROM emp
WHERE salary = (
    SELECT DISTINCT salary
    FROM emp
    ORDER BY salary DESC
    LIMIT 1 OFFSET 1
)
"""
second_highest_df = pd.read_sql_query(second_salary_query, conn)
print("\n🥈 Second Highest Salary Employee(s):")
print(second_highest_df)

# Close connection
conn.close()
