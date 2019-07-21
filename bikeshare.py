import time
import pandas as pd
import numpy as np
from collections import Counter

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # .lower() suggested by previous reviewer
    while True:
        city = input("Which city would you like to get data for? (Chicago, New York City or Washington in lowercase) ").lower()
        if city in ["chicago", "new york city", "washington"]:
            break
        else:
            print("That is not a valid entry for a city, please try again. ")
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month would you like data on? (january to june or all) ").lower()
        if month in ["january", "february", "march", "april", "may", "june", "all"]:
            break
        else:
            print("Please try again. That was not a valid entry. ")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("which day of the week would you like data on? Or choose 'all' to not filter by days of the week. ").lower()
        if day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]:
            break
        else:
            print("Please try again, that was not a valid day of the week. ")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df["month"] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    popular_month = df["month"].mode()[0]
    popular_day = df["day_of_week"].mode()[0]
    popular_hour = df["Start Time"].dt.hour.mode()[0]

    # display the most common month
    #check if there is one or more months in month column.
    if len(set(df["month"])) == 1 and len(set(df["day_of_week"])) != 1:
        #print ("Since you have filtered by month, the most common month is of course:", months[popular_month-1].title(), ". The most popular day of the week is", popular_day, "and the most popular time of day is:", popular_hour + ".")
        print("Since you have filtered by month, the most common month is of course: {}. The most popular day of the week is {}, and the most popular time of day is: {}".format(months[popular_month-1].title(),popular_day, popular_hour))

    # display the most common day of the week
    if len(set(df["day_of_week"])) == 1 and len(set(df["month"])) != 1:
        print("Since you have filtered by day, the most common day of the week is of course {}, the most popular hour is {}, and the most popular month for {} is {}.".format(popular_day, popular_hour, popular_day, months[popular_month-1].title()))

    # check if df has been filtered by both month and day
    if len(set(df["day_of_week"])) == 1 and len(set(df["month"])) == 1:
        #print("You have filtered by both month and day; the most popular time of day for a", popular_day, "in", months[popular_month-1].title(), "is", popular_hour), "."
        print("You have filtered by both month and day; the most popular time of day for a {} in {} is {}.".format(popular_day, months[popular_month-1].title(), popular_hour))
    # check if dataframe has been filtered
    if len(set(df["day_of_week"])) != 1 and len(set(df["month"])) != 1:
        #print("For" + city, ", the most popular month is:" + months[popular_month-1].title(), "the most popular day of the week is" + popular_day, "and the most popular hour is" + popular_hour + ".")
        print("For your city, the most popular month is {}, the most popular day of the week is {} and the most popular hour is {}.".format(months[popular_month-1].title(), popular_day, popular_hour))



    # display the most common start hour



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start = df["Start Station"].mode()[0]

    # display most commonly used end station
    pop_end = df["End Station"].mode()[0]

    # display most frequent combination of start station and end station trip
    start_end_combined = list(zip(df["Start Station"], df["End Station"]))
    pop_combined = Counter(start_end_combined).most_common(1)[0][0] #https://stackoverflow.com/questions/39989608/python-counting-multiple-modes-in-a-list

    print("The most popular start station is:", pop_start)
    print("the most popular end station is:", pop_end)

    print ("The most frequent trip was from {} to {}".format(*pop_combined))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time for your city is:", df["Trip Duration"].sum())

    # display mean travel time
    print("Mean travel time for your city is:", df["Trip Duration"].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()

    # Display counts of gender
    # Display earliest, most recent, and most common year of birth
    try:
         gender = df["Gender"].value_counts()
         old_customer = int(df["Birth Year"].min())
         young_customer = int(df["Birth Year"].max())
         common_age = int(df["Birth Year"].mode()[0])

         print("The oldest users were born in {}, the youngest in {}. The most common year of birth is {}. {} men vs. {} women used the bike service for your filter selection. There were {} subscribers and {} customers.".format(old_customer, young_customer, common_age, gender[0], gender[1], user_types[0], user_types[1]))
    # check for city data that doesn't have  all information on users.
    except KeyError:
        print("There is no information on gender or age for your city."),
        print("The user types are available: for your filter(s) there are", user_types[0], "subscribers and", user_types[1], "customers.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    counter = 6
    raw_data = input("Would you like to see some raw data? (answer y/n) ")
    if raw_data == "y":
        print(df.iloc[:counter])
        counter += 6
        more_data = input("Would you like to see more? ")
        while more_data == "y":
            print (df.iloc[:counter])
            counter += 6
            more_data = input("even more? ")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
