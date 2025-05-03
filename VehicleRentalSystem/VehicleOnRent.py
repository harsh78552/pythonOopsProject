import json


class Vehicle:
	def __init__(self, vehicle_id, brand, rent_per_hour, status):
		self.__vehicle_id = vehicle_id
		self.__brand = brand
		self.__rent_per_hour = rent_per_hour
		self.__status = status

	def addVehicleData(self):
		vehicle_data = {
			'vehicle_id': self.__vehicle_id,
			'brand': self.__brand,
			'rent_per_hour': self.__rent_per_hour,
			'status': self.__status
		}
		return vehicle_data


class Car(Vehicle):
	def __init__(self, vehicle_id, brand, rent_per_hour, model, status, car_type, fuel_type, seating_capacity,
	             transmission):
		super().__init__(vehicle_id, brand, rent_per_hour, status)
		self.car_model = model
		self.car_type = car_type
		self.fuel_type = fuel_type
		self.seating_capacity = seating_capacity
		self.transmission = transmission

	def addCarData(self):
		vehicle_data = super().addVehicleData()
		car_data = {
			'model': self.car_model,
			'car_type': self.car_type,
			'fuel_type': self.fuel_type,
			'seating_capacity': self.seating_capacity,
			'transmission': self.transmission
		}
		vehicle_data.update(car_data)

		try:
			with open("vehicle_data.json", "r") as file:
				existing_data = json.load(file)
		except FileNotFoundError:
			existing_data = []

		existing_data.append(vehicle_data)

		with open("vehicle_data.json", "w") as file:
			json.dump(existing_data, file, indent=4)
		print('Car data added successfully..')


class Bike(Vehicle):
	def __init__(self, vehicle_id, brand, rent_per_hour, status, bike_type, engine_capacity, has_helmet, gear_type):
		super().__init__(vehicle_id, brand, rent_per_hour, status)
		self.bike_type = bike_type
		self.engine_capacity = engine_capacity
		self.has_helmet = has_helmet
		self.gear_type = gear_type

	def addBikeData(self):
		vehicle_data = super().addVehicleData()
		bike_data = {'bike_type': self.bike_type, 'engine_capacity': self.engine_capacity,
		             'has_helmet': self.has_helmet, 'gear_type': self.gear_type}
		vehicle_data.update(bike_data)
		try:
			with open('vehicle_data.json', 'r') as file:
				existing_data = json.load(file)
		except FileNotFoundError:
			existing_data = []
		existing_data.append(vehicle_data)
		with open('vehicle_data.json', 'w') as file:
			json.dump(existing_data, file, indent=4)
		print('bike data added successfully..')


class VehicleInfo:
	@staticmethod
	def vehicleInfo(brand, model=None, transmission=None):
		vehicleList = []
		with open('vehicle_data.json', 'r') as file:
			vehicleData = json.load(file)
		for vehicle in vehicleData:
			if vehicle['brand'] == brand.upper() and vehicle['model'] == model and vehicle[
				'transmission'] == transmission:
				vehicleList.append(vehicle)
			elif vehicle['brand'] == brand.upper() and not model and not transmission:
				vehicleList.append(vehicle)
		return vehicleList


class VehicleUpdateOrDelete:
	@staticmethod
	def updateCarData(brand, model, status):
		with open('vehicle_data.json', 'r') as file:
			carData = json.load(file)
		for data in carData:
			if data['brand'].upper() == brand.upper() and data['model'] == model:
				data['status'] = status
				break
		with open('vehicle_data.json', 'w') as file:
			json.dump(carData, file, indent=4)
		print('status-updated successfully..')
