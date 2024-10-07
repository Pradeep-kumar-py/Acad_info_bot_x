import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Initialize the bot with your token
bot = telebot.TeleBot("7661028804:AAFxiZ0CQlpv3aNGwgIuF4CEjL6dlsZd3sY")

# Dictionary to store contact details of the faculty
faculty_contacts = {
    'ASGE': {
        'Head of Department': 'Dr. Ganesh Mundhe\nEmail: gmundhe@aitpune.edu.in',
        'Teaching': {
            'Dr. (Mrs) Swati Kulkarni': 'Email: skulkarni@aitpune.edu.in',
            'Mr. V. Hivrale': 'Email: vhivrale@aitpune.edu.in'
        },
        'Non-Teaching': {
            'Mr. Raghu Babar': 'Email: rbabar@aitpune.edu.in',
            'Ms. Swati Salunkhe': 'Email: ssalunkhe@aitpune.edu.in'
        }
    },
    'Computer': {
        'Head of Department': 'Prof. (Dr.) S R Dhore\nEmail: hodcomp@aitpune.edu.in',
        'Teaching': {
            'Mr. Kuldeep Hule': 'Email: kuldeephule@aitpune.edu.in',
            'Mrs. Asha Sathe': 'Email: asathe@aitpune.edu.in'
        },
        'Non-Teaching': {
            'Mr. Ravindindra Desai': 'Email: rdesai@aitpune.edu.in',
            'Ms. Priyanka Holkar': 'Email: priyankaholkar@aitpune.edu.in'
        }
    },
    'IT': {
        'Head of Department': 'Dr. (Mrs) Sangeeta Jadhav\nEmail: hodit@aitpune.edu.in',
        'Teaching': {
            'Dr. Rahul Desai': 'Email: rahuldesai@aitpune.edu.in',
            'Dr. Ashwini Sapkal': 'Email: asapkal@aitpune.edu.in'
        },
        'Non-Teaching': {
            'Ms. Jyoti Taralkar': 'Email: jyoti@aitpune.edu.in',
            'Mr. Suryakant Kenjale': 'Email: suryakantkenjale@aitpune.edu.in'
        }
    },
    'ENTC': {
        'Head of Department': 'Dr. G R Patil\nEmail: hodetc@aitpune.edu.in',
        'Teaching': {
            'Dr. P B Karandikar': 'Email: pkarandikar@aitpune.edu.in',
            'Dr. Shraddha Oza': 'Email: sdoza@aitpune.edu.in'
        },
        'Non-Teaching': {
            'Mrs. Sujata Kadam': 'Email: skadam@aitpune.edu.in',
            'Mr. Bhikaji Gadekar': 'Email: bhikajigadekar@aitpune.edu.in'
        }
    },
    'Mechanical': {
        'Head of Department': 'Prof (Dr) UV Awasarmol\nEmail: hodmech@aitpune.edu.in',
        'Teaching': {
            'Mr. V R Kulkarni': 'Email: vrkulkarni@aitpune.edu.in',
            'Dr. J D Patil': 'Email: jdpatil@aitpune.edu.in'
        },
        'Non-Teaching': {
            'Mr. A G Jirgale': 'Email: agjirgale@aitpune.edu.in',
            'Mr. S H Karande': 'Email: shkarande@aitpune.edu.in'
        }
    }
}

# State variables
user_data = {}

# Function to create custom keyboard with buttons
def create_keyboard(options):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for option in options:
        markup.add(KeyboardButton(option))
    return markup

# Start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome! Please select a department:", 
                     reply_markup=create_keyboard(faculty_contacts.keys()))
    user_data[message.chat.id] = {}

# Handle department selection
@bot.message_handler(func=lambda message: message.text in faculty_contacts.keys())
def select_department(message):
    department = message.text
    user_data[message.chat.id]['department'] = department
    bot.send_message(message.chat.id, f"You selected {department}. Please select the type of staff:", 
                     reply_markup=create_keyboard(['Head of Department', 'Teaching', 'Non-Teaching']))

# Handle staff type selection
@bot.message_handler(func=lambda message: message.text in ['Head of Department', 'Teaching', 'Non-Teaching'])
def select_staff_type(message):
    staff_type = message.text
    chat_id = message.chat.id
    user_data[chat_id]['staff_type'] = staff_type
    
    department = user_data[chat_id]['department']
    
    if staff_type == 'Head of Department':
        contact = faculty_contacts[department]['Head of Department']
        bot.send_message(chat_id, f"Contact details:\n{contact}")
    else:
        staff_list = faculty_contacts[department][staff_type].keys()
        bot.send_message(chat_id, f"Please select a faculty member:", 
                         reply_markup=create_keyboard(staff_list))

# Handle faculty member selection
@bot.message_handler(func=lambda message: any(message.text in faculty_contacts[dept][type_].keys() for dept in faculty_contacts for type_ in ['Teaching', 'Non-Teaching']))
def select_faculty_member(message):
    chat_id = message.chat.id
    department = user_data[chat_id]['department']
    staff_type = user_data[chat_id]['staff_type']
    faculty_member = message.text
    
    contact = faculty_contacts[department][staff_type][faculty_member]
    bot.send_message(chat_id, f"Contact details:\n{contact}\nDo you need further assistance? (yes/no)", 
                     reply_markup=create_keyboard(['Yes', 'No']))

# Handle further assistance
@bot.message_handler(func=lambda message: message.text.lower() in ['yes', 'no'])
def further_assistance(message):
    if message.text.lower() == 'yes':
        bot.send_message(message.chat.id, "Please select a department:", 
                         reply_markup=create_keyboard(faculty_contacts.keys()))
    else:
        # Remove the custom keyboard when the session ends
        bot.send_message(message.chat.id, "Thank you for using the bot! Goodbye.", 
                         reply_markup=ReplyKeyboardRemove())

# Start the bot
bot.polling()
