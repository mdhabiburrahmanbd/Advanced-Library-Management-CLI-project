
import json
from datetime import datetime, timedelta
import save_all_books

def lend_book(all_books):
    try:
        with open("lend_books.json", "r") as fp:
            lend_books = json.load(fp)
    except FileNotFoundError:
        lend_books = []

    title = input("Enter the Book Title to Lend: ")
    for book in all_books:
        if book["title"] == title:
            if book["quantity"] > 0:
                borrower_name = input("Enter Borrower's Name: ")
                phone_number = input("Enter Borrower's Phone Number: ")
                return_date = datetime.now() + timedelta(days=14)  # 2 weeks loan period
                return_date_str = return_date.strftime("%d-%m-%Y %H:%M:%S")

                lend_info = {
                    "title": title,
                    "borrower_name": borrower_name,
                    "phone_number": phone_number,
                    "return_date": return_date_str
                }

                lend_books.append(lend_info)

                book["quantity"] -= 1
                save_all_books.save_all_books(all_books)

                with open("lend_books.json", "w") as fp:
                    json.dump(lend_books, fp, indent=4)

                print(f"Book '{title}' lent successfully to {borrower_name}.")
                return
            else:
                print("There are not enough books available to lend.")
                return

    print("Book not found.")

def return_book(all_books):
    try:
        with open("lend_books.json", "r") as fp:
            lend_books = json.load(fp)
    except FileNotFoundError:
        print("No books are currently lent out.")
        return

    title = input("Enter the Book Title to Return: ")
    borrower_name = input("Enter Borrower's Name: ")

    for lend in lend_books:
        if lend["title"] == title and lend["borrower_name"] == borrower_name:
            lend_books.remove(lend)

            for book in all_books:
                if book["title"] == title:
                    book["quantity"] += 1
                    save_all_books.save_all_books(all_books)
                    break

            with open("lend_books.json", "w") as fp:
                json.dump(lend_books, fp, indent=4)

            print(f"Book '{title}' returned successfully by {borrower_name}.")
            return

    print("Lend record not found.")
