import os
import random
import json
from datetime import datetime, timedelta, time
import sqlite3

# Directory containing images
image_directory = r'C:\Users\ahmed\Programming Valey\Content\Images'

# Function to list all image files in the specified directory
def list_images(directory):
    image_extensions = ('.png', '.jpeg', '.jpg', '.gif')
    return [f for f in os.listdir(directory) if f.lower().endswith(image_extensions)]

# Function to strip the number and extension from the image name
def strip_image_name(image_name):
    return os.path.splitext(image_name)[0].rsplit(' ', 1)[0]

# Function to save data to a JSON file
def save_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Function to load data from a JSON file
def load_data(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to load image titles from a text file
def load_image_titles(filename):
    image_titles = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if ':' in line:
                image, title = line.split(':', 1)
                image_titles[image.strip()] = title.strip()
    return image_titles

# Function to search for courses in the SQLite database
def search_courses(keyword):
    conn = sqlite3.connect('courses.db')
    cursor = conn.cursor()
    query = '''
    SELECT Title, Link, Rating, Number_of_Rater
    FROM courses
    WHERE Title LIKE ?
    ORDER BY Number_of_Rater DESC, Rating DESC
    LIMIT 10
    '''
    cursor.execute(query, ('%' + keyword + '%',))
    results = cursor.fetchall()
    conn.close()
    return [{"title": title, "link": link, "rating": rating, "number_of_rater": number_of_rater} for title, link, rating, number_of_rater in results]

# Function to generate the schedule
def generate_schedule(start_datetime, image_count, interval_hours=1):
    schedule = []
    current_time = start_datetime
    
    while len(schedule) < image_count:
        if time(12, 0) <= current_time.time() <= time(23, 0):
            schedule.append(current_time)
        current_time += timedelta(hours=interval_hours)
    
    return schedule

# Function to format date and time
def format_date_time(dt):
    formatted_date = dt.strftime('%m/%d/%Y').lstrip("0").replace("/0", "/")
    formatted_time = dt.strftime('%I:%M %p').lstrip("0")
    return formatted_date, formatted_time

# Function to create posts
def create_posts(start_date, start_time, filename='scheduled_posts.json'):
    start_datetime = datetime.combine(start_date, start_time)
    all_images = list_images(image_directory)
    used_images = load_data('used_images.json')
    image_titles = load_image_titles('image_titles.txt')
    available_images = [img for img in all_images if img not in used_images]
    image_count = len(all_images)

    schedule = generate_schedule(start_datetime, image_count)

    posts = []

    for post_time in schedule:
        if not available_images:
            available_images = all_images
            used_images = []

        selected_image = random.choice(available_images)
        stripped_name = strip_image_name(selected_image)
        recommended_courses = search_courses(stripped_name)
        hashtags = ["#Free", "#FreeCourses", "#courses", "#programming", f"#{stripped_name.replace(' ', '')}"]

        formatted_date, formatted_time = format_date_time(post_time)
        
        image_name = os.path.splitext(selected_image)[0]
        description = f"Check out our FREE certified Courses to learn {image_name} in 2024👇👇"

        post = {
            "Date": formatted_date,
            "Time": formatted_time,
            "Image Path": os.path.join(image_directory, selected_image),
            "Title": image_titles.get(selected_image, ""),  # Use the image title from the dictionary
            "Recommended Courses": recommended_courses,
            "Hashtags": hashtags,
            "Description": description
        }

        posts.append(post)
        used_images.append(selected_image)
        available_images.remove(selected_image)

    save_data(filename, posts)
    save_data('used_images.json', used_images)

    for post in posts:
        print(f"Scheduled date: {post['Date']}")
        print(f"Scheduled time: {post['Time']}")
        print(f"Image: {post['Image Path']}")
        print(f"Title: {post['Title']}")
        print("Recommended Courses:")
        for course in post["Recommended Courses"]:
            print(f" - {course['title']} ({course['link']})")
        print("Hashtags: " + " ".join(post["Hashtags"]))
        print(f"Description: {post['Description']}")
        print("\n")

# Example usage
if __name__ == "__main__":
    # Manually set the starting date and time
    start_date = datetime.strptime('2024-09-03', '%Y-%m-%d').date()  # Starting date
    start_time = datetime.strptime('1:00 PM', '%I:%M %p').time()    # Starting time
    create_posts(start_date, start_time)
