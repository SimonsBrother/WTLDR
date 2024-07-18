""" Some tests for the emailing module.
Note that these tests are manual, and require an email and password. """

import wtldr.modules.emailing as emailing
from datetime import datetime

from dotenv import dotenv_values

from wtldr.modules.logging_ import create_logger


def test_first_email(email_manager: emailing.EmailManager):
    """ Tries to get the first email using get_email, which is an email I sent to the account, which ensures emails can be retrieved by ID.
     This indirectly tests the Email static methods. """
    expected_email = emailing.Email(1, 'Caleb Hair <calebthair@outlook.com>', 'Lab rat test subject',
                                    "Lab rat lab rat lab rat", datetime.fromisoformat('2024-05-13 13:33:47'))

    actual_email = email_manager.get_email_from_mailbox(1)

    assert expected_email.__repr__() == actual_email.__repr__()
    assert expected_email.body.rstrip() == actual_email.body.rstrip()


def test_tldr_email(email_manager: emailing.EmailManager):
    """ Tries to get a typical TLDR email using get_email. """

    # I think due to subtle differences in the body between copying it from a terminal compared to when it
    # is retrieved makes comparing the exact contents impractical, so I'm checking the approximate length.
    approximate_expected_body = """OpenAI announced a new AI model yesterday called GPT-4o that can
converse using speech in real time, read emotional cues, and respond
to visual input  

 Sign Up [1] |Advertise [2]|View Online [3] 

		TLDR 

		TOGETHER WITH [QA Wolf] [4]

TLDR 2024-05-14

 👋 GOODBYE LOW TEST COVERAGE AND SLOW QA CYCLES (SPONSOR) [4] 

 Bugs sneak out when less than 80% of user flows are tested before
shipping. But getting that kind of coverage — and staying there —
is hard and pricey for any sized team.

QA Wolf [4]takes testing off your plate:

→ Get to 80% test coverage in just 4 months.

→ Achieve 3-minute QA cycles [4].

→ Stay bug-free with 24-hour maintenance [4] and on-demand test
creation.

→ Get unlimited parallel test runs [4]

→ Zero Flakes guaranteed

QA Wolf has generated amazing results [5] for companies like
Salesloft, AutoTrader, Mailchimp, and Bubble.

⭐ Rated 4.8/5 on G2.

Learn more about their 90-day pilot [4]

📱 

BIG TECH & STARTUPS

 MAJOR CHATGPT-4O UPDATE ALLOWS AUDIO-VIDEO TALKS WITH AN
“EMOTIONAL” AI CHATBOT (6 MINUTE READ) [6] 

 OpenAI announced a new AI model yesterday called GPT-4o that can
converse using speech in real time, read emotional cues, and respond
to visual input. It will roll out over the next few weeks for free to
ChatGPT users and as a service through API. Paid subscribers will have
five times the rate limits of free users. The API will feature twice
the speed, 50% lower cost, and five times higher rate limits compared
to GPT-4 Turbo. A 26-minute long video that introduces GPT-4o and
demonstrates its abilities is available in the article. 

 META IS REPORTEDLY WORKING ON CAMERA-EQUIPPED AI EARPHONES (2 MINUTE
READ) [7] 

 Meta is reportedly working on AI-powered earphones equipped with
cameras. Internally codenamed 'Camerabuds', the earphones will
leverage AI capabilities for real-time object identification and
foreign language translation. Meta's leadership sees AI-powered
earphones as the next logical step in the evolution of wearable
technology. It has partnered with Kansas-based electronics company Ear
Micro to explore the possibilities of this emerging technology. 

🚀 

SCIENCE & FUTURISTIC TECHNOLOGY

 $16K G1 HUMANOID RISES UP TO SMASH NUTS, TWIST, AND TWIRL (4 MINUTE
READ) [8] 

 Unitree has released the first few details on its G1 Humanoid Agent,
a $16,000 robotic helper. The robot is equipped with 3D LiDAR sensors,
a depth camera, three-fingered grippers, and a 9,000-mAh battery pack.
It can recover from brutal kicks and punches, as seen in the short
demo video in the article. At around 35 kg, the robot can fold itself
down to 690x450x300-mm proportions for compact carry. 

 USING MRI, ENGINEERS HAVE FOUND A WAY TO DETECT LIGHT DEEP IN THE
BRAIN (6 MINUTE READ) [9] 

 Scientists often label cells with proteins that glow to measure
changes in gene expression, but this technique is difficult to apply
to structures deep within the brain as light scatters too much before
it can be detected. MIT engineers have engineered blood vessels to
express a protein that causes them to dilate in the presence of light.
This dilation can be observed with magnetic resonance imaging,
allowing researchers to pinpoint the source of light. The new
technique allows researchers to explore the inner workings of the
brain in more detail than previously possible. 

💻 

PROGRAMMING, DESIGN & DATA SCIENCE

 80% OFF SURFSHARK ONE — ESSENTIAL TOOLS TO PROTECT YOURSELF ONLINE
(SPONSOR) [10] 

 Block tracking, avoid malware, and protect yourself from data
breaches — with one easy-to-use app. This bundle includes
Alternative ID [10], which provides a new identity and email for
online registrations to protect your real identity; Surfshark Alert
[11], which notifies you if your email, credit card, or ID is leaked
in a breach; and four other tools. Click here for 80% off + 3/mo extra
[11] 

 PG_LAKEHOUSE (GITHUB REPO) [12] 

 pg_lakehouse is an extension that transforms Postgres into an
analytical query engine over object stores. Querying non-operational
data by moving it into a cloud data warehouse or operating a new query
engine is expensive and time-consuming. pg_lakehouse allows this data
to be queried directly from Postgres, eliminating the need for new
infrastructure, loss of data freshness, data movement, and
non-Postgres dialects of other query engines. 

 THE ALTERNATIVE IMPLEMENTATION PROBLEM (8 MINUTE READ) [13] 

 Positioning a project as an alternative implementation of something
is a losing proposition. Building an alternative implementation means
reacting to the whims of the canonical implementation - they have
control over the direction of the project and you can only keep up.
It's better in most cases to make an original system rather than being
chained by expectations to match another implementation. 

🎁 

MISCELLANEOUS

 BEFORE LAUNCHING, GPT-4O BROKE RECORDS ON CHATBOT LEADERBOARD UNDER A
SECRET NAME (3 MINUTE READ) [14] 

 The mysterious chat-topping AI chatbot known as 'gpt2-chatbot' that
had been undergoing testing on the LMSYS Chatbot Arena has been
revealed to be OpenAI's newly announced GPT-4o model. The model had
topped the Chatbot Arena leaderboard, achieving the highest documented
score ever. OpenAI tested multiple versions of GPT-4o on Chatbot Arena
before its announcement yesterday. The models surpass all other models
by a significant gap and have become the strongest ever in the Arena. 

 GAMESTOP, AMC SOAR MORE THAN 70% EACH AS ‘ROARING KITTY' MEME
TRADER RESURFACES (5 MINUTE READ) [15] 

 'Roaring Kitty', the man who inspired the epic short squeeze of 2021,
posted online for the first time in roughly three years on Monday,
causing GameStop and AMC shares to rally dramatically. The picture he
posted of a video gamer leaning forward on their chair garnered 63,000
likes in 13 hours. He later posted a few videos with scenes from
popular TV shows and movies, but there is no clear indication of what
these posts mean. GameStop's stock has started to move higher
recently, which, along with the enormous amount of short interest in
the stock, may have rekindled his interest. 

⚡ 

QUICK LINKS

 GET YOUR BRAND IN FRONT OF 4+ MILLION TLDR READERS (SPONSOR) [16] 

 Have you ever wanted to see your own brand in TLDR? Our team already
helps companies like AWS, Google Cloud, and Vercel reach an audience
of smart tech-savvy professionals like yourself, find out more here
[16]! 

 PROTECTING YOUR EMAIL ADDRESS VIA SVG INSTEAD OF JS (5 MINUTE READ)
[17] 

 This article presents an email-protection technique based on SVG that
will keep emails hidden from any simple or amateurish scripts trawling
the web seeking to copy any unprotected email addresses they find. 

 GOOGLE IS BRINGING PROJECT STARLINE'S ‘MAGIC WINDOW' EXPERIENCE TO
REAL VIDEO CALLS (2 MINUTE READ) [18] 

 Google is teaming up with HP to commercialize Project Starline and
bring its futuristic videoconferencing technology to Zoom and Meet
calls. 

 IT'S AN AGE OF MARVELS (7 MINUTE READ) [19] 

 A look at the world we live in and the amazing technologies humanity
has developed. 

 APPLE FINALLY ADDS IPHONE ALERTS FOR THIRD-PARTY BLUETOOTH TRACKERS
(3 MINUTE READ) [20] 

 iOS 17.5 enables iPhones to alert users when unauthorized third-party
Bluetooth trackers are following them. 

 RECENT DOCKER BUILDKIT FEATURES YOU'RE MISSING OUT ON (9 MINUTE READ)
[21] 

 BuildKit, an improved builder backend for Docker, introduced many new
features to Docker. 

 GPT-4O (2 MINUTE READ) [22] 

 A key part of OpenAI's mission is to put very capable AI tools in the
hands of people - GPT-4o makes talking to a computer feel natural and
it will allow people to do much more with computers than ever before. 

Want to advertise in TLDR? 📰

 If your company is interested in reaching an audience of tech
executives, decision-makers and engineers, you may want to ADVERTISE
WITH US [23]. 

 If you have any comments or feedback, just respond to this email! 

Thanks for reading, 
Dan Ni & Stephen Flanders 

If you don't want to receive future editions of TLDR, please
unsubscribe from TLDR [24] or manage all of your TLDR newsletter
subscriptions [25]. 

 

Links:
------
[1] https://tldr.tech/signup?utm_source=tldr
[2] https://advertise.tldr.tech/?utm_source=tldr&utm_medium=newsletter&utm_campaign=advertisetopnav
[3] https://a.tldrnewsletter.com/web-version?ep=1&lc=68b1568a-1130-11ef-90bb-8bb14c9311d5&p=e8cf6474-11c1-11ef-9716-c3259b496aae&pt=campaign&t=1715682360&s=522d4582b6fdd8434a2b28a840295f90faa83859aa7850f6e610136e8f1602f5
[4] https://www.qawolf.com/lp/tldr?utm_campaign=GoodbyeLowSlow05142024&utm_source=tldr&utm_medium=newsletter
[5] https://www.qawolf.com/case-studies?utm_campaign=GoodbyeLowSlow05142024&utm_source=tldr&utm_medium=newsletter
[6] https://arstechnica.com/information-technology/2024/05/chatgpt-4o-lets-you-have-real-time-audio-video-conversations-with-emotional-chatbot/?utm_source=tldrnewsletter
[7] https://www.androidauthority.com/meta-ai-earphones-3442560/?utm_source=tldrnewsletter
[8] https://newatlas.com/robotics/unitree-g1-humanoid-agent/?utm_source=tldrnewsletter
[9] https://news.mit.edu/2024/using-mri-engineers-have-found-way-detect-light-deep-brain-0510?utm_source=tldrnewsletter
[10] https://surfshark.com/deal/alternative-id?coupon=altiddeal&transaction_id=1023e089e6a0fb74a5446b51f88727&offer_id=1568&affiliate_id=16286&source=&aff_sub=&utm_source=Affiliates&utm_medium=16286&utm_campaign=affiliate&recurring_goal_id=1559
[11] https://surfshark.com/deal/alert?coupon=alertdeal&transaction_id=102aa6007216c3115ba2b2bfa1cbd8&offer_id=1587&affiliate_id=16286&source=&aff_sub=&utm_source=Affiliates&utm_medium=16286&utm_campaign=affiliate&recurring_goal_id=1527
[12] https://github.com/paradedb/paradedb/tree/dev/pg_lakehouse?utm_source=tldrnewsletter
[13] https://pointersgonewild.com/2024/04/20/the-alternative-implementation-problem/?utm_source=tldrnewsletter
[14] https://arstechnica.com/information-technology/2024/05/before-launching-gpt-4o-broke-records-on-chatbot-leaderboard-under-a-secret-name/?utm_source=tldrnewsletter
[15] https://www.cnbc.com/2024/05/13/gme-jumps-as-trader-roaring-kitty-who-drove-meme-craze-posts-again.html?utm_source=tldrnewsletter
[16] https://advertise.tldr.tech/?utm_source=tldr&utm_medium=newsletter&utm_campaign=quick05142024
[17] https://rouninmedia.github.io/protecting-your-email-address-via-svg-instead-of-js/?utm_source=tldrnewsletter
[18] https://www.theverge.com/2024/5/13/24155395/google-project-starline-hp-video-conferencing-2025?utm_source=tldrnewsletter
[19] https://blog.plover.com/tech/its-an-age-of-marvels.html?utm_source=tldrnewsletter
[20] https://www.theverge.com/2024/5/13/24155630/apple-google-airtag-bluetooth-tracker-alert-standard?utm_source=tldrnewsletter
[21] https://martinheinz.dev/blog/111?utm_source=tldrnewsletter
[22] https://blog.samaltman.com/gpt-4o?utm_source=tldrnewsletter
[23] https://advertise.tldr.tech/?utm_source=tldr&utm_medium=newsletter&utm_campaign=advertisecta
[24] https://a.tldrnewsletter.com/unsubscribe?ep=1&l=cfa2d55a-b7be-11e8-a3c9-06b79b628af2&lc=68b1568a-1130-11ef-90bb-8bb14c9311d5&p=e8cf6474-11c1-11ef-9716-c3259b496aae&pt=campaign&pv=4&spa=1715680897&t=1715682360&s=a053bc61c1a92adc7bd0f328cb8e2d24e60411630279148db30602433c43264f
[25] https://tldr.tech/tech/manage?email=calebslabrat%40outlook.com"""
    expected_email = emailing.Email(3, 'TLDR <dan@tldrnewsletter.com>', 'b\'GPT-4o crushes leaderboard \'',
                                    "", datetime.fromisoformat('2024-05-14 10:26:00'))
    actual_email = email_manager.get_email_from_mailbox(3)

    assert expected_email.__repr__() == actual_email.__repr__()  # Compares the object values excluding the body.
    # Ensure the contents are approximately the same length
    assert abs(len(actual_email.body.strip()) - len(approximate_expected_body.strip())) < 300


def test_search_for_tldr(email_manager: emailing.EmailManager):
    """ Gets all the TLDR emails using get_tldr_emails and ensures they have the same sender. """
    tldr_emails = email_manager.get_tldr_email_ids()

    email_manager.open_mailbox()
    for email_id in tldr_emails:
        email_obj = email_manager.get_email(email_id)
        sender = email_obj.sender
        assert "dan@tldrnewsletter.com" in sender

    email_manager.close_mailbox()


# TODO: make invalid tests for Email static methods


if __name__ == "__main__":
    secrets = dotenv_values()

    username = secrets["EMAIL"]
    password = secrets["PASSWORD"]
    imap_server = "imap-mail.outlook.com"  # https://www.systoolsgroup.com/imap/ for other servers

    email_manager_ = emailing.EmailManager(username, password, imap_server, create_logger("/Users/calebhair/Documents/Projects/WTLDR/wtldr/testing/logs"))

    test_first_email(email_manager_)
    print("Passed")
    test_tldr_email(email_manager_)
    print("Passed")
    test_search_for_tldr(email_manager_)
    print("Passed")

    del email_manager_
