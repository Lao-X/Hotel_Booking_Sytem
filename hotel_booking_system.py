import csv
from datetime import datetime
from tkinter import *

# Read csv file
rooms = []
with open('hotel_room.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader) # skip header
    for row in reader:
        rooms.append({'Room ID': row[0], 'Room Type': row[1], 'Max People': row[2], 'Price': row[3]})


# Book a room functions
def int_peeps():
    """ Convert str input to integer, if input is wrong, request another input """
    pp = input('Enter number of people from 1-4')  # tkinter
    try:
        pp = int(pp)
        # Checks if int(pp) is between 1-4, 1 and 4 included
        if 1 <= pp <= 4:
            room_filter(pp)
        else:
            print('Invalid!!, Enter number of people from 1-4')
            int_peeps()
    except ValueError:
        print('Invalid, Enter number of people from 1-4')
        int_peeps()


def room_filter(pp):
    """ Filters rooms to show available rooms based on number of guests """
    # empty set
    set_1 = set()
    # empty dicitionary
    dict_rooms = {}
    pep = str(pp)
    for room in rooms:  # iterates through the variable containing the csv file that has been read
        if pep == '1':
            set_1.add(room['Room Type'])
        elif pep == '2':
            if room['Max People'] != '1':
                set_1.add(room['Room Type'])
        elif (pep == '3') | (pep == '4'):
            if (room['Max People'] != '1') & (room['Max People'] != '2'):
                set_1.add(room['Room Type'])

    no_rooms = len(set_1)
    for x, y in zip(range(0, no_rooms), set_1):
        dict_rooms.update({x: y})

    select_room(dict_rooms)


# Global varaible to store the room which was selected in a list
room_selected = []

def select_room(dict_rooms):
    """ Prompts the user/guest to select desired room """
    room_index = input(f"Enter number assigned to desired room {dict_rooms}")
    try:
        if int(room_index) in dict_rooms.keys():
            # place room into a global variable to be accessed later for the receipt
            room_selected.append(dict_rooms[int(room_index)])
            print(dict_rooms[int(room_index)])
        else:
            select_room(dict_rooms)

    except ValueError:
        # If there is a ValueError the function will be recalled requesting a proper input
        print('Invalid')
        select_room(dict_rooms)


def date_check_in():
    """ Converts the check-in-date to date time """
    check_in = input("Check in date: [DD/MM/YYYY]")
    try:
        check_in_date = datetime.strptime(check_in, "%d/%m/%Y").date()
        date_check_out(check_in_date)
    except ValueError:
        # If there is a ValueError the function will be recalled requesting a proper input
        print('date incorrect')
        date_check_in()


def date_check_out(check_in_date):
    """ Converts the check-out-date to date time"""
    check_out = input("Check out date: [DD/MM/YYYY]")  # tkinter
    try:
        check_out_date = datetime.strptime(check_out, "%d/%m/%Y").date()
        # Ensures check-out-date doesn't come before check-in-date
        if check_out_date <= check_in_date:
            print('Check out date must be at least a day(24 hours) after check in date')
            date_check_out(check_in_date)
        else:
            duration_stay(check_out_date, check_in_date)

    except ValueError:
        # If there is a ValueError the function will be recalled requesting a proper input
        print('date incorrect')
        date_check_out(check_in_date)


# Global varaible to store the check in, check out dates and duration of stay
date_details = []

def duration_stay(check_out_date, check_in_date):
    """ Stores check-in, check-out dates and duration of stay in a list """
    days = check_out_date - check_in_date
    details = [check_in_date, check_out_date, days.days]
    # for this global list (date_details) check-in first, check-out second, duration last
    date_details.extend(details)


reservation_cost = []

def booking_price():
    """ Get the rate of the selected room and calculate the reservation price to be paid """
    price_set = set()
    price_list = []  # make a global variable
    for room in rooms:
        if room_selected[0] == room['Room Type']:  # or call the function in the function select_room(dict_rooms)
            price_set.add(room['Price'])
    for pce in price_set:
        price_list.append(pce)

    # Rate first then actual cost of the reservation
    reservation_cost.extend([price_list[0], int(price_list[0]) * date_details[2]])
    print(f"{date_details[2]} Nights X £{price_list[0]}")
    print(f"You will pay £{int(price_list[0]) * date_details[2]}")

def store_in_csv(receipt, re):
    """ Store completed bookings in a csv file """
    column_head = ['Ref_tag', 'Name', 'Check_in_date', 'Check_out_date', 'Room_type', 'Room_rate', 'Amount_to_pay']
    with open(re, 'a', newline = '') as f:
        writer = csv.DictWriter(f, fieldnames=column_head)
        if f.tell() == 0:
            writer.writeheader()
        for booking in receipt:
            writer.writerow(booking)

def clear_global_variables():
    """ Clear the global variables after storing details in the csv file """
    date_details.clear()
    room_selected.clear()
    reservation_cost.clear()


def del_rows():
    """ Delete rows from a csv file
        Output will be the details of the reservation being cancelled and
        Amount of money that will be returned to the customer
    """
    lines = list()
    ref_tag_del = input('Please enter reference tag')
    # call a function which gets the details of the reservation being cancelled
    receipt_del = receipt_cancel_res(ref_tag_del)
    # convert the amount to pay to an integer
    try:
        receipt_del[6] = int(receipt_del[6])

        # Searches the booking.csv file, locates desired reservation using ref_tag and deletes it
        with open(re, 'r', newline='') as readFile:
            reader = csv.reader(readFile)
            for row in reader:
                lines.append(row)
                for field in row:
                    if field == ref_tag_del:
                        lines.remove(row)
        with open(re, 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)

        print(
            f"Ref_tag:{receipt_del[0]}\nName:{receipt_del[1]}\nCheck_in_date:{receipt_del[2]}\nCheck_out_date:{receipt_del[3]}")
        print(
            f"Room_type:{receipt_del[4]}\nRoom_rate:{receipt_del[5]}\nAmount_to_pay:{receipt_del[6]}\nAmount_refunded:{0.70 * receipt_del[6]}")
        print('Cancel completed!')

    except TypeError:
        print('Invalid Ref_tag')
        guest_action = input('Welcome to TIM HOTELS\n1.Book a Room\n2.Cancel a Reservation\n3.Quit\n')
        action_ss(guest_action)


def receipt_cancel_res(ref_tag_del):
    """ This function gets the details of the reservation being cancelled """
    with  open(re) as file_obj:
        # skip heading
        heading = next(file_obj)

        # Create reader objec by passing the file
        # object to reader method
        reader_obj = csv.reader(file_obj)

        # Iterate over each row in the csv using reader object
        for rw in reader_obj:
            if rw[0] == ref_tag_del:
                return rw


re = 'bookings.csv'  # Name of csv that will store the bookings
def book_a_room():
    """ Calls functions to book a room """
    name = input('Enter a Name:')  # tkinter
    # No of guests and select room type
    int_peeps()
    # Check-in, check-out dates and duration
    date_check_in()
    booking_price()

    # Create Reference tag using name, duration and reservation price
    ref_tag = name + str(date_details[2]) + str(reservation_cost[1])

    # Store booking details into the receipt
    receipt = []
    # From is the check_in_date, To is the check_out date
    receipt.append({'Ref_tag': ref_tag, 'Name': name, \
                    'Check_in_date': str(date_details[0]), 'Check_out_date': str(date_details[1]), \
                    'Room_type': room_selected[0], 'Room_rate': reservation_cost[0], \
                    'Amount_to_pay': reservation_cost[1]})

    print(receipt[0])
    print('Booking completed!')
    # Store booking details in a csv file
    store_in_csv(receipt, re)

    clear_global_variables()


def action_ss(guest_action):
    try:
        hotel_action = int(guest_action)
        if hotel_action == 1:
            book_a_room()
            guest_action = input('Welcome to TIM HOTELS\n1.Book a Room\n2.Cancel a Reservation\n3.Quit\n')
            action_ss(guest_action)
        elif hotel_action == 2:
            del_rows()
            guest_action = input('Welcome to TIM HOTELS\n1.Book a Room\n2.Cancel a Reservation\n3.Quit\n')
            action_ss(guest_action)
        elif hotel_action == 3:
            return # Quit
        else:
            print('Enter a number ranging from 1-3')
            guest_action = input('Welcome to TIM HOTELS\n1.Book a Room\n2.Cancel a Reservation\n3.Quit\n')
            action_ss(guest_action)
    except ValueError:
        print('Enter a number ranging from 1-3')
        guest_action = input('Welcome to TIM HOTELS\n1.Book a Room\n2.Cancel a Reservation\n3.Quit\n')
        action_ss(guest_action)


guest_action = input('Welcome to TIM HOTELS\n1.Book a Room\n2.Cancel a Reservation\n3.Quit\n')
action_ss(guest_action)