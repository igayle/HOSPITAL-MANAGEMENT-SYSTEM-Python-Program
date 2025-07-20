# HOSPITAL MANAGEMENT SYSTEM

import datetime

# Person class (Base)
class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

# Patient class (inherits from Person)
class Patient(Person):
    def __init__(self, name, age, gender, patient_id):
        super().__init__(name, age, gender)
        self.patient_id = patient_id
        self.appointments = []

    def view_profile(self):
        print(f"Patient ID: {self.patient_id}, Name: {self.name}, Age: {self.age}, Gender: {self.gender}")

# Doctor class (inherits from Person)
class Doctor(Person):
    def __init__(self, name, age, gender, doctor_id, specialty, schedule):
        super().__init__(name, age, gender)
        self.doctor_id = doctor_id
        self.specialty = specialty
        self.schedule = schedule

    def is_available(self, time):
        return time in self.schedule

    def view_schedule(self):
        print(f"Doctor ID: {self.doctor_id}, Name: {self.name}, Specialty: {self.specialty}")
        print("Available Times:", ", ".join(self.schedule))

# Appointment class
class Appointment:
    def __init__(self, appointment_id, patient, doctor, date, time):
        self.appointment_id = appointment_id
        self.patient = patient
        self.doctor = doctor
        self.date = date
        self.time = time
        self.status = "Confirmed"

    def confirm(self):
        self.status = "Confirmed"
        print(f"\nAppointment {self.appointment_id} confirmed.")

    def cancel(self):
        self.status = "Cancelled"
        print(f"\nAppointment {self.appointment_id} has been cancelled.")

# HospitalSystem class
class HospitalSystem:
    def __init__(self):
        self.patients = {}
        self.doctors = {}
        self.appointments = {}

    def add_patient(self, name, age, gender):
        patient_id = f"P{len(self.patients)+1:03d}"
        new_patient = Patient(name, age, gender, patient_id)
        self.patients[patient_id] = new_patient
        print(f"Patient {name} added with ID: {patient_id}")

    def add_doctor(self, name, age, gender, specialty, schedule):
        doctor_id = f"D{len(self.doctors)+1:03d}"
        new_doctor = Doctor(name, age, gender, doctor_id, specialty, schedule)
        self.doctors[doctor_id] = new_doctor
        print(f"Doctor {name} added with ID: {doctor_id}")

    def book_appointment(self, patient_id, doctor_id, date, time):
        if not patient_id.strip() or not doctor_id.strip():
            print("Patient or Doctor ID cannot be empty.")
            return

        if patient_id not in self.patients:
            print("Patient ID not found.")
            return
        if doctor_id not in self.doctors:
            print("Doctor ID not found.")
            return

        try:
            appointment_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            if appointment_date < datetime.date.today():
                print("You cannot book an appointment in the past.")
                return
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        doctor = self.doctors[doctor_id]

        if time not in doctor.schedule:
            print("Doctor not available at this time.")
            return

        for appointment in self.appointments.values():
            if (appointment.doctor.doctor_id == doctor_id and
                appointment.date == date and
                appointment.time == time and
                appointment.status == "Confirmed"):
                print("This time slot is already booked.")
                return

        appointment_id = f"A{len(self.appointments)+1:03d}"
        patient = self.patients[patient_id]
        new_appointment = Appointment(appointment_id, patient, doctor, date, time)
        self.appointments[appointment_id] = new_appointment
        patient.appointments.append(appointment_id)
        print(f"Appointment booked with ID: {appointment_id}")

    def view_appointments(self):
        if not self.appointments:
            print("No appointments scheduled.")
        else:
            print("\n--- All Appointments ---")
            for appt in self.appointments.values():
                print(f"{appt.appointment_id}: Patient {appt.patient.name}, Doctor {appt.doctor.name}, {appt.date} at {appt.time}, Status: {appt.status}")

    def cancel_appointment(self, appointment_id):
        if appointment_id in self.appointments:
            self.appointments[appointment_id].cancel()
        else:
            print("Appointment not found.")

    def generate_bill(self, appointment_id):
        if appointment_id not in self.appointments:
            print("Appointment not found.")
            return

        appointment = self.appointments[appointment_id]

        if appointment.status != "Confirmed":
            print("Cannot bill for a cancelled or unconfirmed appointment.")
            return

        print("\n" + "="*40)
        print("         SUNRISE HOSPITAL BILLING")
        print("="*40)
        print(f"Appointment ID: {appointment.appointment_id}")
        print(f"Patient: {appointment.patient.name} (ID: {appointment.patient.patient_id})")
        print(f"Doctor: {appointment.doctor.name} ({appointment.doctor.specialty})")
        print(f"Date: {appointment.date}")
        print(f"Time: {appointment.time}")
        print("-"*40)

        consultation_fee = 3000
        print(f"Consultation Fee: JMD ${consultation_fee}")

        try:
            extra_fee = float(input("Enter additional service fees (tests, meds): JMD $"))
            if extra_fee < 0:
                print("Fee cannot be negative. Defaulting to 0.")
                extra_fee = 0
        except ValueError:
            print("Invalid input. Defaulting extra fee to 0.")
            extra_fee = 0.0

        total = consultation_fee + extra_fee

        print("-"*40)
        print(f"TOTAL BILL: JMD ${total:.2f}")
        print("="*40)
        print("Thank you for choosing Sunrise Hospital!\n")

# Main menu loop

def main_menu():
    system = HospitalSystem()

    while True:
        print("\n===== Hospital Management System =====")
        print("1. Add Patient")
        print("2. Add Doctor")
        print("3. Book Appointment")
        print("4. View Appointments")
        print("5. Cancel Appointment")
        print("6. Generate Bill")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            name = input("Enter patient's name: ")
            while True:
                try:
                    age = int(input("Enter patient's age: "))
                    if age < 0:
                        print("Age cannot be negative.")
                    else:
                        break
                except ValueError:
                    print("Please enter a valid number.")
            gender = input("Enter patient's gender: ")
            system.add_patient(name, age, gender)

        elif choice == "2":
            name = input("Enter doctor's name: ")
            while True:
                try:
                    age = int(input("Enter doctor's age: "))
                    if age < 0:
                        print("Age cannot be negative.")
                    else:
                        break
                except ValueError:
                    print("Please enter a valid number.")
            gender = input("Enter doctor's gender: ")
            specialty = input("Enter specialty (e.g., Dentist, Surgeon): ")
            schedule = input("Enter available times (comma separated, e.g. 9:00 AM, 10:00 AM): ")
            schedule_list = [s.strip() for s in schedule.split(",") if s.strip()]
            if not schedule_list:
                print("No valid schedule entered. Defaulting to empty list.")
            system.add_doctor(name, age, gender, specialty, schedule_list)

        elif choice == "3":
            patient_id = input("Enter patient ID: ")
            doctor_id = input("Enter doctor ID: ")
            date = input("Enter appointment date (YYYY-MM-DD): ")
            time = input("Enter time (e.g. 10:00 AM): ")
            system.book_appointment(patient_id, doctor_id, date, time)

        elif choice == "4":
            system.view_appointments()

        elif choice == "5":
            appointment_id = input("Enter appointment ID to cancel: ")
            system.cancel_appointment(appointment_id)

        elif choice == "6":
            appointment_id = input("Enter appointment ID to generate bill: ")
            system.generate_bill(appointment_id)

        elif choice == "7":
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

# Start the program
main_menu()

# Academic Integrity Statement
print("\nI CERTIFY THAT I HAVE NOT GIVEN OR RECEIVED ANY UNAUTHORIZED ASSISTANCE ON THIS ASSIGNMENT")
print("Electronic Signature: Immnauel Gayle")
