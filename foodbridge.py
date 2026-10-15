
# FoodBridge: Zero Hunger Project
# IBM Project Submission - Python Prototype
# SDG 2: Zero Hunger

donations = []
recipients = []
next_donation_id = 1


def add_donation():
    global next_donation_id

    print("\n--- Register Food Donation ---")
    provider = input("Restaurant/Provider name: ").strip()
    food = input("Food name/type: ").strip()
    try:
        quantity = int(input("Number of meal portions: "))
    except ValueError:
        print("Please enter a valid quantity.")
        return

    location = input("Location: ").strip()
    expiry = input("Safe-to-consume deadline (e.g., 6 PM today): ").strip()

    if not provider or not food or not location or quantity <= 0:
        print("Invalid details. Please try again.")
        return

    donation = {
        "id": next_donation_id,
        "provider": provider,
        "food": food,
        "quantity": quantity,
        "location": location.lower(),
        "expiry": expiry,
        "status": "Available"
    }

    donations.append(donation)
    print("Donation registered successfully!")
    print("Donation ID:", next_donation_id)
    next_donation_id += 1


def register_recipient():
    print("\n--- Register NGO / Community Kitchen ---")
    name = input("NGO/community kitchen name: ").strip()
    location = input("Location: ").strip()

    try:
        capacity = int(input("Number of people you can serve: "))
    except ValueError:
        print("Please enter a valid capacity.")
        return

    if not name or not location or capacity <= 0:
        print("Invalid details. Please try again.")
        return

    recipients.append({
        "name": name,
        "location": location.lower(),
        "capacity": capacity
    })

    print("Recipient registered successfully!")


def view_donations():
    print("\n--- Available Food Donations ---")

    available = [d for d in donations
                 if d["status"] == "Available"]

    if not available:
        print("No available donations.")
        return

    for d in available:
        print(f"\nDonation ID: {d['id']}")
        print("Provider:", d["provider"])
        print("Food:", d["food"])
        print("Portions:", d["quantity"])
        print("Location:", d["location"].title())
        print("Safe-to-consume deadline:", d["expiry"])
        print("Status:", d["status"])


def find_matches():
    print("\n--- Find Suitable Food Recipients ---")

    try:
        donation_id = int(input("Enter donation ID: "))
    except ValueError:
        print("Enter a valid donation ID.")
        return

    donation = next(
        (d for d in donations
         if d["id"] == donation_id
         and d["status"] == "Available"),
        None
    )

    if donation is None:
        print("Donation not found or already handed over.")
        return

    matches = [
        r for r in recipients
        if r["location"] == donation["location"]
        and r["capacity"] > 0
    ]

    if not matches:
        print("No registered recipient found in this location.")
        print("Please contact a verified local NGO.")
        return

    print("\nSuitable recipients:")
    for i, recipient in enumerate(matches, start=1):
        portions = min(
            donation["quantity"], recipient["capacity"]
        )
        print(f"{i}. {recipient['name']}")
        print("   Location:", recipient["location"].title())
        print("   Possible portions:", portions)


def complete_handover():
    print("\n--- Confirm Food Handover ---")

    try:
        donation_id = int(input("Enter donation ID: "))
    except ValueError:
        print("Enter a valid donation ID.")
        return

    donation = next(
        (d for d in donations
         if d["id"] == donation_id
         and d["status"] == "Available"),
        None
    )

    if donation is None:
        print("Available donation not found.")
        return

    matching_recipients = [
        r for r in recipients
        if r["location"] == donation["location"]
        and r["capacity"] > 0
    ]

    if not matching_recipients:
        print("No suitable recipient registered in this location.")
        return

    print("\nSelect recipient:")
    for i, r in enumerate(matching_recipients, start=1):
        print(f"{i}. {r['name']} (Capacity: {r['capacity']})")

    try:
        choice = int(input("Enter recipient number: "))
    except ValueError:
        print("Invalid choice.")
        return

    if choice < 1 or choice > len(matching_recipients):
        print("Invalid recipient number.")
        return

    recipient = matching_recipients[choice - 1]
    portions = min(donation["quantity"], recipient["capacity"])

    print("\nBefore confirming, verify that the food")
    print("is safe, properly stored, and suitable for donation.")
    print("Portions to hand over:", portions)

    confirm = input("Has the safe handover been completed? (yes/no): ")
    if confirm.strip().lower() != "yes":
        print("Handover not recorded.")
        return

    donation["quantity"] -= portions
    recipient["capacity"] -= portions

    if donation["quantity"] == 0:
        donation["status"] = "Completed"

    print("Handover recorded successfully!")
    print("Recipient:", recipient["name"])
    print("Meal portions redistributed:", portions)


def impact_dashboard():
    print("\n--- FoodBridge Impact Dashboard ---")

    total_registered = sum(d["quantity"] for d in donations)
    available = sum(
        d["quantity"] for d in donations
        if d["status"] == "Available"
    )
    redistributed = total_registered - available

    print("Total meal portions registered:", total_registered)
    print("Meal portions redistributed:", redistributed)
    print("Meal portions still available:", available)
    print("Registered donations:", len(donations))
    print("Registered NGOs/community kitchens:", len(recipients))

    print("\nSDG 2 Goal: Help improve access to food.")
    print("Note: These are prototype records, not verified")
    print("real-world hunger or food-waste measurements.")


def load_demo_data():
    global next_donation_id

    if donations or recipients:
        print("Load demo data only in a fresh session.")
        return

    donations.append({
        "id": next_donation_id,
        "provider": "Green Leaf Restaurant",
        "food": "Vegetable meals",
        "quantity": 30,
        "location": "kakinada",
        "expiry": "6 PM today",
        "status": "Available"
    })
    next_donation_id += 1

    recipients.append({
        "name": "Helping Hands NGO",
        "location": "kakinada",
        "capacity": 50
    })

    print("Sample data loaded successfully!")
    print("Demo donation ID: 1")
    print("You can now find matches and confirm a handover.")


def main():
    while True:
        print("\n" + "=" * 42)
        print(" FOODBRIDGE - ZERO HUNGER PROJECT")
        print("=" * 42)
        print("1. Register food donation")
        print("2. Register NGO/community kitchen")
        print("3. View available donations")
        print("4. Find suitable recipients")
        print("5. Confirm food handover")
        print("6. View impact dashboard")
        print("7. Load sample demonstration data")
        print("8. Exit")

        choice = input("Choose an option (1-8): ").strip()

        if choice == "1":
            add_donation()
        elif choice == "2":
            register_recipient()
        elif choice == "3":
            view_donations()
        elif choice == "4":
            find_matches()
        elif choice == "5":
            complete_handover()
        elif choice == "6":
            impact_dashboard()
        elif choice == "7":
            load_demo_data()
        elif choice == "8":
            print("Thank you for supporting Zero Hunger!")
            break
        else:
            print("Invalid choice. Please select 1-8.")


if __name__ == "__main__":
    main()
