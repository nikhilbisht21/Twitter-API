
# coding: utf-8

# # Twitter Search/Streaming API
# 
# 
# This API is for fetching and storing the target tweets with metadata(e.g. modi,AbkiBarModiSarkar,ModiForPM etc)
# ### Objectives
# <ul>
# <li>Trigger a twitter search/stream for recent high traffic events.
# 
#     </li>
# <li> 
#     Return stored tweets and their metadata based on applied filters/search.
#     </li>
#     <li> 
#     Export data to csv file
#     </li>
# </ul>
# 
# #### Basic structure diagram of API
# <img src='twitter.png'>
# 
# ### Specifications
# #### Programming language : Python
# #### Database : MongoDB(NoSQL Database)
# #### Data fetching method : Searching and Streaming
# 
# ### Prerequisite
# #### Python modules
# <ul>
#     <li>python-twitter</li>
#     <li>pymongo</li>
#     </ul>
#     
# #### Twitter authetication keys
# In order to fetch the data from twitter we have to send a connection request to twitter servers with header. 
# This header contains authetication parameters which are basically authetication tokens provided by twitter.
# Following keys are needed in order to use the api:
# <ul>
#     <li>consumer_key</li>
#     <li>access_token_key</li>
#     <li>consumer_secret</li>
#     <li>access_token_secret</li>
# </ul>
# 
# #### MongoDB
# There are two ways to work on mongoDB, either it could be installed directly in our local system or use the free cloud database service.A URI is needed in case free cloud database is used.<br>
# See resources for further details.
# 
#  
# 
# 
# 
#     
# # API Functions
# 
# <ul>
#     <li>configure()</li>
#     <li>exportFilter()</li>
#     <li>exportToCSV()</li>
#     <li>filterDateTime()</li>
#     <li>filterTweets()</li>
#     <li>initialize()</li>
#     <li>search()</li>
#     <li>searchTweets()</li>
#     <li>sortTweets()</li>
#     <li>streamTweets()</li>
#     <li>verify()</li>
#     <li>viewBook()</li>   
#     </ul>
#     
# # Getting Started
# 
# 
# <b>1.</b> Import twitter_api as tap<br>
# <b>2.</b> tap.configure(<b>consumer_key</b>='consumer_key',<b>access_token_key</b>='access_token_key',<b>tap.consumer_secret</b>='consumer_secret',
# <b>tap.access_token_secret</b>='access_token_secret',<b>uri</b>='uri')
# <br><b>3.</b> tap.initialize()
# <br><b>4.</b> tap.searchTweets(keywords=['modi','AbkiBarModiSarkar','ModiForPM'],deliminiter='or',count=1000)
#     <b>OR</b> tap.streamTweets(keywords=['modi','AbkiBarModiSarkar','ModiForPM'],deliminiter='or',count=1000)
#  #### Now api is ready to be use. For further details check documentation and references.
# 
# 
# ### References
# Standard Searching https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets<br>
# Stream Filtering  https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters<br>
# Introduction to Tweet JSON https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/intro-to-tweet-json<br>
# Tweet data dictionaries https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object<br>
# Link to get application tokens https://apps.twitter.com/<br>
# Guide to get application tokens https://github.com/bear/python-twitter/blob/master/doc/getting_started.rst<br>
# Link to the guide to get URI https://docs.mongodb.com/manual/tutorial/atlas-free-tier-setup/<br>
# Download link to monogoBD https://www.mongodb.com/download-center

# In[1]:


import twitter
import pymongo
import pprint as pp
import csv,json


# In[2]:


#Intializing the parameters for percent_encode

def par():
    """
    par()
    
    Intializes global variable "a" which is used by percent_encode() in string encoding w.r.t twitter standards
    """
    
    global a,mon
    
    a=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    
    a.append('_')
    a.append('.')
    a.append('~')
    a.append('-')
    
    mon={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
    


# In[3]:


#Percent Encode Function to encode strings

def percent_encode(code):
    """
    percent_encode(code)
    
    Returns an encoded string according to twitter standards, used while sending search query and getting data from twitter database
    
    parameters:
    1.code(string)
    
    returns:
    An encoded string w.r.t to twitter standards
    """
    
    tmp=""
    for vb in code:
        if vb not in a:
            #print(vb)
            b=hex(ord(vb)).split('x')
            b=b[len(b)-1].upper()
            tmp+='%{}'.format(b)
        else:
            tmp+=vb
            
    return tmp


# In[6]:


#Extracting the data from tweet for collection


def extract(tweet):
    """
    extract(tweet)
    
    This function extract the details from a single tweet i.e. a dictionary object and stores the minimal details of tweet in...
    ..dictionary named as data.
    
    parameters:
    1.tweet(dictionary):
        This dictonary contains a single tweet data
    
    returns:
    1.data
        Dictionary with minimal detais of a single tweet
    2.user
        Dictionary with minimal details of tweet's user

    """
    
    try:
        data={}
        data['tweet_id']=tweet['id_str']
    
        tmp=tweet['created_at'].split(' ')
        date='{0} {1} {2}'.format(tmp[5],mon[tmp[1]],tmp[2])
        time=tmp[3]
        day=tmp[0]
        data['created_at']={
        'date':date,
        'time':time,
        'day':day
        }
        data['lang']=tweet['lang']
        data['retweet_count']=tweet['retweet_count']
        data['retweeted']=tweet['retweeted']
        data['favorite_count']=tweet['favorite_count']
        data['favorited']=tweet['favorited']
        data['quote_status']=tweet['is_quote_status']
        data['place']=tweet['place']
        data['text']=tweet['text']
        data['truncated']=tweet['truncated']
        data['source']=tweet['source'].split('>')[1].split('<')[0]
        data['user_id']=tweet['user']['id_str']
    
        if tweet['in_reply_to_status_id_str']:
            data['is_reply']=True
        else:
            data['is_reply']=False
        
        data['reply_to']={
            "status_id":tweet['in_reply_to_status_id_str'],
            "user_id":tweet['in_reply_to_user_id_str'],
            "user_screen_name":tweet['in_reply_to_screen_name']
        }
    
        if 'retweeted' in tweet.keys():
            data['retweeted']=False
        else:
            data['retweeted']=True
            
        data['urls']=[]
    
        if len(tweet['entities']['urls']) is not 0:
            for va in range(len(tweet['entities']['urls'])):
                data['urls'].append(tweet['entities']['urls'][va]['expanded_url'])
            
        data['mentions']=[]
    
        if len(tweet['entities']['user_mentions']) is not 0:
            for va in range(len(tweet['entities']['user_mentions'])):
                tmp=tweet['entities']['user_mentions'][va]
                data['mentions'].append({'user_id':tmp['id_str'],
                                 'name':tmp['name'],
                                'screen_name':tmp['screen_name']})
            
        data['hashtags']=[]
    
        if len(tweet['entities']['hashtags']) is not 0:
            for va in range(len(tweet['entities']['hashtags'])):
                data['hashtags'].append('#{0}'.format(tweet['entities']['hashtags'][va]['text']))
            
        data['media_status']=False
        data['media']=[]
    
    
        if 'media' in tweet['entities'].keys():
            data['media_status']=True
            for va in range(len(tweet['entities']['media'])):
                data['media'].append({
                    'id':tweet['entities']['media'][va]['id_str'],
                    'type':tweet['entities']['media'][va]['type'],
                    'url':tweet['entities']['media'][va]['media_url'],
                'url_https':tweet['entities']['media'][va]['media_url_https']})   
    
        if 'extended_entities' in tweet.keys():
            data['media_status']=True
            for va in range(len(tweet['extended_entities']['media'])):
                data['media'].append({
                    'id':tweet['extended_entities']['media'][va]['id_str'],
                    'type':tweet['extended_entities']['media'][va]['type'],
                    'url':tweet['extended_entities']['media'][va]['media_url'],
                    'url_https':tweet['extended_entities']['media'][va]['media_url_https']})
            
    
        user={}
        user['id']=tweet['user']['id_str']
        user['name']=tweet['user']['name']
        user['screen_name']=tweet['user']['screen_name']
        user['profile_link']=tweet['user']['url']
        user['location']=tweet['user']['location']
        user['lang']=tweet['user']['lang']
        user['description']=tweet['user']['description']
        user['followers_count']=tweet['user']['followers_count']
        user['friends_count']=tweet['user']['friends_count']
        user['favourites_count']=tweet['user']['favourites_count']
        user['verified']=tweet['user']['verified']
        user['listed_count']=tweet['user']['listed_count']
        user['profile_background_image_url']=tweet['user']['profile_background_image_url']
        user['profile_background_image_url_https']=tweet['user']['profile_background_image_url_https']
        user['profile_image_url']=tweet['user']['profile_image_url']
        user['profile_image_url_https']=tweet['user']['profile_image_url_https']
        
    except:
        print('An unexpected error occured')
    
    return data,user


# In[7]:


#Adding tweet and user records to database


def add_document(db,data,user):
    """
    add_document(db,data,user)
    
    This function add a tweet to database.
    The tweet is divided into two subparts to remove redundancy in database.
    Subparts of a single tweet:
        1.tweet:
            It has the details related to tweet only
        2.user:
            It has the details about the user of the tweet
        tweet,user are saved in different collections in database
        
    parameters:
    1.db:
        Instance of the database
    2.data:
        Dictionary with the information about tweet
    3.user:
        Dictionary with the information about tweet's user
    returns:
    An integer value denoting success and failure of adding document to database
    
    """
    
    resa=None
    resb=None
    
    try:
        count=db.tweets.find({'tweet_id':data['tweet_id']}).count()
        if count is 0:
            resa=db.tweets.insert_one(data)
            #print(resa.inserted_id)
    
        count=db.users.find({'id':user['id']}).count()
        if count is 0:
            resb=db.users.insert_one(user)
            #print(res.inserted_id)
        
        if resa:
            return 1
        else:
            return 0
    except:
        return 0
    


# In[338]:


#Class to return paginated tweets

class tweetBook:
    """
    tweet class
    
    tweet class is used to implement pagination of the inforamtion retrieved  from database
    
    data members:
    1.pages(int):
        No. of pages in the dictionary(Calculated as total total tweets/tweets per page)
    2.data(list):
        List to store the records retrieved from database.
        Index of list acts as pages for records
    3.pointer(int):
        Points to the current page of the records
    
    member functions:
    1.__init__(self):
        Constructor 
    2.def assign(self,data,num):
        Add limited tweets in a single index of list resulting as a page of records
    3.def next(self):
        This function increment the pointer thus moving to next page of record
    4.def previous(self):
        This function decrement the pointer thus moving to previous page of record
    
    """
    
    pages=0
    data=[]
    pointer=0
    
    def _init_(self):
        self.pages=0
        self.pointer=0
    
    def assign(self,data,num):
        
        self.pages=self.pages+1
        tmp={'tweets':data[0:num],'meta':{'page no':self.pages,'total tweets':num}}
        self.data.append(tmp)
        
    def next(self):
        if self.pointer!=self.pages:   
            self.pointer=self.pointer+1  
        return self.data[self.pointer-1]
        #print(self.pointer)
    
    def previous(self):
        if self.pointer!=1:   
            self.pointer=self.pointer-1
        
        if self.pointer is -1:
            self.pointer=self.pages
            
        return self.data[self.pointer-1]
        #print(self.pointer)
        
    def update_meta(self):
        for va in self.data:
            va['meta']['total pages']=self.pages

#ob=tweetBook()
#ob.next()
#ob.previous()


# In[23]:


#collect user details


def get_user(db,id):
    """
    get_user(db,id)
    
    This function returns the user details for a single tweet by fetching user document from database 
    
    parameters:
    1.db:
        Instance of database
    2.id
        userid to be matched in the database to get user information
        
    returns:
    A dictionary containing details of the user
    """
    usr=db.users.find({'id':str(id)},{'_id':0})
    return next(usr)


# In[286]:


#collect tweet details

def get_tweet(db,id):
    """
    get_tweet(db,id)
    
    This function returns the tweet details for a single user by fetching tweet document from database 
    
    parameters:
    1.db:
        Instance of database
    2.id
        tweet_id to be matched in the database to get user information
        
    returns:
    A dictionary containing details of the tweets by user
    """
    twt=db.tweets.find({'user_id':str(id)},{'_id':0})
    
    data=[]
    for va in twt:
        data.append(va)
        
    return data


# In[288]:


#Generating tweet pages

def gen_pages(db,twts,limit=32):
    """
    gen_pages(db,twts,limit=32)
    
    This function is used to implement pagination to the records fetched from the database.
    It uses tweet class to form a book like data structure providing with pages.
    
    parameters
    1.db:
        Instance of the database
    2.twts(dictionary):
        Tweet records fetched from the database
    2.limit(int)
        No. of tweets per page
        
    returns:
    An object of tweet class
    Operations which be perfored on this object
    next():
        Goto next page of tweet book
    previous():
        Goto previous page of tweet book  
    """
    
    i=0
    data=[]

    ob=tweetBook()

    for dat in twts:
        
        tmp=get_user(db,dat['user_id'])
        dat['user']=tmp
        
        if i==limit:
            ob.assign(data,limit)
            data.clear()
            data.append(dat)
            i=1
        else:
            data.append(dat)
            i=i+1

    if i>=1:
        ob.assign(data,i)
        data.clear()
        
    ob.update_meta()
    
    return ob
        


# In[6]:


#Making Connection to NoSQL Database


def database():
    """
    database()
    
    This function intialize the global instance of the database
    
    Database: monoDB
    Database name: twitter
    Collection Names: tweets,user
    url: Link of the online database of mongoDB
    
    Note: To run mongoDB from localhost don't pass any parameter to MongoClient()
    """
    try:
        url=None
        global db
        
        data=json.load(open('twitter.json'))
        url=data['uri']
        
        if url is '':
            url=None
        
        client = pymongo.MongoClient(url)

        #Create an object to Connect or create new database(Here database name is "twitter" )
        db=client.twitter

        #Check status
        status=db.command("serverStatus")
            
    except:
        print('Error in creating connection with database')
        db=None
    


# In[369]:


#Searching in tweets

def search(keywords=None,search_by='text'):
    """"
    search(keyword=None,search_by='text')
    
    This function is used to perform search operation over the tweet records stored in database
    
    parameters:
    1.keywords(list):
        Words to be searched in database
    2.search_by(string)
        where to search for keywords in database
        options:
            text
            name
            screen_name
            
    returns:
    An instance of tweet class
    Operations which be perfored on this object
    next():
        Goto next page of tweet book
    previous():
        Goto previous page of tweet book  
    """
    
    ob=None
    count=0
    keyword=get_words(keywords)
    
    #try:
    if search_by is 'text':
        db.tweets.create_index([(search_by,pymongo.TEXT)])
        data=db.tweets.find({'$text':{'$search':"%s"%keyword}},{'_id':0})
        count=data.count()
        db.tweets.drop_index('%s_text'%search_by);
        
    if search_by is 'name' or search_by is 'screen_name':
        db.users.create_index([(search_by,pymongo.TEXT)])
        data=db.users.find({'$text':{'$search':"\"%s\""%keyword}},{'_id':0})
        
        if data.count()>0:
            usr=next(data)
            usr=usr['id']
            data=db.tweets.find({'user_id':usr},{'_id':0})
            count=data.count()
        
        db.users.drop_index('%s_text'%search_by);
        
 
    if count>0:
        print('{0} tweets found'.format(data.count()))
        ob=gen_pages(db,data)
    else:
        print('No tweets found with such %s'%search_by)
                                
    
    #except:
     #   print('An error occoured')
    
    return ob


# In[297]:


#Sorting the Tweets by text,favorite_count,retweet_count,date,time,day

def sortTweets(sort_by=None,order='asc'):
    """
    sortTweets(sort_by=None,order='asc')
    
    This function returns the sorted tweets fetched from the database
    
    parameters:
    1.sort_by(string)
        Keys on the basis of which record are to be sorted
        options:
            date
            time
            day
            text
            retweet_count
            favorite_count
    2.order:
        Ascending or descending order
        options:
            asc
            des
            
    returns:
    An instance of tweet class
    Operations which be perfored on this object
    next():
        Goto next page of tweet book
    previous():
        Goto previous page of tweet book  
    """
    
    if order is 'asc':
        order=1
    elif order is 'des':
        order=-1
        
    if sort_by in ['date','time','day','text','retweet_count','favorite_count']:
        sort_by='created_at.{}'.format(sort_by)
        
    data=db.tweets.find({},{'_id':0}).sort([(sort_by,order)])
   
    ob=gen_pages(db,data)
    
    return ob


# In[301]:


#Filter tweets

def filterTweets(filter_by=None,keywords=None,flag=None,value=None):
    """
    filterTweets(filter_by=None,keywords=None,flag=None,value=None)
    
    This function is used to filter the tweets fetched from the database
    
    parameters:
    1.filter_by(string):
        options:
            retweet_count
            favorite_count
            followers_count
            friends_count
            favourites_count
            listed_count
            favorited
            quote_status
            retweeted
            truncated
            media_status
            is_reply
            lang
            place
            text
            source
            urls
            mentions
            hashtags
            name
            screen_name
            description
    2.keywords(list):
        Words to be filter the tweets
        Note: To be used with following filter options only:
            lang,place,text,source,urls,mentions,hashtags,name,screen_name,description
    3.flag(string):
        used with filter with string type values
        options:
            et
            lt
            gt
            lte
            gte
            ne
         Note: To be used with following filter options only: 
             retweet_count,favorite_count,followers_count,friends_count,favourites_count,listed_count
    4.value(int,bool)
        values for the filter
        Note: To be used with following filter options only: 
            Integer value: retweet_count,favorite_count,followers_count,friends_count,favourites_count,listed_count'
            Bool value: favorited','quote_status','retweeted','truncated','media_status','is_reply
    
    returns:
    An instance of tweet class
    Operations which be perfored on this object
    next():
        Goto next page of tweet book
    previous():
        Goto previous page of tweet book  
    """
    
    db.tweets.drop_indexes()
    db.users.drop_indexes()
    
    
    if flag:
        sym='$%s'%flag
    
    if keywords:
        st=get_words(keywords)
        
    #print(flag,st)
        
        
    if filter_by in ['retweet_count','favorite_count']:
        if flag is 'et':
            data=db.tweets.find({filter_by:value},{'_id':0})
        else:
            data=db.tweets.find({filter_by:{sym:value}},{'_id':0})
    elif filter_by in ['followers_count','friends_count','favourites_count','listed_count']:
        data=db.users.find({filter_by:{sym:value}},{'_id':0})
        data=getTweets(db,data)
        fl=1
    elif filter_by in ['favorited','quote_status','retweeted','truncated','media_status','is_reply']:
        data=db.tweets.find({filter_by:value},{'_id':0})
    elif filter_by is'verified':
        data=db.users.find({filter_by:value},{'_id':0})
        data=getTweets(db,data)
        fl=1
    elif filter_by is'source':
        db.tweets.create_index([(filter_by,pymongo.TEXT)])
        data=db.tweets.find({'$text':{'$search':"{0}".format(st)}})
    elif filter_by in ['lang','place','text','source','urls','mentions','hashtags']:
        db.tweets.create_index([(filter_by,pymongo.TEXT)])
        if flag is 'exact':
            data=db.tweets.find({'$text':{'$search':"\"{0}\"".format(st)}})
        elif flag is 'contains':
            data=db.tweets.find({'$text':{'$search':"{0}".format(st)}})
        elif flag is 'starts':
            data=db.tweets.find({filter_by:{'$regex':'^%s'%st}})
        elif flag is 'ends':
            data=db.tweets.find({filter_by:{'$regex':'%s$'%st}})
    elif filter_by in ['name','screen_name','description']:
        db.users.create_index([(filter_by,pymongo.TEXT)])
        if flag is 'exact':
            data=db.users.find({'$text':{'$search':"\"{0}\"".format(st)}})
        elif flag is 'contains':
            data=db.users.find({'$text':{'$search':"{0}".format(st)}})
        elif flag is 'starts':
            data=db.users.find({filter_by:{'$regex':'^%s'%st}})
        elif flag is 'ends':
            data=db.users.find({filter_by:{'$regex':'%s$'%st}})
        data=getTweets(db,data)
        fl=1
        
        
    if fl is 1 and len(data)>0:
        print('{0} tweets matched'.format(len(data)))
        obj=gen_pages_b(db,data)
    elif data.count()>0:
        print('{0} tweets matched'.format(data.count()))
        obj=gen_pages(db,data)
    else:
        print('No tweets found with %s filter'%filter_by)
    
    return obj        


# In[337]:


#Generating tweet pages

def gen_pages_b(db,twts,limit=32):
    """
    gen_pages_b(db,twts,limit=32)
    
    This function is used to implement pagination to the records fetched from the database.
    It uses tweet class to form a book like data structure providing with pages.
    
    parameters
    1.db:
        Instance of the database
    2.twts(dictionary):
        Tweet records fetched from the database
    2.limit(int)
        No. of tweets per page
        
    returns:
    An object of tweet class
    Operations which be perfored on this object
    next():
        Goto next page of tweet book
    previous():
        Goto previous page of tweet book  
    """
    
    i=0
    data=[]

    ob=tweetBook()

    for dat in twts:
        if i==limit:
            ob.assign(data,limit)
            data.clear()
            data.append(dat)
            i=1
        else:
            data.append(dat)
            i=i+1

    if i>=1:
        ob.assign(data,i)
        data.clear()
        
    ob.update_meta()
    
    return ob
        


# In[304]:


#Get all tweets

def getTweets(db,dat):
    """
    gettweets(db,data)
    
    This function returns the tweets by the a particular user 
    
    parameters:
    1.db:
        Instance of database
    2.data(dictionary)
        User details
        
    returns:
    A dictionary with tweets by a user
    """
    
    data=[]
    for var in dat:
        twts=db.tweets.find({'user_id':var['id']},{'_id':0})
        for va in twts:
            va['user']=var
            data.append(va)
            
    return data


# In[306]:


#Combine keywords for filter

def get_words(txt=[],delt='and'):
    """
    get_words(txt=[],delt='and')
    
    Combine the values of a list into a string on the basis of operation needed
    
    parameters:
    1.txt(list)
        list of values to be combined
    2.del(string)
        Delinimter
        options:
            and
            or
    
    returns:
    A string of combines list values
    """
    dt=''
    
    if delt is 'or':
        dl=','
    else:
        dl=' '
    
    for var in txt:
        dt+='%s%s'%(str(var),dl)
    
    return dt[0:len(dt)-1]


# In[310]:


#Data fetching through searching

def searchTweets(keywords=[],deliminiter='and',count=100):
    """
    searchTweets(keywords=[],deliminiter='and',count=100)
    
    This function fecth the tweets from the twitter's database with standard search protocol defined by twitter.
    Connection will closed by the twitter server after every request completion.
    These tweets are in form of data dictionary which is passed to store() function to store it in database.
    
    parameters:
    1.keywords(list):
        words to be searched for or for which tweets is to be collected
    2.deliminiter(string)
        relation between multipe keywords if provided
    3.count(int):
        number to tweets to be fetched
    
    returns:
    None
    
    Print numbers of records added to database successfully
    """
    
    rec=0
    query=percent_encode(get_words(keywords,deliminiter))
    q="q=%s&result_type=recent&count=100"%(query)
    
    while count>0:
        count=count-100
        result = api.GetSearch(raw_query=q,return_json=True,include_entities=True)
        rec=rec+store(result['statuses'])
        q=result['search_metadata']['next_results']
        q=q[1:len(q)]
    
    print('{0} Records Added Successfully'.format(rec))


# In[371]:


#Data fetching through streaming(Note: It is to be used to collect random tweets only, Not an accurate way to search tweets)

def streamTweets(keywords=[],deliminiter='and',count=100,language='',filter_level='none'):
    
    """
    streamTweets(keywords=[],deliminiter='and',count=100)
    
    This function fecth the tweets from the twitter's database with stream filter protocol defined by twitter.
    Connection will be open with twitter servers until it is closed by api.
    These tweets are in form of data dictionary which is passed to store() function to store it in database.
    
    parameters:
    1.keywords(list):
        words to be searched for or for which tweets is to be collected
    2.deliminiter(string)
        relation between multipe keywords if provided
    3.count(int):
        number to tweets to be fetched
    4.languages
        options:
            en
            hi
            for more : https://developer.twitter.com/en/docs/developer-utilities/supported-languages/api-reference/get-help-languages
    5.filter_level:
        Setting this parameter to one of none, low, or medium will set the minimum value of the filter_level Tweet attribute required
        to be included in the stream. The default value is none, which includes all available Tweets.
    returns:
    None
    
    Print numbers of records added to database successfully
    """
    
    rec=0
    query=percent_encode(get_words(keywords,deliminiter))
    results=api.GetStreamFilter(track=query,filter_level=filter_level,languages=language)
    
    for var in range(count):
        try:
            (data,user)=extract(next(results))
            rec=rec+add_document(db,data,user)
        except:
            continue
    
    results.close()
            
    print('{0} Records Added Successfully'.format(rec))
    


# In[313]:


#Store twitter search results to database

def store(stats):
    """
    store(stats)
    
    Iterate over the tweets fetched from twitter database
    
    parameters:
    1.stats(list)
        List with certain number of tweets
        
    returns:
    An integer value 
    """
    rec=0
    for var in range(len(stats)):
        (data,user)=extract(stats[var])
        rec=rec+add_document(db,data,user)
    
    return rec


# In[320]:


#Export to CSV files

def exportToCSV(columns=[],filename='twitter'):
    """
    exportToCSV(columns=[],details='tweets'
    
    This function is use to export specific details from database to csv file.
    This function used DicWriter of csv to write data dictionary to csv file
    
    1.columns(list)
        database key values to be exported to csv file
    3.filename
        name of csv file
        
    returns:
    None
    
    Prints status of file completion
    """
    
    dct={}
    for var in columns:
        dct[var]=1
    dct['_id']=0
    
    if  details is 'users':
        res=db.users.find({},dct)
    else:
        res=db.tweets.find({},dct)
        
    
    with open('%s.csv'%filename, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        
        for va in res:
            print(va)
            writer.writerow(va)
        
    
    print('Writing complete')
    


# In[328]:


#Filter by date,time and day

def filterDateTime(filter_by=None,value1=None,value2=None,flag=None):
    """
    filterTweets(filter_by=None,keywords=None,flag=None,value=None)
    
    This function is used to filter the tweets fetched from the database on the basis of date
    
    parameters:
    1.filter_by(string):
        options:
            date
            time
            day
    2.value1(list,string):
        Values for the filtering
        Note: To be used with following filter options and flag only:
            Date
            Time
            Day
                Format:
                Date(list):[2018,3,21] i.e. [yyyy,mm,dd]
                    Flags:
                        et
                        gt
                        lt
                        lte
                        gte
                        ne
                Time(list):[14,2,1] i.e [hh,mm,ss]
                    Flags:
                        et
                        gt
                        lt
                        lte
                        gte
                        ne
                Day(string):
                value options:
                        'Mon'
                        'Tue'
                        'Wed'
                        'Thu'
                        'Fri'
                        'Sat'
                        'Sun'
    2.value2(list,string):
        Values for the filtering
        Note: To be used with following filter options only:
            Date
            Time
        Format:
            Date(list):[2018,3,21] i.e. [yyyy,mm,dd]
            Time(list):[14,2,1] i.e [hh,mm,ss]
        Flags:
            bt
        
    4.flag(string):
        used with filter with string type values
        options:
            bt
            et
            lt
            gt
            lte
            gte
            ne
         Note: To be used with following filter options only:
             Date
             Time

    returns:
    An instance of tweet class
    Operations which be perfored on this object
    next():
        Goto next page of tweet book
    previous():
        Goto previous page of tweet book  
    """
    
    obj=None
    filter_b='created_at.%s'%filter_by
    
    if flag:
        sym='$%s'%flag
        
    if filter_by is 'date' and flag is not 'bt':
        value=getDate(value1)
    elif filter_by is 'time' and flag is not 'bt':
        value=getTime(value1)
    elif filter_by is 'day':
        value=value1  
    elif filter_by is 'date' and flag is 'bt':
        value1=getDate(value1)
        value2=getDate(value2)
    elif filter_by is 'time' and flag is 'bt':
        value1=getTime(value1)
        value2=getTime(value2)
        
    print(value1,value2)
    
    if filter_by in ['date','time','day'] and flag is 'et':
        data=db.tweets.find({filter_b:value},{'_id':0})
    elif filter_by in ['date','time'] and flag in ['gt','lt','lte','gte','ne']:
        data=db.tweets.find({filter_b:{sym:value}},{'_id':0})
    elif filter_by in ['date','time'] and flag is 'bt':
        data=db.tweets.find({filter_b:{'$gt':value1},filter_b:{'$lt':value2}},{'_id':0})
        
    if data.count()>0:
        print('{0} tweets matched'.format(data.count()))
        obj=gen_pages(db,data)
    else:
        print('No tweets found with %s filter'%filter_by)
        
    return obj


# In[330]:


#Get concatinated value for date,time

def getDate(dt):
    """
    getDate(dt)
    
    returns a formated date from the values of list parameter
    """
    date=''
    for va in dt:
        date+='%s '%va
    
    return date[0:len(date)-1]

def getTime(tm):
    """
    getTime(dt)
    
    returns a formated time from the values of list parameter
    """
    time=''
    for va in tm:
        if va is 0 or va is '0' or len(str(va)) is 1:
            va='0'+str(va)
        time+='%s:'%str(va)
    
    return time[0:len(time)-1]


# In[365]:


#Configure API

def configure(consumer_key=None,access_token_key=None,consumer_secret=None,access_token_secret=None,uri=None):
    """
    configure(consumer_key=None,access_token_key=None,consumer_secret=None,access_token_secret=None,uri=None)
    
    Saves the authetication keys to a json file for further initialization process
    
    parameters:
    1.consumer_key
    2.access_token_key
    3.consumer_secret
    4.access_token_secret
    """
    
    data={
        'keys':{'consumer_key':consumer_key
        ,'access_token_key':access_token_key
        ,'consumer_secret':consumer_secret
        ,'access_token_secret':access_token_secret
               }
        ,'uri':uri
    }
    
    try:
        with open('twitter.json', 'w') as outfile:
            json.dump(data, outfile)
        print('API configured successfully')
    except:
        print('Error in configuring API')
        


# In[367]:


#Intializing the search/streaming connection

def initialize():
    """
    initialize()
    
    Initializes the api instance using python-twitter library which is used to create conection and fetch tweets
    """
    
    global api
    
    try:
    
        data=json.load(open('twitter.json'))
    
        consumer_key=data['keys']['consumer_key']
        access_token_key=data['keys']['access_token_key']
        consumer_secret=data['keys']['consumer_secret']
        access_token_secret=data['keys']['access_token_secret']

        api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)
        
        database()
        par()
        
        print('API intialized')
    except:
        print('Error in intializing API')


# In[334]:


#Verifying intialization

def verify():
    """
    verify():
    
    Prints the details of user for verifcation purpose
    """
    pp.pprint(api.VerifyCredentials())


# In[335]:


#View tweet book page

def viewBook(book):
    """
    viewBook(book)
    
    parameter:
    1.book
        Instance of tweetBook
    
    Prints the tweets in single page
    """
    
    pp.pprint(book)


# In[374]:


#Export filtered data to csv file

def exportFilter(book,cols=[],filename='filterTwitter'):
    """
    exportFilter(book,cols=[],filename='filterTwitter')
    
    Export the filtered tweets to the csv file
    
    parameters:
    1.book:
        Instance of tweetBook class
    2.filename(string)
        name of csv file
    
    """
    
    col=book.data[var]['tweets'][0].keys()
    data=[]
    
    for var in range(book.pages):
        dat=book.data[var]['tweets']
        for var in dat:
            try:
                tmp={}
                for va in col:
                    tmp[col]=var[col]
                data.append(tmp)
            except:
                continue  
    
    try:
        with open('%s.csv'%filename, 'wb') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=col)
        
            for va in data:
                print(va)
                writer.writerow(va)
        
    
        print('Writing complete')
    except:
        print('Error while writing to file')
            
            


# In[5]:


"""by nikhil singh bisht
    email:nikhilsinghbisht21@gmailcom
    git:github.com/nikhilbisht21 
    linkden:linkedin.com/in/Nikhil-bisht-155947132/
    Date:3/23/2018
    """

