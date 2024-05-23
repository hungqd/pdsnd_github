import time
import pandas as pd

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}

ALL_MONTHS = [
    "all",
    "january",
    "febraury",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
]

ALL_WEEKDAYS = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
    "all",
]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")

    city = None
    month = None
    day = None

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city not in ["chicago", "new york city", "washington"]:
        city = input("Please enter Chicago, Washington or New York City for your analysis: ").strip().lower()

    # get user input for month (all, january, february, ... , june)
    while month not in ALL_MONTHS:
        month = input("Enter any one of the first 6 months or enter All to select all 6 months: ").strip().lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in ALL_WEEKDAYS:
        day = input("Please enter day of week: ").strip().lower()

    print("-" * 40)
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
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.weekday
    df["hour"] = df["Start Time"].dt.hour

    if month != "all":
        idx = ALL_MONTHS.index(month)
        df = df[df["month"] == idx]

    if day != "all":
        idx = ALL_WEEKDAYS.index(day)
        df = df[df["day_of_week"] == idx]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # display the most common month
    most_common_month = ALL_MONTHS[df["month"].mode()[0]]
    print(f"Most common month: {most_common_month}")

    # display the most common day of week
    most_common_day_of_week = ALL_WEEKDAYS[df["day_of_week"].mode()[0]]
    print(f"Most common day of week: {most_common_day_of_week}")

    # display the most common start hour
    most_common_start_hour = df["hour"].mode()[0]
    print(f"Most common start hour: {most_common_start_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    start_station = df["Start Station"].mode()[0]
    print(f"Most common start station: {start_station}")

    # display most commonly used end station
    end_station = df["End Station"].mode()[0]
    print(f"Most common end station: {end_station}")

    # display most frequent combination of start station and end station trip
    combination = df[["Start Station", "End Station"]].agg(" - ".join, axis=1).mode()[0]
    print(
        f"Most frequent combination of start station and end station trip: {combination}"
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print(f"Total travel time: {total_travel_time} hours")

    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print(f"Mean travel time: {mean_travel_time} hours")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types")
    counts_of_user_types = df["User Type"].value_counts()
    for k in counts_of_user_types.keys():
        print(f"- {k}: {counts_of_user_types[k]}")

    # Display counts of gender
    if "Gender" in df.columns:
        print("Genders counts:")
        counts_of_gender = df["Gender"].value_counts()
        for k in counts_of_gender.keys():
            print(f"- {k}: {counts_of_gender[k]}")

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        min_yob = int(df["Birth Year"].min())
        print(f"Earliest year of birth: {min_yob}")
        max_yob = int(df["Birth Year"].max())
        print(f"Most recent year of birth: {max_yob}")
        common_yob = int(df["Birth Year"].mode()[0])
        print(f"Most common year of birth: {common_yob}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def ask_for_confirmation(message) -> bool:
    """
    Ask user to confirm 'Yes' or 'No'
    
    Returns: True if user answered 'Yes', False if user answered 'No'.
    """

    while True:
        restart = input(message).strip().lower()
        if restart not in ["yes", "no"]:
            print("Invalid input!")
        elif restart != "yes":
            return False
        else:
            return True


def show_raw_data(df):
    """Ask user if they would like to see raw data."""

    batch_size = 5
    data_size = df.size
    start_index = 0

    while start_index + batch_size < data_size:
        if not ask_for_confirmation("Would you like to see some raw data (yes/no): "):
            break
        else:
            print(df.iloc[start_index : start_index + batch_size])
            start_index += batch_size

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.size > 0:
            show_raw_data(df)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        else:
            print("There is no data for your query")

        if not ask_for_confirmation("Would you like to restart? Enter yes or no: "):
            break


if __name__ == "__main__":
    main()
