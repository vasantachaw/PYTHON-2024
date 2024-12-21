from tqdm import tqdm
import time
import mysql.connector as mq
import numpy as np
from mysql.connector import Error
from datetime import datetime


class SBI_BANK:
    def __init__(self):

        self.sbi_db_connection = mq.connect(
            host="localhost", user="root", password="", autocommit=True
        )
        try:
            if self.sbi_db_connection.is_connected():
                self.cursor = self.sbi_db_connection.cursor()
                self.cursor.execute("use sbibank")

        except Error as e:
            print(f"Error {e}")

    def register(self):
        print("\n\n")
        print(np.char.center(" S B I    R E G I S T E R A T I O NN    F O R M", 160))
        print("\n")
        self.fname = str(input(" Enter your First Name : ")).lower()
        self.lname = str(input(" Enter your last Name : ")).lower()
        self.age = int(input(" Enter your Age : "))
        self.sex = str(input(" Enter your Gender M/F : ")).lower()
        self.address = str(input(" Enter your Address : ")).lower()
        self.dob = str(input(" Enter your Date Of Birth : "))
        self.add_email = str(input(" Enter your Email Id : ")).lower()
        self.occupation = str(input(" Enter your Occupation : ")).lower()
        self.phone = int(input(" Enter your Phone Number : "))
        self.pincode = int(input(" Set Your New pin Code : "))
        self.balance = float(input(" Enter your Intial Deposite Amount : $"))

        try:
            if self.sbi_db_connection.is_connected():
                self.sql = """insert into sbi_database (fname,lname,age,sex,address,dob,add_email,occupation,phone,pincode,balance,dates)
                values
                (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)  """

                self.dt = [
                    self.fname,
                    self.lname,
                    self.age,
                    self.sex,
                    self.address,
                    self.dob,
                    self.add_email,
                    self.occupation,
                    self.phone,
                    self.pincode,
                    self.balance,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ]
                self.cursor.execute(self.sql, self.dt)
                self.sbi_db_connection.commit()
                print(" \n Submit Successfull !\n")
        except Error as e:
            print(f"Error {e}")

    def reset(self):
        print("\n\n")
        print(np.char.center(" S B I    U P D A T E    P I N C O D E", 160))
        print("\n")
        try:
            if self.sbi_db_connection.is_connected():
                self.add_email = str(input(" Enter your Email Id : "))
                self.dob = str(input(" Enter your Date Of Birth : "))
                self.pin_fetch_query = "select add_email,dob from sbi_database"
                self.cursor.execute(self.pin_fetch_query)
                self.new_data = self.cursor.fetchall()
                for self.data in self.new_data:
                    if self.add_email.lower() == self.data[
                        0
                    ].lower() and self.dob == str(self.data[1]):
                        self.pincode = int(input(" Update Your  pin Code : "))
                        self.pincode1 = int(input(" Confirm your  pin Code : "))
                        if self.pincode == self.pincode1:
                            self.update_pin = f"update sbi_database set pincode='{self.pincode1}' where add_email='{self.add_email}' and dob='{self.dob}'"
                            self.cursor.execute(self.update_pin)
                            self.sbi_db_connection.commit()
                            self.cursor.close()
                            self.sbi_db_connection.close()
                            print(" Successfully Update Your Pincode !\n")

                        else:
                            pass

                    else:
                        print("not login")
        except Error as e:
            print(f"Error {e}")


class SBI_ATM(SBI_BANK):
    def __init__(self):
        super().__init__()
        print(" Please Insert Your Card .")
        for i in tqdm(range(101), desc=" Loading…", ascii=False, ncols=75):
            time.sleep(0.0)

    def display(self):
        print("\n 1. Deposite Your Amount .")
        print(" 2. Withdraw Your Amount .")
        print(" 3. Inqury Your blance .")
        print(" 4. Cancel . ", end="")

    def enter_pin(self):
        self.pin_code = int(input("\n Enter Your Pin Code : "))

    def enter_amount(self):
        self.amount = float(input(" Enter Your amount : $"))

    def deposite_amount(self):
        try:
            self.enter_amount()
            self.cursor.execute(self.pin_fetch_query)
            self.am = self.cursor.fetchall()
            for amu in self.am:
                if self.pin_code == amu[0]:

                    self.cursor.execute(
                        f"select balance from sbi_database where pincode='{self.pin_code}'"
                    )
                    self.amt = self.cursor.fetchall()
                    for k in self.amt:
                        self.cursor.execute(
                            f"update sbi_database set balance='{k[0]+self.amount}' where pincode='{self.pin_code}'"
                        )
                        self.sbi_db_connection.commit()
                        print(" Successfully Deposited !")

        except ValueError as e:
            print(e)

    def inqury_balannc(self):
        try:
            self.cursor.execute(
                f"select fname,lname,balance from sbi_database where pincode='{self.pin_code}'"
            )
            self.inquary_amount = self.cursor.fetchall()
            for self.inq_amount in self.inquary_amount:

                print()
                print(np.char.center(" Account Holder Balance Detail 1", 160))
                print(
                    np.char.center(
                        "-----------------------------------------------------------------------------------",
                        160,
                    )
                )
                print(
                    np.char.center(
                        f" First name : {self.inq_amount[0]}   |   Last Name : {self.inq_amount[1]}   |   Baalance : ${self.inq_amount[2]}0 ",
                        160,
                    )
                )
                print()
            self.cursor.close()
            self.sbi_db_connection.close()
        except Error as e:
            print("EEroor", e)
        # print(f" Your Total Amount : ${self.balance}.00")

    def withdraw_amount(self):
        try:
            self.enter_amount()
            self.cursor.execute(self.pin_fetch_query)
            self.am = self.cursor.fetchall()
            for amu in self.am:
                if self.pin_code == amu[0]:

                    self.cursor.execute(
                        f"select balance from sbi_database where pincode='{self.pin_code}'"
                    )
                    self.amt = self.cursor.fetchall()
                    for real_amount in self.amt:

                        if real_amount[0] > self.amount and 0 < real_amount[0]:
                            upmoney = real_amount[0]
                            upmoney -= self.amount
                            self.cursor.execute(
                                f"update sbi_database set balance='{upmoney}' where pincode='{self.pin_code}'"
                            )
                            self.sbi_db_connection.commit()
                            print(f" Your ${upmoney}0 Withdraw Successfully  ")

                        else:
                            print(" Insufficiant balance !")
        except Error as e:
            print(e)


if __name__ == "__main__":
    print("\n\n")
    print(np.char.center(" WE L C O M E   T O    S B I    B A N K \n", 165))
    print("\n")
    print(np.char.center("1. Set Up Your Account Now !", 160))
    print(np.char.center("             2. Access Your Money, Anytime, Anywhere !", 160))
    print(np.char.center("3. Reset ATM Pincode !", 153))

    chose = int(input())
    print("\n")
    sbibnk = SBI_ATM()
    if chose == 1:
        sbibnk.register()
    elif chose == 2:
        try:
            sbibnk.enter_pin()
            if sbibnk.sbi_db_connection.is_connected():
                sbibnk.pin_fetch_query = "select pincode from sbi_database "
                sbibnk.cursor.execute(sbibnk.pin_fetch_query)
                new_datas = sbibnk.cursor.fetchall()
                for datas in new_datas:
                    if sbibnk.pin_code == datas[0]:
                        sbibnk.pin = sbibnk.pin_code
                        while True:
                            sbibnk.display()
                            chose = int(input())
                            if chose == 1:
                                sbibnk.deposite_amount()
                            elif chose == 3:
                                sbibnk.withdraw_amount()
                            elif chose == 4:
                                sbibnk.inqury_balannc()
                            else:
                                break
                                # case 1:
                                #     sbibnk.deposite_amount()
                                # case 2:
                                #     sbibnk.withdraw_amount()

                                # case 3:
                                #     sbibnk.inqury_balannc()
                                # case 4:
                                #     break
                else:
                    print(" WWrong Pincode !")
        except Error as e:
            print(f" {e}")

    elif chose == 3:
        sbibnk.reset()
    else:
        print(" Invalid choosed !")
