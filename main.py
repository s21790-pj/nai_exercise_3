import argparse
import json
import numpy as np


def build_arg_parser():
    """

    :return:
    """
    parser = argparse.ArgumentParser(description='Compute similarity score')
    parser.add_argument('--user', dest='user', required=True, help='Name of user')
    return parser


def euclidean_score(dataset, user1, user2):
    """
    This method calculating distance score between users1 and users2 based on provided date.

    :param dataset:
    :param user1:
    :param user2:
    :return:
    """
    if user1 not in dataset:
        raise TypeError('Cannot find ' + user1 + ' in the dataset')

    if user2 not in dataset:
        raise TypeError('Cannot find ' + user2 + ' in the dataset')

    # Movies rated by both user1 and user2
    common_movies = {}

    for item in dataset[user1]:
        if item in dataset[user2]:
            common_movies[item] = 1

    # If there are no common movies between the users,
    # then the score is 0
    if len(common_movies) == 0:
        return 0

    squared_diff = []

    for item in dataset[user1]:
        if item in dataset[user2]:
            squared_diff.append(np.square(dataset[user1][item] - dataset[user2][item]))

    return 1 / (1 + np.sqrt(np.sum(squared_diff)))


def pearson_score(dataset, user1, user2):
    """
    This method calculating Pearson correlation score between users1 and users2 based on provided date.

    :param dataset:
    :param user1:
    :param user2:
    :return:
    """
    if user1 not in dataset:
        raise TypeError('Cannot find ' + user1 + ' in the dataset')

    if user2 not in dataset:
        raise TypeError('Cannot find ' + user2 + ' in the dataset')

    # Movies rated by both user1 and user2
    common_movies = {}

    for item in dataset[user1]:
        if item in dataset[user2]:
            common_movies[item] = 1

    num_ratings = len(common_movies)

    # If there are no common movies between user1 and user2, then the score is 0
    if num_ratings == 0:
        return 0

    # Calculate the sum of ratings of all the common movies
    user1_sum = np.sum([dataset[user1][item] for item in common_movies])
    user2_sum = np.sum([dataset[user2][item] for item in common_movies])

    # Calculate the sum of squares of ratings of all the common movies
    user1_squared_sum = np.sum([np.square(dataset[user1][item]) for item in common_movies])
    user2_squared_sum = np.sum([np.square(dataset[user2][item]) for item in common_movies])

    # Calculate the sum of products of the ratings of the common movies
    sum_of_products = np.sum([dataset[user1][item] * dataset[user2][item] for item in common_movies])

    # Calculate the Pearson correlation score
    Sxy = sum_of_products - (user1_sum * user2_sum / num_ratings)
    Sxx = user1_squared_sum - np.square(user1_sum) / num_ratings
    Syy = user2_squared_sum - np.square(user2_sum) / num_ratings

    if Sxx * Syy == 0:
        return 0

    return Sxy / np.sqrt(Sxx * Syy)


def get_matching_results(users, data_json, choosen_user):
    """
        A function that counts the score for each user using
        euclidean and pearson algorithm
        :return: a score for each user from 1.0 to 0.0
     """
    pearson_score_list = {}
    euclidean_score_list = {}

    for user in users:
        euclidean_score_list[user] = euclidean_score(data_json, choosen_user, user)
        pearson_score_list[user] = pearson_score(data_json, choosen_user, user)

    pearson_score_list = sorted(pearson_score_list.items(), key=lambda x: x[1], reverse=True)
    euclidean_score_list = sorted(euclidean_score_list.items(), key=lambda x: x[1], reverse=True)
    return pearson_score_list, euclidean_score_list


def get_movies_to_recommend(passed_user, match_user, data_json):
    """
    function which sorts movie list

    :param passed_user:
    :param match_user:
    :param data_json:
    """
    passed_user_movies = data_json[passed_user]
    match_user_movies = sorted(data_json[match_user].items(), key=lambda x: x[1], reverse=True)

    print(f"Recommended movies for user {passed_user}")
    show_movies_list(match_user_movies, passed_user_movies)


def get_not_recommended_movies(passed_user, scores, data_json):
    """

    Function which take 3 matching users movie list.

    :param passed_user:
    :param scores:
    :param data_json:
    """
    passed_user_movies = data_json[passed_user]
    not_recommended_movies = data_json[scores[2][0]]
    not_recommended_movies.update(data_json[scores[1][0]])
    not_recommended_movies.update(data_json[scores[0][0]])
    not_recommended_movies = sorted(not_recommended_movies.items(), key=lambda x: x[1], reverse=False)

    print(f"Not recommended movies for user {passed_user}")
    show_movies_list(not_recommended_movies, passed_user_movies)


def show_movies_list(movie_list, passed_user_movie_list):
    counter = 0
    selected_movies = []
    for chosen_movie in movie_list:
        if chosen_movie[0] not in passed_user_movie_list.keys() and counter < 5:
            selected_movies.append(chosen_movie)
            counter += 1
    for idx in range(len(selected_movies)):
        print(f"{idx + 1}. {selected_movies[idx]}")


def get_all_users(data_json):
    """
    Function returning list of users.

    :param data_json:
    :return:
    """
    users = list(set(data_json.keys()))
    users.remove(user)
    return users


if __name__ == '__main__':
    """

    """
    args = build_arg_parser().parse_args()
    user = args.user

    with open('ratings.json', 'r', encoding='UTF8') as json_file:
        data_json = json.loads(json_file.read())

    all_users = get_all_users(data_json)
    pearson_score_list, euclidean_score_list = get_matching_results(all_users, data_json, user)
    print("Pearson results")
    print(f"The best match for user {user} is {pearson_score_list[0][0]} with score {pearson_score_list[0][1]}")
    get_movies_to_recommend(user, pearson_score_list[0][0], data_json)
    get_not_recommended_movies(user, pearson_score_list, data_json)
    print("\nEuclidean results")
    print(f"The best match for user {user} is {euclidean_score_list[0][0]} with score {euclidean_score_list[0][1]}")
    get_movies_to_recommend(user, euclidean_score_list[0][0], data_json)
    get_not_recommended_movies(user, euclidean_score_list, data_json)