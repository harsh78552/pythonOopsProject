import json
import time

from VehicleRentalSystem.User import SessionValidation, ShownUser
from VehicleRentalSystem.VehicleOnRent import VehicleInfo, VehicleUpdateOrDelete


class VehicleRentalProcess:
	@staticmethod
	def viewVehicle(customer_email, brand):
		checkSessionValidation = SessionValidation.sessionValidation(customer_email)
		if checkSessionValidation:
			vehicleData = VehicleInfo.vehicleInfo(brand)
			print(json.dumps(vehicleData, indent=4))

	@staticmethod
	def rentalProcessInitialize(email, brand, model, transmission, status='ongoing'):
		checkRentalProcess = False
		User = ShownUser.showUser(email)
		checkSessionValidation = SessionValidation.sessionValidation(email)
		if checkSessionValidation:
			vehicleData = VehicleInfo.vehicleInfo(brand, model, transmission)
			try:
				with open('customerVehicleRentData.json', 'r') as file:
					customerData = json.load(file)
			except FileNotFoundError:
				customerData = []
			if vehicleData[0]['status'] == 'available':
				customerData.append(
					{'customerName': User['name'], 'email': email, 'phone_no': User['phone_no'], 'brand': brand,
					 'model': model, 'status': status, 'rentPerHourCost': vehicleData[0]['rent_per_hour'],
					 'rent_time_start': int(time.time())})
				with open('customerVehicleRentData.json', 'w') as file:
					json.dump(customerData, file, indent=4)
				print(
					f"Hello, {User['name']} I'm really glad you've chosen my platform. I'm here to help you every step of the way—enjoy the experience!")
				checkRentalProcess = True
			else:
				print(
					f'sorry,vehicle of this brand: {brand} and model: {model} is not available..You could try another..')
		if checkRentalProcess:
			VehicleUpdateOrDelete.updateCarData(brand, model, 'not-available')


class VehicleReturnProces:
	def __init__(self, userMail, brand, model):
		self.userMail = userMail
		self.brand = brand
		self.model = model

	def returnProcess(self):
		try:
			checkSessionValidation = SessionValidation.sessionValidation(self.userMail)
			if checkSessionValidation:
				with open('customerVehicleRentData.json', 'r') as file:
					customerRentData = json.load(file)
				checkRentalRecordFound = False
				rentStartTime = None
				hourCost = None
				return_time = int(time.time())
				for data in customerRentData:
					if data['email'] == self.userMail and data['brand'] == self.brand and data['model'] == self.model:
						data['status'] = 'completed'
						rentStartTime = data['rent_time_start']
						hourCost = data['rentPerHourCost']
						checkRentalRecordFound = True
						break
				if checkRentalRecordFound:
					with open('customerVehicleRentData.json', 'w') as file:
						json.dump(customerRentData, file, indent=4)
					VehicleUpdateOrDelete.updateCarData(self.brand, self.model, 'available')
					totalRentTime = abs(return_time - rentStartTime)
					totalHour = totalRentTime // 3600
					print(
						f"Vehicle returned successfully. Total rental duration: {totalHour} hours.")
					print(f"Total cost: {totalHour * hourCost}")
				else:
					print("No active rental record found for this user.")
		except Exception as error:
			print(f'error is : {str(error)}')
