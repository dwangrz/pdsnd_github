import time
import pandas as pd
import numpy as np
from IPython.display import display

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

    city = input("\nWould you like to see data for Chicago, New York City or Washington?\n").lower()

    while city not in CITY_DATA.keys():
        city = input("\nInvalid input, please input city 'Chicago', 'New York City' or 'Washington'\n").lower()


    # get user input for month (all, january, february, ... , june)
    month = input("\nWould you like to filter the data by month? type the month(january, february, ..., june) or 'all' for no time filter.\n").lower()

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while month not in months:
        month = input("\nInvalid month input? type the month(january, february, ..., june) or 'all' for no time filter.\n").lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("\nWould you like to filter the data by day of week? type the day(monday, tuesday, ... sunday) or 'all' for no day filter.\n").lower()

    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while day not in days:
        day = input("\nInvalid day input? type the day(monday, tuesday, ... sunday) or 'all' for no day filter.\n").lower()


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
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_index = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month_index]

    df['day_of_week'] = df['Start Time'].dt.day_of_week
    if day != 'all':
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        #The day of the week with Monday=0, Sunday=6.
        day_index = days.index(day.title())
        df = df[df['day_of_week'] == day_index]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    popular_month = df['month'].mode()[0]

    popular_month_count = df[df['month'] == popular_month].shape[0]

    print('The Most Common Month: {}, Count: {}'.format(popular_month, popular_month_count))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    popular_day_count = df[df['day_of_week'] == popular_day].shape[0]

    print('The Most common day of week:', popular_day, 'Count:', popular_day_count)


    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    popular_hour_count = df[df['hour'] == popular_hour].shape[0]

    print('The Most common start hour: {}, Count: {}'.format(popular_hour, popular_hour_count))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    popular_start_station_count = df[df['Start Station'] == popular_start_station].shape[0]

    print('The Most commonly used start station: {}, Count: {}'.format(popular_start_station, popular_start_station_count))


    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    popular_end_station_count = df[df['End Station'] == popular_end_station].shape[0]

    print('The Most commonly used end station: {}, Count: {}'.format(popular_end_station, popular_end_station_count))


    # display most frequent combination of start station and end station trip

    print('\ndisplay most frequent combination of start station and end station trip...\n')

    popular_start_end_station = df[['Start Station', 'End Station']].mode().iloc[0]

    popular_start_end_station_count = df[(df['Start Station'] == popular_start_end_station[0]) & (df['End Station'] == popular_start_end_station[1])].shape[0]

    print('Start: {}, End: {}, Count: {}'.format(popular_start_end_station[0], popular_start_end_station[1], popular_start_end_station_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    print('Total travel time: {}, Count: {}'.format(total_travel_time, df['Trip Duration'].shape[0]))


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    print('Mean travel time: {}'.format(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    print('\nCalculating User types:\n')

    user_types = df['User Type'].dropna().unique()

    for type in  user_types:
        print('\n{}, Count: {}'.format(type, df.loc[df['User Type'] == type].shape[0]))


    # Display counts of gender
    # Washington file does not have 'Gender' and 'Birth year' columns
    print('\nCalculating User genders:\n')

    genders = []
    if 'Gender' in df:
        genders = df['Gender'].dropna().unique()
    else:
        print("\nColumn 'Gender' does not exist in dataFrame\n")

    for gender in genders:
        print('\n{}, Count: {}'.format(gender, df.loc[df['Gender'] == gender].shape[0]))



    # Display earliest, most recent, and most common year of birth
    print('\nCalculating earliest, most recent, and most common year of birth:\n')

    if 'Birth Year' in df:
        birth_year = df['Birth Year'].dropna()
        birth_year_min = birth_year.min()
        birth_year_max = birth_year.max()
        birth_year_most_common = birth_year.mode()[0]
        print("\nThe most earlist year of birth: {} \nThe most recent year of birth: {} \nThe most most common year of birth: {}".format(birth_year_min, birth_year_max, birth_year_most_common))
    else:
        print("\nColumn 'Birth Year' does not exist in dataFrame\n")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """
    Asks user if want to displays next 5 rows of individual trip data. 'yes' will displays next 5 rows data.
    'no' will exit.
    """
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while (view_data.lower() != 'no'):
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_data = input("\nDo you want to see the next 5 rows of data?\n").lower()
        reply = view_data.lower()
        if reply != 'yes':
            print('Your answer is: \"{}\", will not dispaly trip data anymore.'.format(reply))
            break


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
