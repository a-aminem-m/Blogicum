# Blogicum

###### (This project was developed during the "Python Developer" training program at [Yandex.Practicum](https://practicum.yandex.ru/), as a part of the learning curriculum).

Blogiсum is a social network designed for publishing personal diaries. Users can create their own pages and share posts categorized into topics such as **travel**, **culinary**, or **python development**. Additionally, users can optionally associate a location with each post, enhancing the overall user experience.

## Project Structure

The project comprises two registered applications:

1. **Pages App**: Responsible for handling static pages within the project.

2. **Blog App**: Manages user-generated posts, categories, and locations.

## Implemented Features

1. **Admin Zone Setup**: Configured the admin zone to manage the creation, modification, and deletion of model objects:

    - Category
    - Location
    - Post

2. **Custom Error Pages**: Created custom error pages to enhance user experience.

3. **User Authentication**: Integrated user authentication to enable user registration and login functionalities.

## How Blogiсum Works

The core element of Blogiсum is the publication or **post**. Each post has the following attributes:

- Title of the post.
- Main text content.
- Publication date. Authors can set any date, even future ones.
- Date added to the database.
- **Published** flag.
- Author: A registered user on the platform. Superusers can also add authors.
- Location: A specific location associated with the post. The location can be left unspecified, in which case, the template displays **Planet Earth**.
- Category: A collection that groups posts based on a specific theme.

## Current Progress

Here's what has already been accomplished:

- Created and registered applications: **pages** for static pages and **blog** for user-generated posts.
- Configured the admin zone for managing categories, locations, and posts.
- Established custom error pages for a polished user experience.
- Integrated user authentication for registration and login.
  
## Working Logic

- A post cannot be added without specifying at least one category.
- Specifying a location for a post is optional.
- Site administrators can remove any post, category, or location.
- A post is displayed on the site pages if it meets the following criteria:
    - Publication date is not later than the current time.
    - The post is marked as "published."
    - The category to which it belongs is still published.

    The publication status of a location does not affect the display of posts associated with it.

## Getting Started

Follow these steps to set up and run the project locally:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/django_sprint4.git
   cd blogiсum
   ```

2. Create and activate a virtual environment:

    **Windows:**

    ```bash
    python -m venv venv
    source venv/Scripts/activate
    ```

    **Linux/macOS:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Upgrade PIP:

    **Windows:**

    ```bash
    python -m pip install --upgrade pip
    ```

    **Linux/macOS:**

    ```bash
    python3 -m pip install --upgrade pip
    ```

4. Install dependencies from the requirements.txt file:

    ```bash
    pip install -r requirements.txt
    ```

5. Perform migrations:

    **Windows:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

    **Linux/macOS:**

    ```bash
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```

6. Run the project:

    **Windows:**

    ```bash
    python manage.py runserver
    ```

    **Linux/macOS:**

    ```bash
    python3 manage.py runserver
    ```

8. **Access the Application:**

   Open your web browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the project.

9. **Create Your First Post:**

   - Log in with the superuser credentials created earlier.
   - Navigate to the admin interface [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).
   - Add a new post, category, and location if desired.

10. **Explore and Interact:**

    - Visit the homepage and explore different categories.
    - Create your own user account to publish personal posts.
    - Read, comment, and interact with posts from other users.

Feel free to reach out if you have any questions, feedback, or need further assistance. Happy blogging! 📖✨

