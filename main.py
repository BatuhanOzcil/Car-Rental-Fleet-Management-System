# =BATUHAN ÖZÇİL ID:125200023
#  CMPE261 Car Rental Fleet Management System


#custom exceptions
class VehicleUnavailableError(Exception):
    pass


class InvalidDurationError(Exception):
    pass


class VehicleNotFoundError(Exception):
    pass


class FileError(Exception):
    pass


#Vehicle class
class Vehicle:
    def __init__(self, plate_id, make_model, category, daily_rate, is_available=True):
        self.plate_id = plate_id
        self.make_model = make_model
        self.category = category
        self.daily_rate = float(daily_rate)
        self.is_available = bool(is_available)

    def display_info(self):
        status = "[Available]" if self.is_available else "[UNAVAILABLE]"
        return f"{status} {self.make_model} - Plate: {self.plate_id} - {self.daily_rate:.2f}$/day"

    def set_rented(self):
        self.is_available = False

    def set_available(self):
        self.is_available = True


# rental class
class Rental:
    def __init__(self, rental_id, customer_name, vehicle_plate, days_rented, daily_rate):
        if days_rented <= 0:
            raise InvalidDurationError("Rental duration must be > 0")

        self.rental_id = rental_id
        self.customer_name = customer_name
        self.vehicle_plate = vehicle_plate
        self.days_rented = days_rented
        self.total_cost = daily_rate * days_rented

    def generate_receipt(self):
        return (
            f"--- Rental Receipt ---\n"
            f"Rental ID: {self.rental_id}\n"
            f"Customer: {self.customer_name}\n"
            f"Vehicle: {self.vehicle_plate}\n"
            f"Days: {self.days_rented}\n"
            f"Total Cost: ${self.total_cost:.2f}\n"
        )


# fleetmanager class
class FleetManager:
    def __init__(self):
        self.fleet = []
        self.rentals = []
        self.next_rental_id = 1

    def add_vehicle(self, vehicle):
        self.fleet.append(vehicle)

    def _find_vehicle(self, plate):
        for v in self.fleet:
            if v.plate_id == plate:
                return v
        raise VehicleNotFoundError(f"Vehicle {plate} not found")

    def rent_vehicle(self, plate, customer, days):
        if days <= 0:
            raise InvalidDurationError("Rental duration must be greater than 0")

        vehicle = self._find_vehicle(plate)

        if not vehicle.is_available:
            raise VehicleUnavailableError(f"Vehicle {plate} is currently UNAVAILABLE")

        vehicle.set_rented()

        rental = Rental(
            rental_id=self.next_rental_id,
            customer_name=customer,
            vehicle_plate=plate,
            days_rented=days,
            daily_rate=vehicle.daily_rate
        )

        self.rentals.append(rental)
        self.next_rental_id += 1
        return rental

    def return_vehicle(self, plate):
        vehicle = self._find_vehicle(plate)
        vehicle.set_available()

    def generate_revenue_report(self):
        total = sum(r.total_cost for r in self.rentals)
        category_revenue = {}

        for r in self.rentals:
            v = self._find_vehicle(r.vehicle_plate)
            category_revenue[v.category] = category_revenue.get(v.category, 0) + r.total_cost

        most_popular = max(category_revenue, key=category_revenue.get) if category_revenue else "N/A"
        return total, most_popular

    # data analysis helperı
    def get_most_rented_category(self):
        return self.generate_revenue_report()[1]

    def list_available_vehicles(self):
        return [v for v in self.fleet if v.is_available]

    # file persistence
    def save_state(self, filename):
        try:
            with open(filename, "w", encoding="utf-8") as f:
                # vehicle
                for v in self.fleet:
                    f.write(
                        f"VEHICLE,{v.plate_id},{v.make_model},"
                        f"{v.category},{v.daily_rate},{v.is_available}\n"
                    )
                # rental
                for r in self.rentals:
                    f.write(
                        f"RENTAL,{r.rental_id},{r.customer_name},"
                        f"{r.vehicle_plate},{r.days_rented},{r.total_cost}\n"
                    )
        except Exception as e:
            raise FileError(f"Error saving file: {e}")

    def load_state(self, filename):
        try:
            self.fleet.clear()
            self.rentals.clear()

            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if not parts:
                        continue

                    tag = parts[0]

                    if tag == "VEHICLE":
                        _, plate, model, cat, rate, avail = parts
                        self.fleet.append(
                            Vehicle(
                                plate,
                                model,
                                cat,
                                float(rate),
                                avail == "True"
                            )
                        )
                    elif tag == "RENTAL":
                        _, rid, name, plate, days, cost = parts
                        days_i = int(days)
                        cost_f = float(cost)
                        daily_rate = cost_f / days_i if days_i > 0 else cost_f
                        r = Rental(int(rid), name, plate, days_i, daily_rate)
                        r.total_cost = cost_f  # yeniden hesaplama
                        self.rentals.append(r)

            if self.rentals:
                self.next_rental_id = max(r.rental_id for r in self.rentals) + 1
            else:
                self.next_rental_id = 1

        except FileNotFoundError:
            raise FileError("File not found")
        except Exception as e:
            raise FileError(f"Error loading file: {e}")


# console
def main():
    manager = FleetManager()
    DATA_FILE = "fleet_data.txt"

    # eski state için try
    try:
        manager.load_state(DATA_FILE)
        print(">> Previous data loaded.")
    except FileError:
        print(">> No previous data loaded (file missing or invalid).")

    while True:
        print("\n=== CityDrive Fleet Management System ===")
        print("1. Add Vehicle")
        print("2. Rent Vehicle")
        print("3. Return Vehicle")
        print("4. Generate Reports")
        print("5. Save & Exit")

        choice = input("Select: ").strip()

        if choice == "1":
            print("\nEnter Vehicle Details:")
            plate = input("Plate: ").strip()
            model = input("Model: ").strip()
            category = input("Category: ").strip()
            try:
                rate = float(input("Daily Rate: ").strip())
            except ValueError:
                print(">> Invalid rate.")
                continue

            v = Vehicle(plate, model, category, rate)
            manager.add_vehicle(v)
            print(f">> Vehicle {plate} added to fleet.")

        elif choice == "2":
            plate = input("\nEnter Plate to Rent: ").strip()
            customer = input("Customer Name: ").strip()

            try:
                days = int(input("Days: ").strip())
                rental = manager.rent_vehicle(plate, customer, days)
                print(f">> Rental Successful! Total Cost: ${rental.total_cost:.2f}")
                print(">> Receipt generated.")
                # receipt detayı için alttaki
                # print(rental.generate_receipt())
            except ValueError:
                print(">> Invalid number for days.")
            except VehicleUnavailableError as e:
                print(f">> Error: {e}")
            except VehicleNotFoundError as e:
                print(f">> Error: {e}")
            except InvalidDurationError as e:
                print(f">> Error: {e}")

        elif choice == "3":
            plate = input("\nEnter Plate to Return: ").strip()
            try:
                manager.return_vehicle(plate)
                print(">> Vehicle returned. Status updated to Available.")
            except VehicleNotFoundError as e:
                print(f">> Error: {e}")

        elif choice == "4":
            total, popular = manager.generate_revenue_report()
            print("\n--- Revenue Report ---")
            print(f"Total Revenue: ${total:.2f}")
            print(f"Most Popular Category: {popular}")

        elif choice == "5":
            try:
                manager.save_state(DATA_FILE)
                print(">> State saved. Exiting...")
            except FileError as e:
                print(f">> Error while saving: {e}")
            break

        else:
            print(">> Invalid selection.")


if __name__ == "__main__":
    main()
