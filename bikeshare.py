#Update June 12, 2023

"""This project uses data provided by Motivate, a bike share system provider for many major cities in the United States,
to uncover bike share usage patterns between three large cities: Chicago, New York City, and Washington, DC.

REFERENCES
This project utilizes reference data and codes from Udacity and Udacity GPT
1. Explore US Bikeshare Data. Udacity.com. 
   Available at: https://learn.udacity.com/nanodegrees/nd104/parts/cd0024/lessons/ls1727/concepts/7845b970-2e46-4901-aafa-ba44702fd8fe 
   (Accessed: 12 June 2023).
   
-------------------------------------------------------------------------"""
import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
# list all supported cities, months, and days
cities = ['chicago', 'new york city', 'washington']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December', 'All']
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington)
    while True:
        city = str(input('Would you like to explore data for Chicago, New York City, or Washington?\n')).lower()

        if city not in cities:
            print(
                f'Error! The supported cities are "Chicago", "New York City", and "Washington".')
        else:
            break

    # get user input for month (all, jan, feb, ... , jun)
    print(f"You can explore data for each month or all months. Please enter 'All' for all months or each specific month, such as 'January',..,'December' \n")

    while True:
        month = str(input('Which month would like to explore: ')).title()

        if month not in months:
            print('The month is invalid! Please re-enter the month.')
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print(
        f"You can explore data for each day or all days in the week. Please enter 'All' for all week days or each specific days, such as 'Monday',...,'Sunday' \n")

    while True:
        day = str(input('Which day would like to explore: ')).title()

        if day not in days:
            print('The day is invalid! Please re-enter the day.')
        else:
            break

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # print(df.head())

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        month_number = months.index(month) + 1

        # create the new dataframe
        df = df[df['month'] == month_number]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Popular Times of Travel...\n')
    start_time = time.time()

    # calculate and display the most common month

    popular_month = df['month'].mode()[0]
    month_index = popular_month - 1
    print('   The most popular month is {}'.format(months[month_index]))

    # calculate and display the most common day of week
    # Count the number of occurrences of each day and take the highest count

    popular_day = df['day_of_week'].mode()[0]
    print('   The most popular day is', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]

    if common_hour > 12:
        am_pm = 'PM'
        time_ampm = common_hour - 12
    else:
        am_pm = 'AM'
        time_ampm = common_hour

    print('   The most common start hour is', time_ampm, am_pm)

    print("\nThis calculation took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    popular_start_station = df['Start Station'].mode()[0]
    print('   The most common Start Station is', popular_start_station)

    # display most commonly used end station

    popular_end_station = df['End Station'].mode()[0]
    print('   The most common End Station is', popular_end_station)

    # display most frequent combination of start station and end station trip

    df['trip'] = df['Start Station'] + ' to ' + df['End Station']
    common_trip = df['trip'].mode()[0]
    print('   The most common trip from start to end is', common_trip)

    print("\nThis calculation took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_travel_time = df['Trip Duration'].sum()

    # calculate the number of hours, minutes, and seconds
    hours = total_travel_time // 3600
    minutes = (total_travel_time % 3600) // 60
    seconds = total_travel_time % 60

    print('   The total travel time is:', hours, 'hours,', minutes, 'minutes,', round(seconds, 2), 'seconds')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    hours_m, remainder = divmod(mean_travel_time, 3600)
    minutes_m, seconds_m = divmod(remainder, 60)

    print('   The mean travel time is:', round(mean_travel_time, 2), 'seconds ')
    print('      or', hours_m, 'hour(s),', minutes_m, 'minute(s), and', round(seconds_m, 2), 'second(s)')

    print("\nThis calculation took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_types = df['User Type'].value_counts()

    print('   The user types are: ')
    for user, count_users in user_types.items():
        print('      ', user, ':', count_users)

    # Display counts of gender

    if 'Gender' not in df.columns:
        print('   The Gender data is not available for the current state.')
    else:
        gender_counts = df['Gender'].value_counts()
        print('\n   The user genders are: ')
        for gender, count in gender_counts.items():
            print('      ', gender, ':', count)

    # Display earliest, most recent, and most common year of birth

    if 'Birth Year' in df:
        min_birthyear = df['Birth Year'].min()
        max_birthyear = df['Birth Year'].max()
        common_birthyear = df['Birth Year'].mode()[0]

        print('\n   The Birth Year data are:')
        print('       Earliest   :', int(min_birthyear))
        print('       Most recent:', int(max_birthyear))
        print('       Most common:', int(common_birthyear))

    else:
        print('   The Birth Year data is not available for the current state.')

    print("\nThis calculation took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def list_data(df):
    """Prompt user if they want to see the raw data. If the answer is 'Yes', then it will print 5 rows of data at a time until the answer 'No' is received"""
    start_index = 0

    while True:
        user_input = input('Continue with reviewing raw data (Y/N)? ')

        if user_input.lower() == 'y':
            if start_index < len(df):
                print(df.iloc[start_index:start_index + 5])
                start_index += 5
        elif user_input.lower() == 'n':
            break
        else:
            print('Invalid input! Please enter Y or N')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        list_data(df)

        restart = input('\nWould you like to restart (Y/N)?\n')
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
    main()
