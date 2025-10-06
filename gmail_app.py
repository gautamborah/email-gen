# src/main.py

from src.gmail_helper.gmail_service import login_and_get_reader

def main():
    # Login and get GmailReader instance
    reader = login_and_get_reader()

    # Get first email
    email1 = reader.get_next_email()
    print("--- Email 1 ---")
    print(email1)

    # Get next email
    email2 = reader.get_next_email()
    print("\n--- Email 2 ---")
    print(email2)

    # Refresh emails if needed
    reader.refresh()

if __name__ == "__main__":
    main()
