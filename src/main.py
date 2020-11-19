# main.py -- the bootstrapper
#
# Author: Daniel Choo
# Date:   11/17/20
# URL:    https://www.github.com/kyoogoo/twump

from extract import Extract
from analysis import Analysis


def main():
    # Initializing variables.
    extract = Extract()
    analysis = Analysis()
    menu_check = [1, 2, 3]
    usr_input = -1
    input_flag = False

    logo = """.   . .    .  .    .  .    .  .    .  .    .  .    .  .    .  .
 .     .    .  .    .  .    .  .    ..S88888X88t. .    . . .      . .
  .    .   .  ;;   .       .       . .XX88888X8@@88@t%..:%88%   . .
     .   .   :@8t;   .  .    .  .   X888888X8X88S8X88888@88888:.      .  .
  .    .    .X888:X   .   .   .   .%888888888888888888888 @@8@  .     .
    .     .  88S888.X:  .   .   . :X88888%8 888888S@888%88888t    . .
  .   .     .S@8 88888 8t.        X8888@8S8888S8888S88 8 88@t . .      .
    .   . .  ;888 8888888@8@..  . 88888888S88 8 @888%X8888X.      .  .
  .          :8 8888 888888@8 S88@8X8888888888888888888%88S .. .         .
     . .  .  %X@888888S888 8S@888888888S8 888 888 @ @8XS8S: .   .  . .
  .         .XX88888S8888X888 8S8 888888888888@888888S8888S    .   .    .
    .  . .   ;8S8 8 @88 8 88X8%888%8S888888888 88888888888. . .  .    .
  .        . :S @88888888888 888888888XS888888 8888 888 @      .    .
    . .  .   .:%8888888888S8888 888S88S8888 88888888888:    .  .     . .
  .        .   ;%8888 @8888 888888S888 8888888888888 S     .   . .
     . .        .888888S8888%8 888888S88888888S8 888:.  .    .      .
  .      .  . . .888 888 @88888 8S8888888S888@888 8   .   .    .  .
    .  .        ..@8888888888 8888S88S8 88888X8888      .   .        .
  .      .  .  .  : X8%8S8 888888S8888888%8S8888:        .   . .  .
    . .       .  .   . ;8@8 888 88888888 @88 8St     .     .
  .     . .      .   ;888888S888S@88 8888 888t         .     .  .  .
     .     .t%%SS@88 88888888 88888 @88X8888.  .  .  .   .    .     .
  .    .    ;8X@888%88888 @88888 8S@8@ 888..           .   .     .
    .    . . :S@888 888888 888S88888888 .    . .  . .    .   .  .   .
  .   .      ...%t   .t88888888; S.%::  .  .     .    .    .      .
    .   .  .  .        :t.:;;.. .  .         .      .   .    .  .
  .      .   . .  . .  ...   ..      . . .     .  .   .   .   .    .  """

    print(logo + "\n")
    api = extract.authorize()    # Checking users' consumer/api key.

    # While the user would like to keep running the program...
    while True:
        while not input_flag:
            # Prompt user
            try:
                print("\nWhat would you like to do?\n1.) Scrape\n2.) Analysis\n3.) Exit\n", end="\r")
                usr_input = int(input("\nEnter your choice: "))
                if usr_input in menu_check:
                    input_flag = True

            # Invalid input.
            except ValueError:
                print("\nInvalid input. Proper responses: 1, 2, 3 (integers)")

        # Extract tweets
        if usr_input == 1:
            extract.scrape(api)

        # Doing K-NN analysis.
        elif usr_input == 2:
            analysis.menu()

        # Bye :(
        elif usr_input == 3:
            print("\nBye :(")
            return 0

        # This should not be possible. Literally. I think.
        else:
            raise Exception('This is not possible. How did you get here.')

        # Gotta reset our flag.
        input_flag = False

    return 0


main()
