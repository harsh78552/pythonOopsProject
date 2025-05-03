import hashlib
import json
import time
import uuid


def generate_randomId():
	unique_id = str(uuid.uuid4())
	return unique_id


class UserRegister:
	def __init__(self, name, email, password, phone_no, license_no):
		self.__name = name
		self.__email = email
		self.__password = hashlib.sha256(password.encode()).hexdigest()
		self.__phone_no = phone_no
		self.__license_no = license_no

	def register_user(self):
		userdata = {'user_id': generate_randomId(), 'name': self.__name, 'email': self.__email,
		            'password': self.__password,
		            'phone_no': self.__phone_no,
		            'license_no': self.__license_no}
		with open('user_data.json', 'r') as file:
			existing_data = json.load(file)
		for data in existing_data:
			if data['email'] == self.__email and data['license_no'] == self.__license_no:
				print('User already exist..')
		existing_data.append(userdata)
		with open('user_data.json', 'w') as file_:
			json.dump(existing_data, file_, indent=4)
			print('user register successfully....')


class UserLogin:
	def __init__(self, email, password):
		self.email = email
		self.password = hashlib.sha256(password.encode()).hexdigest()

	def userLogin(self):
		with open('user_data.json', 'r') as file:
			existing_data = json.load(file)
		for userData in existing_data:
			if userData['email'] == self.email and userData['password'] == self.password:
				try:
					with open('session.json', 'r') as file:
						exist_user_info = json.load(file)
				except (FileNotFoundError, json.JSONDecodeError):
					exist_user_info = []
				exist_user_info.append(
					{'email': self.email, 'session_id': generate_randomId(), 'timestamp': int(time.time())})
				with open('session.json', 'w') as file:
					json.dump(exist_user_info, file, indent=4)
					print('user login successfully...')
			else:
				print('user not registered..')


class UserLogout:
	def __init__(self, userEmail):
		self.userEmail = userEmail

	def logout(self):
		session_found = False
		with open('session.json', 'r') as file:
			existing_user = json.load(file)
		for session in existing_user:
			if session['email'] == self.userEmail:
				existing_user.remove(session)
				session_found = True
				break
		if session_found:
			with open('session.json', 'w') as file:
				json.dump(existing_user, file, indent=4)
				print('Logout successful!')
		else:
			print('No active session found for this user.')


class SessionValidation:
	@staticmethod
	def sessionValidation(userEmail):
		sessionExist = False
		sessionFound = False
		try:
			with open('session.json', 'r') as file:
				session = json.load(file)
			for session_data in session:
				if session_data['email'] == userEmail:
					sessionFound = True
					session_age = int(time.time()) - session_data['timestamp']
					if session_age > 86400:
						session.remove(session_data)
						sessionExist = True
					break
			with open('session.json', 'w') as file:
				json.dump(session, file, indent=4)
			if sessionExist:
				return False
			elif sessionFound:
				return True
			else:
				return False
		except FileNotFoundError:
			return "Session data is not available."


class ShownUser:
	@staticmethod
	def showUser(email):
		with open('user_data.json', 'r') as file:
			user_data = json.load(file)
		for user_ in user_data:
			if user_['email'] == email:
				return user_
		return f"user from this  email id {email} not exist..\nregister first!!"


# user = UserRegister('Harsh Tiwari', 'harsh844509@gmail.com', 'harsh@123', '7654092577', 'Hlcs789456235')
# user.register_user()
# user = UserLogin('harsh844509@gmail.com', 'harsh@123')
# user.userLogin()
