import praw 
import pandas as pd
import matplotlib.pyplot as plt 
import pprint 
pp = pprint.PrettyPrinter(indent=2)
import json

reddit = praw.Reddit(
    client_id='qB2zYopSCvIXVQ',
    client_secret='HS_uLyox1i_ULUlqNiB-rCINduI',
    user_agent='social_analytics_scraper',
    username='noshiteinstein',
    password='Password1!'
)

posts = [
    "https://www.reddit.com/r/singapore/comments/65w4jb/need_help_with_choosing_between_nus_is_and_smu_sis/",
    "https://www.reddit.com/r/singapore/comments/b7zj6r/smu_interview/",
    "https://www.reddit.com/r/singapore/comments/b4v56k/is_it_really_worth_the_4_years_to_obtain_a_degree/",
    "https://www.reddit.com/r/singapore/comments/b03568/smu_admissions_2019/",
    "https://www.reddit.com/r/singapore/comments/69qpkf/degree_in_information_systems/",
    "https://www.reddit.com/r/SGExams/comments/bju38y/uni_how_is_the_culture_and_community_like_in_smu/?utm_source=share&utm_medium=ios_app",
    "https://www.reddit.com/r/singapore/comments/awfvxk/screwed_up_alevels_looking_for_advice/",
    "https://www.reddit.com/r/singapore/comments/albo22/current_student_and_alumni_of_smu_what_do_you/",
    "https://www.reddit.com/r/singapore/comments/83dh8h/anyone_willing_to_shed_some_light_on_nussmu/",
    "https://www.reddit.com/r/singapore/comments/8er108/what_are_your_views_about_smu/"
]

# def extractAuthorAndBody(commentObject) :
#     output = [str(commentObject.author), commentObject.body] # author, comment
#     replies = []
#     reply_queue = commentObject.replies[:]
#     while reply_queue :
#         temp = reply_queue.pop(0)
#         temp_arr = [str(temp.author), temp.body]
#         replies.append(temp_arr)
#     output.append()
#     return output

def recAuthorBody(commentObject) :
    replies = []
    
    if commentObject.replies :
        for reply in commentObject.replies[:]:
            replies.append(recAuthorBody(reply))
    if replies != []:
        return [ str(commentObject.author), commentObject.body, replies ]
    else:
        return [ str(commentObject.author), commentObject.body ]

def getAllComments(commentObject) :
    if commentObject.replies :
        for reply in commentObject.replies[:]:
            replies.append(recAuthorBody(reply))
    # if replies != []:
    #     return [ str(commentObject.author), commentObject.body, replies ]
    # else:
    #     return [ str(commentObject.author), commentObject.body ]

AuthorBodyReplies = []

# post = reddit.submission("https://www.reddit.com/r/singapore/comments/65w4jb/need_help_with_choosing_between_nus_is_and_smu_sis/")
# print ( type(post.comments) )
# for comment in post.comments:
#     AuthorBodyReplies.append(recAuthorBody(comment))

counter = 0
for url in posts:
    urlid = url.split("/")[6]
    post = reddit.submission(urlid)
    # print ( type(post.comments) )
    for comment in post.comments:
        AuthorBodyReplies.append(recAuthorBody(comment))
    counter += 1
    print (counter)

pp.pprint(AuthorBodyReplies)

with open("redditComments.json", "w+") as outfile:
    json.dump( AuthorBodyReplies, outfile )

result = {
    "author" : [],
    "message" : [],
    "timestamp" : [],
}

