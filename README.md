[![Build Status](https://travis-ci.org/LeMayhem/nightlife.svg?branch=deploy)](https://travis-ci.org/LeMayhem/nightlife)

# Nightlife

## Welcome to Nightlife

Nightlife is a schedule of the week's outings, for people who love electronic music, build by an electronic music lover.
You can find all the popular events and artists, follow them to stay tuned and make friends before going out.

This project aims to use Django framework and Spotify API. This is a WIP, you can follow the building of new features on this repo.

## Installation

/!\ New dockerfile in progress   

1. Clone the repository:

    ```bash
    git clone https://github.com/lemayhem/nightlife.git
    cd nightlife
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv .env
    source .env/bin/activate
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply the migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

7. Access the application in your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000).


## Features

### Homepage

<img src="./src/mediafiles/readme/localhost_8000.png" width=30%>

You have access to:
- The 4 most populars events from current week (based on "ongoing" button)
- 4 most popular artists (based on "following" button)
- Latest events created
- The top 4 promoters

### Events
<img src="./src/mediafiles/readme/localhost_8000_events.png" width=30%>

Here you can discover and follow events. Promoters can sign up to create their own events to reach new people.   
Promoters can ask to feature their events.   
Events are regrouped by date   

<img src="./src/mediafiles/readme/localhost_8000_events_the-magician-album-tour.png" width=30%>

Members can discuss on every events to find friends to hangout with.

### Artists

<img src="./src/mediafiles/readme/localhost_8000_artists.png" width=30%>

You can check all the events your favorites artists are playing. You can follow them in order to keep you in touch.   
You can filter artists live, by using the search bar   
With Spotify API, you can do some actions:
- You can massively follow all the artists from your spotify to Nightlife.
- You can massively import all the artists from your Spotify to Nightlife (Admin)

<img src="./src/mediafiles/readme/localhost_8000_artists_amelie-lens.png" width=30%>

Members can discuss on every artists fan pages to meet other fans.

### Blog

<img src="./src/mediafiles/readme/localhost_8000_blog.png" width=30%>

Members can inform themselves with the blog part.  
Admin can create posts to feature events or artists, to be desplayed on home page.

<img src="./src/mediafiles/readme/localhost_8000_blog_the-magician.png" width=30%>

Members can also discuss on every blog posts.

### Search

<img src="./src/mediafiles/readme/localhost_8000_search.png" width=30%>

- You can search globally from the header's searchbar, which will search on Artists, events and blogposts
- You can filter by using searchbars on Artists, events and blogposts list pages

### Member page

<img src="./src/mediafiles/readme/localhost_8000_accounts_admin.png" width=30%>

- You can see the member/promoter page
- All the events from the promoter can be reach here

## WIP:
- Dockerise the app (In progress !)
- Build more interactions between Spotify API and Nightlife (Playlists, etc)
- Add Facebook login
- Add Soundcloud API
- Add notifications system (In progress !)
- More filters on list pages
- Footer


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Authors

- [Michael LEMAY](https://github.com/lemayhem)