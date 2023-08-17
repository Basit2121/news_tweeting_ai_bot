from playwright.sync_api import sync_playwright
import time
import random
import requests
import openai

openai.api_key = ""
        
def click_element_with_class(page, class_name):
    element = page.query_selector(f'.{class_name}')
    if element:
        element.click()

def login_to_twitter(username, password):
    
    with sync_playwright() as playwright:
        while True:
            
            try:
        
                browser = playwright.chromium.launch(headless=True, channel='msedge')
                context = browser.new_context()
                page = context.new_page()
                page.goto("https://twitter.com/login")
                time.sleep(random.uniform(2,4))
                # Fill in the login form
                page.fill('input[autocomplete="username"]', username)
                
                time.sleep(random.uniform(2,4))
                # Press the "Next" button
                page.click('text="Next"')
                time.sleep(random.uniform(2,4))
                # Wait for the password input field to appear
                page.wait_for_selector('input[autocomplete="current-password"]')
                time.sleep(random.uniform(2,4))
                # Fill in the password
                page.fill('input[autocomplete="current-password"]', password)
                time.sleep(random.uniform(2,4))
                # Submit the form
                page.click('div[data-testid="LoginForm_Login_Button"]')
                
                print("Logged in With Username -> ", username)
                
                time.sleep(random.uniform(4,5))
                
                old_tweet = None
                link = None
                tweet_text = None
                
                while True:
                    try:
                        page.goto("https://twitter.com/AlertesInfos")

                        time.sleep(6)

                        if page.query_selector('span.css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0'):
                            print("Skipping Pinned Post")
                            elements = page.query_selector_all('.css-1dbjc4n.r-1awozwy.r-onrtq4.r-18kxxzh.r-1b7u577')
                            elements[1].click()
                        else:
                            elements = page.query_selector_all('.css-1dbjc4n.r-1awozwy.r-onrtq4.r-18kxxzh.r-1b7u577')
                            elements[0].click()
                        
                        time.sleep(5)
                        
                        try:
                            tweet_div = page.query_selector('.css-901oao.r-18jsvk2.r-37j5jr.r-1inkyih.r-16dba41.r-135wba7.r-bcqeeo.r-bnwqim.r-qvutc0')
                        except:
                            pass
                        
                        if tweet_div:
                            
                            try:
                                tweet_text = tweet_div.text_content()
                                
                                tweet_text = tweet_text + '  '
                            except:
                                pass
                        
                        img_url = None
                        
                        video_component = page.query_selector('[data-testid="videoComponent"]')

                        if video_component:
                            pass
                        else:
                            video_component = None
                        
                        try:
                            link_elements = page.query_selector_all('a[href^="https://t.co"]')

                            # Extract and print the links
                            for link_element in link_elements:
                                link = link_element.get_attribute('href')
                                print(link)
                        except:
                            link = None
                        
                        prompt = f"Rephrase the following sentence compleatly but keep it in the french language, Keeps the words that are in Full capital Letters Such as 'FLASH' unchanged and at the start of the text, also do not change any words that are inside quotation marks: '{tweet_text}'"
                        
                        previous_tweet = tweet_text
                        
                        print(previous_tweet)
                        
                        if old_tweet != previous_tweet:
                            
                            print("Getting New Tweets Text")
                            
                            try:
                                
                                img_elements = page.query_selector_all('img[src^="https://pbs.twimg.com"]')
                                if len(img_elements) > 2:
                                    image_link = img_elements[2].get_attribute('src')
                                    if image_link.endswith('name=small'):
                                        img_url = image_link
                                    else:
                                        img_url = None
                                else:
                                    img_url = None
                                    
                            except:
                                pass
                            
                            time.sleep(5)
                            
                            if img_url != None:
                                
                                if link != None:
                                    
                                    page.goto("https://twitter.com/compose/tweet")
                                    
                                    response = openai.Completion.create(
                                        engine="text-davinci-003",
                                        prompt=prompt,
                                        max_tokens=200
                                    )
                                    
                                    if tweet_text != None:

                                        tweet_text = response.choices[0].text.strip()
                                    
                                    tweet_message = tweet_text + ' \n' + link

                                    time.sleep(random.uniform(4,5))
                                    
                                    textarea = page.query_selector('[data-testid="tweetTextarea_0"]')
                                    
                                    time.sleep(random.uniform(1,2))
                                    
                                    textarea.fill(tweet_message)
                                    
                                    time.sleep(random.uniform(4,5))

                                    print("Uploading tweet with link")
                                    
                                    
                                    try:
                                        post_button = page.wait_for_selector('div[data-testid="tweetButton"]')
                                        post_button.click()
                                    except:
                                        pass
                                    
                                    page.keyboard.press('Enter')
                                    
                                    time.sleep(random.uniform(3,5))
                                    
                                    old_tweet = previous_tweet
                                    
                                    print("Tweeted!!!")
                                    
                                else:
                                    print("Getting New Tweets Media")
                                    
                                    response = requests.get(img_url)

                                    with open("tweet.webp", "wb") as f:
                                        f.write(response.content)
                                        
                                    time.sleep(5)
                                    
                                    page.goto("https://twitter.com/compose/tweet")
                                    
                                    response = openai.Completion.create(
                                        engine="text-davinci-003",
                                        prompt=prompt,
                                        max_tokens=1000
                                    )

                                    if tweet_text != None:

                                        tweet_text = response.choices[0].text.strip()
                                    
                                    tweet_message = tweet_text + ' \n'

                                    time.sleep(random.uniform(4,5))
                                    
                                    textarea = page.query_selector('[data-testid="tweetTextarea_0"]')
                                    
                                    time.sleep(random.uniform(1,2))
                                    
                                    textarea.fill(tweet_message)
                                    
                                    time.sleep(random.uniform(4,5))
                                    
                                    image_path = 'tweet.webp'
                                    
                                    print("Uploading Image and Text")
                                
                                    input_file = page.query_selector('input[type="file"]')
                                    input_file.set_input_files(image_path)
                                    
                                    time.sleep(20)
                                    
                                    try:
                                        post_button = page.wait_for_selector('div[data-testid="tweetButton"]')
                                        post_button.click()
                                    except:
                                        pass
                                    
                                    page.keyboard.press('Enter')
                                    time.sleep(5)
                                    page.keyboard.press('Enter')
                                    
                                    time.sleep(random.uniform(3,5))
                                    
                                    old_tweet = previous_tweet
                                    
                                    print("Tweeted!!!")
                                
                            else:
                                
                                video_url = page.url + "/video/1"
                                
                                page.goto("https://twitter.com/compose/tweet")
                                
                                response = openai.Completion.create(
                                        engine="text-davinci-003",
                                        prompt=prompt,
                                        max_tokens=200
                                    )

                                if tweet_text != None:

                                        tweet_text = response.choices[0].text.strip()
                                
                                tweet_message = tweet_text + ' \n' + video_url

                                time.sleep(random.uniform(4,5))
                                
                                textarea = page.query_selector('[data-testid="tweetTextarea_0"]')
                                
                                time.sleep(random.uniform(1,2))
                                
                                textarea.fill(tweet_message)
                                
                                time.sleep(random.uniform(4,5))
                            
                                print("Uploading Text")
        
                                time.sleep(5)
                                
                                try:
                                    post_button = page.wait_for_selector('div[data-testid="tweetButton"]')
                                    post_button.click()
                                except:
                                    pass
                                
                                page.keyboard.press('Enter')
                                
                                time.sleep(random.uniform(3,5))
                                
                                old_tweet = previous_tweet
                                
                                print("Tweeted!!!")
                            
                        else:
                            print("No New Tweets\nChecking Again After 5 minute.")
                            time.sleep(300)
                    except Exception as e:
                        print(e)
                        print("\nThere was an Error, Retrying...")
                        
                context.close()
                browser.close()
            except Exception as e:
                print(e)
                print("\nThere was an Error Getting to Twitter, Retrying...")
        
username = input("Enter Username @")
password = input("Enter Password : ")

login_to_twitter(username, password)