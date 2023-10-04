import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import calendar
import datetime
import smtplib
from email.mime.text import MIMEText

# Email config
smtp_server = 'smtp.gmail.com'
smtp_port = 587
sender_email = 'MichaelKerley07@gmail.com'
sender_password = 'fubi rplr seli fmua'

def send_email(receiver_email, subject, message):
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # Create The Email
        msg = MIMEText(message)
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())

        # Close the server
        server.quit()
        print(f"Notification Sent To {receiver_email}")
    except Exception as e:
        print(f"An Error Occurred: {str(e)}")


# Define the scope and credentials file path
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = None

# Check if running in GitHub Actions environment
if 'GITHUB_ACTIONS' in os.environ:
    # Load credentials from a GitHub Actions secret
    credentials_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_json, scope)
else:
    # Load credentials from a local file
    credentials_path = "C:/Users/Mkerl/Downloads/calendernotif-400322-015ca3a312f6.json"
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)


# Authenticate using the credentials
gc = gspread.authorize(credentials)
    
# Open the Google Sheets document by name
spreadsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1dwAd7sNk4RVsPYALsMgyP0-euXYB_parh5YPml6Zj-I/edit#gid=0")


# Select the specific worksheet (page) by title
worksheet = spreadsheet.worksheet("Sheet1")

# Fetch data from the worksheet as a list of dictionaries, skipping the first row (header row)
data = worksheet.get_all_records(head=1)  # Specify 'head=2' to skip the first row

# Process and send notifications
assignments = []
for row in data:
    year = int(row['year'])
    month = int(row['month'])
    day = int(row['day'])
    assignment_type = row['assignment_type']
    assignment_description = row['assignment_description']

    assignments.append((year, month, day, assignment_type, assignment_description))  # Append each assignment to the list



def send_assignment_notif(assignments, receiver_email):
    # Assignment Type Dictionary
    assignment_types = {
        'exam': 'Exam',
        'quiz': 'Quiz',
        'homework': 'Homework'
    }

    for assignment in assignments:
        year, month, day, assignment_type, assignment_description = assignment

        # Date Format
        formatted_date = datetime.date(year, month, day).strftime('%B %d, %Y')

        # Create a calendar event
        event_description = f"{assignment_types.get(assignment_type, 'Assignment')}: {assignment_description} \n \nDue: {formatted_date}"

        # Check if the event is in the future or due today
        event_date = datetime.date(year, month, day)
        today = datetime.date.today()

        if assignment_type == 'exam':
            exam_notif_date = event_date - datetime.timedelta(days=5)
            if today <= event_date and today >= exam_notif_date:
                send_email(receiver_email, "Exam Notification", event_description)
            elif today == event_date:
                send_email(receiver_email, "EXAM TODAY", event_description)
        
        elif assignment_type == 'quiz':
            quiz_notif_date = event_date - datetime.timedelta(days=3)
            if today <= event_date and today >= quiz_notif_date:
                send_email(receiver_email, "Quiz Notification", event_description)
            elif today == event_date:
                send_email(receiver_email, "QUIZ TODAY", event_description)
        
        elif assignment_type == 'homework':
            hw_notif_date = event_date - datetime.timedelta(days=2)
            if today <= event_date and today >= hw_notif_date:
                send_email(receiver_email, "Homework Notification", event_description)
            elif today == event_date:
                send_email(receiver_email, "HOMEWORK DUE TODAY", event_description)
    



       

# List of Assignments
#assignments = [
 #   (2023, 9, 2, 'exam', 'Midterm Exam'),
  #  (2023, 9, 27, 'quiz', 'Quiz 1'),
   # (2023, 9, 28, 'homework', 'Homework 3'),
    #(2023, 8, 13, 'homework', 'Homework 17'),
#]




receiver_email = 'michaelkerley07@gmail.com'

send_assignment_notif(assignments, receiver_email)


#c = calendar.TextCalendar(calendar.SUNDAY)
#str = c.formatmonth(2025, 1)
#print(str)

 

