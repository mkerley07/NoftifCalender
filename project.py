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


# Function to send assignment notifications
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

        if assignment_type == 'exam':
            exam_notif_date = event_date - datetime.timedelta(days=5)
            if datetime.date.today() < event_date and datetime.date.today() >= exam_notif_date:
                
                send_email(receiver_email, "Exam Notification", event_description)
            elif event_date == datetime.date.today():
                    send_email(receiver_email, "EXAM TODAY", event_description)
        
        elif assignment_type == 'quiz':
            quiz_notif_date = event_date - datetime.timedelta(days=3)
            if datetime.date.today() < event_date and datetime.date.today() >= quiz_notif_date:
                
                send_email(receiver_email, "Quiz Notification", event_description)
            elif event_date == datetime.date.today():
                    send_email(receiver_email, "QUIZ TODAY", event_description)
        
        elif assignment_type == 'homework':
            hw_notif_date = event_date - datetime.timedelta(days=2)
            if datetime.date.today() < event_date and datetime.date.today() >= hw_notif_date:
                
                send_email(receiver_email, "Homework Notification", event_description)
            elif event_date == datetime.date.today():
                    send_email(receiver_email, "HOMEWORK DUE TODAY", event_description)

       

# List of Assignments
assignments = [
    (2023, 9, 23, 'exam', 'Midterm Exam'),
    (2023, 9, 23, 'quiz', 'Quiz 1'),
    (2023, 9, 23, 'homework', 'Homework 3'),
    (2023, 8, 13, 'homework', 'Homework 17'),
]

receiver_email = 'michaelkerley07@gmail.com'

send_assignment_notif(assignments, receiver_email)


#c = calendar.TextCalendar(calendar.SUNDAY)
#str = c.formatmonth(2025, 1)
#print(str)

 

