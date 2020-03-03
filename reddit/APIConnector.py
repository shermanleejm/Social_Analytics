import praw 
import pandas as pd
import matplotlib.pyplot as plt 

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
    "https://www.reddit.com/r/singapore/comments/apr4aw/would_you_recommend_reserving_a_space_at_a_local/",
    "https://www.reddit.com/r/singapore/comments/albo22/current_student_and_alumni_of_smu_what_do_you/",
    "https://www.reddit.com/r/singapore/comments/83dh8h/anyone_willing_to_shed_some_light_on_nussmu/",
    "https://www.reddit.com/r/singapore/comments/8er108/what_are_your_views_about_smu/"
]

d
post = reddit.submission("65w4jb")

for comment in post.comments:
    print (comment.author)
    print (comment.body)
    print (comment.replies.list())
    print ("--------------------")
