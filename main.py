# -*- coding: utf-8 -*-
import vk, os, time, sys, codecs

class EncodedOut:
    def __init__(self, enc):
        self.enc = enc
        self.stdout = sys.stdout
    def __enter__(self):
        if sys.stdout.encoding is None:
            w = codecs.getwriter(self.enc)
            sys.stdout = w(sys.stdout)
    def __exit__(self, exc_ty, exc_val, tb):
        sys.stdout = self.stdout

if os.path.exists('result.txt'):
    os.remove('result.txt')
    result = open('result.txt', 'w')
else:
    result = open('result.txt', 'w')
result.write("Анализатор популярности страниц v0.1 \n1 лайк = 1 очко, 1 репост = 2 очка \n \n===================================\n")
result.close()
token=''
session = vk.AuthSession(access_token=token)
api = vk.API(session)

id = input("Enter page id: ")
print("Getting Friends List...")
friends = api.friends.get(user_id = id, order = "random")
friendscount = len(friends)
friendslist = dict()
i = 0
os.system("cls")
while(i < friendscount):
    print("Processing friend...[{}/{}]".format(i,friendscount))
    info = api.users.get(user_id = friends[i], fields = "deactivated")
    if "deactivated" in info[0]:
        i += 1
    else:
        name = (info[0]["first_name"] + " " + info[0]["last_name"])
        name = name.replace(u'\u0456', u'i').replace(u'\u9ed2', u'unknown').replace(u'\u661f', u'unknown')
        friendslist[friends[i]] = name
    with EncodedOut('utf-8'):
        print(name)
    i += 1
    time.sleep(0.4)
    os.system("cls")
i = 0
print("Processing friend {}/{}...[Done!]".format(friendscount, friendscount))
while (i < friendscount):
    wallpostinf = api.wall.get(owner_id = friends[i], count = 1, filter = "owner")
    postscount = wallpostinf[0]
    ii = 0
    points = 0
    likes = 0
    reposts = 0
    while (ii < postscount):
        print("Processing walls posts of {}...[{}/{}]".format(friendslist[friends[i]], i, friendscount))
        print("Processing posts...[{}/{}]".format(ii, postscount))
        wallpost = api.wall.get(owner_id = friends[i], ofset = ii, count = 100, filter = "owner")
        iii = 1
        process = 0
        if (postscount > 101):
            process = 101
        else: 
            process = postscount
        while(iii < process):
            likes += wallpost[iii]['likes']['count']
            reposts += wallpost[iii]['reposts']['count']
            points = likes + (reposts*2)
            iii += 1
        time.sleep(0.4)
        os.system("cls")
        ii += 100
    result = open('result.txt', 'a')
    result.write("{}, {} posts, likes = {}, reposts = {}, total points = {}\n".format(friendslist[friends[i]], postscount, likes, reposts, points))
    result.close()
    time.sleep(0.4)
    i += 1
    os.system("cls")
result.close()
print("You looks great today! See results in result.txt ;)")
