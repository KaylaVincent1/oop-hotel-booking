import pandas

df = pandas.read_csv("hotels.csv", dtype={"id":str})
df_cards= pandas.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards_security = pandas.read_csv("card_security.csv", dtype=str)
class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    # changes availability to "no"
    def book(self):
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    # checks if hotel is available
    def available(self):
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False

class Reservation:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here is your booking data:
        Name: {self.customer_name}
        Hotel name: {self.hotel.name}
        """
        return content

class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {"number": self.number, "expiration": expiration,
                     "holder":holder, "cvc":cvc}

        # if the card data is in the csv file
        if card_data in df_cards:
            return True
        else:
            return False

# SecureCreditCard(CreditCard) --> SecureCreditCard class inherits the methods of the CreditCard class
class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        # give the password value where password matches number
        password = df_cards_security.loc[df_cards_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False

class SpaBooking(Reservation):
    def generate(self):
        content = f"""
           Thank you for your SPA reservation!
           Here is your SPA booking data:
           Name: {self.customer_name}
           Hotel name: {self.hotel.name}
           """
        return content

print(df)
hotel_id = input("Enter the id of the hotel: ")
hotel = Hotel(hotel_id)

if hotel.available():
    credit_card = SecureCreditCard(number="1234567890123456")
    if credit_card.validate(expiration="12/26", holder="JOHN SMITH", cvc="123"):
        if credit_card.authenticate(given_password="mypass"):
            hotel.book()
            name = input("Enter your name: ")
            reservation_ticket = Reservation(customer_name=name.title(), hotel_object=hotel)
            print(reservation_ticket.generate())

            spa_package = input("Do you want to book a spa package? ")
            if spa_package == "yes":
                spa_reservation_ticket = SpaBooking(customer_name=name.title(), hotel_object=hotel)
                print(spa_reservation_ticket.generate())
            else:
                exit(0)
        else:
            print("Credit card authentication failed")
    else:
        print("There was a problem with the payment")
else:
    print("Hotel is not free.")

