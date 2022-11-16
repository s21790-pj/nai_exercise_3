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


def get_matching_results(users, data, choosen_user):
    """
        A function that counts the score for each user using
        euclidean and pearson algorithm
        :return: a score for each user from 1.0 to 0.0
     """
    pearsonScoreList = {}
    euclideanScoreList = {}
    for user in users:
        euclideanScoreList[user] = euclidean_score(data, choosen_user, user)
        pearsonScoreList[user] = pearson_score(data, choosen_user, user)
    pearsonScoreList = sorted(pearsonScoreList.items())
    euclideanScoreList = sorted(euclideanScoreList.items())
    return pearsonScoreList, euclideanScoreList


def get_movies_to_recommend(passed_user, match_user, data_json):
    """

    :param passed_user:
    :param match_user:
    :param data_json:
    """
    passed_user_movies = data_json[passed_user]
    match_user_movies = sorted(data_json[match_user].items(), key=lambda x: x[1], reverse=True)

    print(f"Recommended movies for user {passed_user}")
    counter = 0
    selected_movies = []
    for chosen_movie in match_user_movies:
        if chosen_movie not in passed_user_movies and counter < 5:
            selected_movies.append(chosen_movie)
            counter += 1
    for idx in range(len(selected_movies)):
        print(f"{idx + 1}. {selected_movies[idx]}\n")


def get_not_recommended_movies(passed_user, scores, data_json):
    """

    :param passed_user:
    :param scores:
    :param data_json:
    """
    passed_user_movies = data_json[passed_user]
    pass


def get_all_users(data_json):
    users = list(set(data_json.keys()))
    users.remove(user)
    return users


if __name__ == '__main__':
    """

    """
    args = build_arg_parser().parse_args()
    user = args.user

    with open('ratings.json', 'r', encoding='UTF8') as json_file:
        data = json.loads(json_file.read())

    all_users = get_all_users(data)

    get_movies_to_recommend('Szymon Olkiewicz', 'Paweł Czapiewski', data)
    get_matching_results(all_users, data, 'Szymon Olkiewicz')
