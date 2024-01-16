from letterboxdpy import user
import csv
import random

user_list = [] 

def meets_criteria(user_obj):
    diary_entries = user.user_diary(user_obj)
    follower_count = int(user_obj.stats.get("Followers", "0").replace(",", ""))
    following_count = int(user_obj.stats.get("Following", "0").replace(",", ""))

    return (
        len(diary_entries) >= 20
        and (5 < follower_count < 500)
        and (5 < following_count < 500)
    )
    
def write_csv(user_obj):
    username = user_obj.get_username()

    # Create a CSV file for the user
    csv_file_path = f"userdata/{username}_data.csv"

    # Get user data
    user_diary_data = user.user_diary(user_obj)
    user_reviews_data = user.user_reviews(user_obj)
    followers = user.user_followers(user_obj)
    following = user.user_following(user_obj)

    # Write data to CSV
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        csv_writer.writerow(['Movie', 'Date Watched', 'Rating', 'Liked', 'Review'])
        for film in user_diary_data:
            movie_title = film['movie']
            date_watched = film['date']
            rating = film['rating']
            liked = film['liked']
            # Check if there's a review in user_reviews_data for the same movie
            review = next((entry['review'] for entry in user_reviews_data if entry['movie'] == movie_title), '')
            csv_writer.writerow([movie_title, date_watched, rating, liked, review])

        # Write follower and following data
        csv_writer.writerow([])  # Add an empty line for better readability
        csv_writer.writerow(['Followers'])
        csv_writer.writerow(followers)
        csv_writer.writerow([])  # Add an empty line for better readability
        csv_writer.writerow(['Following'])
        csv_writer.writerow(following)

    print(f"CSV file created for {username}: {csv_file_path}")

nathan = user.User("nathancheng")
write_csv(nathan)
user_list.append(nathan)

while len(user_list) < 1000:
    for lbx_person in user_list:
        followers = user.user_followers(lbx_person)
        random.shuffle(followers)
        for username in followers:
            if username not in [person.get_username() for person in user_list]:
                try:
                    lbx_sub_person = user.User(username)
                    if meets_criteria(lbx_sub_person):
                        write_csv(lbx_sub_person)
                        user_list.append(lbx_sub_person)
                    else:
                        continue
                except Exception as e:
                    print(f"Error processing user {username}: {e}")