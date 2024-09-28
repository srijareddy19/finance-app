import pandas as pd
import csv 
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS= ["date","amount", "category", "description"]
    FORMAT = "%m-%d-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry= {  #creating a dictionary 
            "date": date, "amount":amount, "category": category, "description":description
        }

        # open a file using a with-as statement and therefore python will automitically close file for you 
        # here we are appending a new entry into the CSV file using DictWriter 
        with open(cls.CSV_FILE,"a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT )
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date) # use '&' instead of and while using pandas and mask
        filtered_df = df.loc[mask] #locating all the rows in the csv where the previous line is true 

        if filtered_df.empty:
            print('No transactions found in the given date range')
        else:
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}") #{start_date.strftime(CSV.FORMAT)} typecasts the datetime object back into a string in the format of the parameter
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum() #specific formatting and syntax to pandas 
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum() 
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${total_income - total_expense:.2f}") #format to the second decimal point 
        return filtered_df
    
    @classmethod
    def get_all_transactions(cls):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT )
        print(df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))

        total_income = df[df["category"] == "Income"]["amount"].sum() #specific formatting and syntax to pandas 
        total_expense = df[df["category"] == "Expense"]["amount"].sum() 

        print("\nSummary:")
        print(f"Total Income: ${total_income:.2f}")
        print(f"Total Expense: ${total_expense:.2f}")
        print(f"Net Savings: ${total_income - total_expense:.2f}") #format to the second decimal point 

        return df

def plot_transactions(df):
    df.set_index("date", inplace=True)
   

    income_df =  df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0).sort_values(by=["date"])
    expense_df =  df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0).sort_values(by=["date"])

    plt.figure(figsize=(10,5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses over Time")
    plt.legend()
    plt.grid(True)
    plt.show()



def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (mm-dd-yyyy) or just click enter for todays date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)
    
def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. View entire transaction history")
        print("4.Exit")

        choice = input("Enter your choice (1-3): ")
        if choice == "1":
            add()
        elif choice == "2": 
            start_date = get_date("Enter the start date (mm-dd-yyyy)")
            end_date = get_date("Enter end_date (mm-dd-yyyy): ")
            df2 = CSV.get_transactions(start_date, end_date)
            if input("Do you want to see a plot of your transactions (y/n)").lower() == "y":
               plot_transactions(df2) 
        elif choice == "3":
            df3 = CSV.get_all_transactions()
            if input("Do you want to see a plot of your transactions (y/n): ").lower() == "y":
                plot_transactions(df3) 
        elif choice == "4":
            print("Exiting...")
        else:
            print("Invalid choice. Enter 1, 2, or 3.")

if __name__ == "__main__":
    main() 
