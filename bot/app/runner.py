import random

from app.config import NUMBER_OF_USERS, MAX_LIKES_PER_USER, MAX_POSTS_PER_USER
from app.bot import Bot
from app.user import User

bot = Bot()
users = []
posts = []
likes = []


def run():

    global users, posts, likes

    print('STAGE: user creation')

    while len(users) < NUMBER_OF_USERS:

        userdata = bot.generate_userdata()
        data = bot.create_user(userdata).json()
        auth_data = bot.login_user(userdata).json()
        user = User(userdata | data, auth_data.get('token'))
        users += [user]
        print(user.data)

    print('-'*50)

    print('STAGE: posts creation')

    for user in users:
        user_posts = []
        num_posts = random.randint(1, MAX_POSTS_PER_USER)
        while len(user_posts) < num_posts:
            post = bot.generate_post()
            post = bot.add_post(user, post).json()
            user_posts.append(post)
            print(post)
        posts += user_posts

    print('-'*50)

    print('STAGE: likes creation')

    num_users_likes_activity = random.randint(1, NUMBER_OF_USERS)
    for _ in range(num_users_likes_activity):
        num_likes = random.randint(0, MAX_LIKES_PER_USER)
        user = random.choice(users)
        user_likes = []
        while len(user_likes) < num_likes:
            post = random.choice(posts)
            like = bot.like_post(user, post['id'])
            like = like.json() | {'user': user.data, 'post': post}
            user_likes += [like]
            print(like)
        likes += user_likes

    print('-'*50)

