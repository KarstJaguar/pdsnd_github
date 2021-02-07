import time
import datetime
import calendar
import pandas as pd
import numpy as np

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
    city_valid = False
    city = ""
    month_valid = False
    month = ""
    #use dictionary to convert month entry to number to be used for month.
    months = {'january':'1', 'february':'2', 'march':'3', 'april':'4', 'may':'5', 'june':'6'}
    day_valid = False
    day = ""
    #use dictionary to convert day entry to number to be used for getting weekday.
    days = {'sunday':'6', 'monday':'0', 'tuesday':'1', 'wednesday':'2', 'thursday':'3', 'friday':'4', 'saturday':'5'}

    print('Hello! Let\'s explore some US bikeshare data! \n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city_valid == False:
        city = input("Which city would you like to explore data for? Enter Chicago, New York City, or Washington. \n")
        city = city.lower()
        #Use if statement to check that selection was valid.
        if city in CITY_DATA:
            city_valid = True
            city = CITY_DATA[city]
        else:
            city_valid = False
            print('Your entry was invalid. You must enter Chicago, New York City, or Washington. \n')

    # get user input for month (all, january, february, ... , june)
    while month_valid == False:
        month = input("\nWhich month would you like to explore data for? Enter All, January, February, March, April, May, or June. \n")
        selected_month = month.lower()
        #Use if statement to check that selection was valid.
        if selected_month == 'all' or selected_month in months:
            month_valid = True
            month = selected_month
        else:
            print('Your entry was invalid. You must enter: All, January, February, March, April, May, or June. \n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day_valid == False:
        selected_day = input('\nWhich day of the week that you want to explore data for. Enter All, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or Saturday. \n')
        selected_day = selected_day.lower()
        #Use if statement to check that selection was valid.
        if selected_day == 'all' or selected_day in days:
            day_valid = True
            day = selected_day
        else:
            print('Your entry was invalid. You must enter: All, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or Saturday. \n \n')

    if month == 'all':
        month = None
    else:
        month = months[month]

    if selected_day == 'all':
        day = None
    else:
        day = days[day]

    print('-'*40)
    return city, month, day

def get_weekday(day):
    days_dictionary = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
    return days_dictionary[day]

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

    filename = city
    """The index_col=[0] code in the read_csv function below was obtained from
    https://stackoverflow.com/questions/36519086/how-to-get-rid-of-unnamed-0-column-in-a-pandas-dataframe
    in a post by cs95 dated Jan 25, 2019 and edited by smci on Dec 15, 2020.
    This code prevents an issue with an unnamed column being displayed to the user
    when individual records are displayed.
    """
    df = pd.read_csv(filename, index_col=[0])
    #Convert Start Time to date time to extract hour, month, year, and day.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['year'] = df['Start Time'].dt.year
    df['day'] = df['Start Time'].dt.day
    df['Start and End Station'] = df['Start Station'] + " to " + df['End Station']

    """Code example for getting the day of week from a date was found at
    https://stackoverflow.com/questions/30222533/create-a-day-of-week-column-in-a-pandas-dataframe-using-python
    in a post by Liam Foley, May 13, 2015.  Post was edited by Peque
    August 30, 2018.
    """
    df['weekday'] = df['Start Time'].dt.dayofweek
    days = {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}
    df['weekday'] = df['weekday'].apply(lambda x: days[x])

    """Code for removing spaces in column names and for querying dataframes was
    found at https://www.geeksforgeeks.org/python-filtering-data-with-pandas-query-method/
    in a post dated August 23, 2019.
    """
    df.columns =[column.replace(" ", "_") for column in df.columns]

    if month == None and day == None:
        return df

    if month != None and day == None:
        df.query("month == %s" %(month), inplace = True)
        return df

    if month != None and day != None:
        df.query("month == %s and day == %s" %(month, day), inplace = True)
        return df

    if month == None and day != None:
        df.query("day == %s" %(day), inplace = True)
        return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""
    total_rows = df.shape[0]
    print(f"Your query returned {total_rows:,} trips. These trips will be analyzed to")
    print("provide information on the most frequent travel times, most")
    print("popular stations, most popular trips, trip duration, and user")
    print("information.\n")

    print('Calculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    #Use a dictionary to get name of month instead of number.
    months = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June"}
    days = {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}
    # display the most common month
    if month == None:
        most_common_month = months[df['month'].mode()[0]]
        print("The most common month for trips meeting your search criteria is %s." %(most_common_month))
    else:
        print("You selected %s as a filter." %(months[int(month)]))

    # display the most common day of week
    if day == None:
        most_common_day = df['weekday'].mode()[0]
        print("The most common day for trips meeting your search criteria is %s." %(most_common_day))
    else:
        print("You selected %s a filter." %(days[int(day)]))

    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print("The most common hour for trips meeting your search criteria is %s." %(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    #remove blank values.
    start_station_frame = df.dropna(subset=['Start_Station'], inplace=False)
    most_common_start_station = start_station_frame['Start_Station'].mode()[0]
    start_station_count = start_station_frame['Start_Station'].value_counts().max()
    print("The most common start station is %s" % (most_common_start_station))
    print("Count: %s." %(start_station_count))

    # display most commonly used end station
    end_station_frame = df.dropna(subset=['End_Station'], inplace=False)
    most_common_end_station = end_station_frame['End_Station'].mode()[0]
    end_station_count = end_station_frame['End_Station'].value_counts().max()
    print("\nThe most common end station is %s." % (most_common_end_station))
    print("Count: %s." %(end_station_count))

    # display most frequent combination of start station and end station trip
    most_common_trip_frame = df.dropna(subset=['Start_and_End_Station'], inplace=False)
    most_common_trip = most_common_trip_frame['Start_and_End_Station'].mode()[0]
    start_end_station_count = most_common_trip_frame['Start_and_End_Station'].value_counts().max()
    print("\nThe most common trip is %s." % (most_common_trip))
    print("Count: %s." %(start_end_station_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip_Duration'].sum()
    total_travel_time_days = int(total_travel_time / (3600 * 24))
    total_travel_time_hours = int((total_travel_time % (3600 * 24)) / 3600)
    total_travel_time_minutes = int(((total_travel_time % 3600) / 60))
    total_travel_time_seconds = int(((total_travel_time % 3600) % 60))
    print("The total travel time for trips meeting your criteria is %s days %s hours %s minutes %s seconds" %(total_travel_time_days, total_travel_time_hours, total_travel_time_minutes, total_travel_time_seconds))
    # display mean travel time
    average_travel_time = df['Trip_Duration'].mean()
    average_travel_time_minutes = int(average_travel_time / 60)
    average_travel_time_seconds = int(average_travel_time % 60)
    print("\nThe average travel time was %s minutes %s seconds." %(average_travel_time_minutes, average_travel_time_seconds))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Here is the breakdown of users by type.")
    user_series = df['User_Type'].value_counts()
    user_dict = user_series.to_dict()
    """Code for printing dictionary keys and values can be found at
    https://stackoverflow.com/questions/26660654/how-do-i-print-the-key-value-pairs-of-a-dictionary-in-python
    in a post by Chepner dated October 30th, 2014.
    """
    for k,v in user_dict.items():
        print("%s: %s" %(k,v))

    """Code for checking if column exists in dataframe was found at
    https://stackoverflow.com/questions/24870306/how-to-check-if-a-column-exists-in-pandas
    in a post by chrisb dated July 21, 2014.
    """
    #Display Gender information.
    #Check if column exists in dataframe.
    if 'Gender' in df.columns:
        print("\nHere is a breakdown of users by gender.")
        gender_series = df['Gender'].value_counts()
        gender_dictionary = gender_series.to_dict()
        """Code for printing dictionary keys and values can be found at
        https://stackoverflow.com/questions/26660654/how-do-i-print-the-key-value-pairs-of-a-dictionary-in-python
        in a post by Chepner dated October 30th, 2014.
        """
        for k,v in gender_dictionary.items():
            print("%s: %s" %(k,v))
    else:
        print("\nThe data you are analyzing does not have Gender data.")

    # Display earliest, most recent, and most common year of birth
    #Check if column exists in dataframe.
    if 'Birth_Year' in df.columns:
        print("\nHere is some information on user birth years.")
        print("Note that riders without birth years are not reflected here.\n")
        youngest_riders_frame = df
        youngest_riders_frame.dropna(subset=['Birth_Year'])
        youngest_riders_birth_year = int(youngest_riders_frame['Birth_Year'].max())
        youngest_riders_frame = youngest_riders_frame.query("Birth_Year == %s" %(youngest_riders_birth_year), inplace = False)
        youngest_rider_count = youngest_riders_frame.count()[0]
        print("The youngest riders were born in %s.  %s riders were born in that year." %(youngest_riders_birth_year, youngest_rider_count))

        oldest_riders_frame = df
        oldest_riders_frame.dropna(subset=['Birth_Year'])
        oldest_riders_birth_year = int(oldest_riders_frame['Birth_Year'].min())
        oldest_riders_frame = oldest_riders_frame.query("Birth_Year == %s" %(oldest_riders_birth_year), inplace = False)
        oldest_rider_count = oldest_riders_frame.count()[0]
        print("The oldest riders were born in %s.  %s riders were born in that year." %(oldest_riders_birth_year, oldest_rider_count))

        most_common_riders_frame = df
        most_common_riders_frame.dropna(subset=['Birth_Year'])
        most_common_birth_year = int(most_common_riders_frame['Birth_Year'].mode()[0])
        most_common_birth_year_frame = most_common_riders_frame.query("Birth_Year == %s" %(most_common_birth_year))
        most_common_birth_year_count = most_common_birth_year_frame.count()[0]
        print("The most common birth year is %s.  %s riders were born in that year." %(most_common_birth_year, most_common_birth_year_count))

    else:
        print("\nThe data you are analyzing does not have birth year data.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def getMaxRow(df):
    count_series = df.count()
    series_min = count_series.min()
    return series_min

def main():
    while True:
        city, month, day = get_filters()

        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        print_data = True
        start_row = 0
        end_row = 5
        max_row = getMaxRow(df)
        """
        Code for dropping columns was found at https://stackoverflow.com/questions/13411544/delete-column-from-pandas-dataframe
        in a post by LondonRob dated August 9th, 2013.
        """
        df.drop(['Start_Station','End_Station', 'month', 'year', 'day', 'weekday', 'End_Time', 'hour'], axis=1, inplace = True)

        """Code for putting dataframe data into a dictionary was found at
        https://stackoverflow.com/questions/26716616/convert-a-pandas-dataframe-to-a-dictionary
        in a post by Alex Riley dated November 3, 2014.
        """
        data_dict = df.to_dict(orient='records')

        first_run = True
        while print_data == True and end_row <= max_row:
            if first_run == True:
                show_data = input('\nWould you like to see individual records returned by your query? Enter Yes or No.\n')
                show_data = show_data.lower()
            else:
                show_data = input('\nWould you like to see more individual records returned by your query? Enter Yes or No.\n')
                show_data = show_data.lower()
            if show_data != 'yes' and show_data != 'no':
                print('Invalid input.')
                continue
            elif show_data == 'no':
                break
            else:
                output_dictionary = data_dict[start_row:end_row]
                for record in output_dictionary:
                    print(record)
                start_row = start_row + 5
                end_row = end_row + 5
                if end_row > max_row:
                    print('You have seen all the data returned by your query.')
                    break
                else:
                    first_run = False

        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() == 'yes':
                first_run = True
                main()
                break
            elif restart.lower() == 'no':
                break
            else:
                print('\nYour input was invalid. Please try again.')
        break


if __name__ == "__main__":
    main()
