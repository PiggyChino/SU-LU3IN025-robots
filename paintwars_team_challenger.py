# Projet "robotique" IA&Jeux 2021
#
# Binome:
#  Gautier Cai: 21100696
#  Aghiles Kahil: 21110119

import random 

def get_team_name():
	return "Les binômes" # à compléter (comme vous voulez)

def get_extended_sensors(sensors):
    for key in sensors:
        sensors[key]["distance_to_robot"] = 1.0
        sensors[key]["distance_to_wall"] = 1.0
        if sensors[key]["isRobot"] == True:
            sensors[key]["distance_to_robot"] = sensors[key]["distance"]
        else:
            sensors[key]["distance_to_wall"] = sensors[key]["distance"]
    return sensors
    
def hateBot(robotId, sensors):
	sensors = get_extended_sensors(sensors)

    # contrôle moteur. Ecrivez votre comportement de Braitenberg ci-dessous.
    # il est possible de répondre à toutes les questions en utilisant seulement:
    #   sensors["sensor_front"]["distance_to_wall"]
    #   sensors["sensor_front"]["distance_to_robot"]
    #   sensors["sensor_front_left"]["distance_to_wall"]
    #   sensors["sensor_front_left"]["distance_to_robot"]
    #   sensors["sensor_front_right"]["distance_to_wall"]
    #   sensors["sensor_front_right"]["distance_to_robot"]

	translation = 1 * sensors["sensor_front"]["distance_to_robot"]
	rotation = (-1) * sensors["sensor_front_left"]["distance_to_robot"] + (1) * sensors["sensor_front_right"]["distance_to_robot"]

    # limite les valeurs de sortie entre -1 et +1
	translation = max(-1,min(translation,1))
	rotation = max(-1, min(rotation, 1))
    
	return translation, rotation


def avoider(robotId, sensors):
	sensors = get_extended_sensors(sensors)
	translation = 1 * sensors["sensor_front"]["distance"]
	rotation = (-1) * sensors["sensor_front_left"]["distance"] + (1) * sensors["sensor_front_right"]["distance"]

    # limite les valeurs de sortie entre -1 et +1
	translation = max(-1,min(translation,1))
	rotation = max(-1, min(rotation, 1))

	return translation, rotation


def hateWall(robotId, sensors):
	sensors = get_extended_sensors(sensors)
	translation = 1 * sensors["sensor_front"]["distance_to_wall"]
	rotation = (-1) * sensors["sensor_front_left"]["distance_to_wall"] + (1) * sensors["sensor_front_right"]["distance_to_wall"]

    # limite les valeurs de sortie entre -1 et +1
	translation = max(-1,min(translation,1))
	rotation = max(-1, min(rotation, 1))

	return translation, rotation
	
	
def loveBot(robotId, sensors):
	translation = 1 * sensors["sensor_front"]["distance_to_robot"]
	rotation = (1) * sensors["sensor_front_left"]["distance_to_robot"] + (-1) * sensors["sensor_front_right"]["distance_to_robot"]

    # limite les valeurs de sortie entre -1 et +1
	translation = max(-1,min(translation,1))
	rotation = max(-1, min(rotation, 1))

	return translation, rotation


def base(robotId, sensors):
	translation = 1
	rotation = 0
	if sensors["sensor_front_left"]["distance"] < 1 or sensors["sensor_front"]["distance"] < 1:
		rotation = 0.5
	elif sensors["sensor_front_right"]["distance"] < 1:
		rotation = -0.5
	return translation, rotation
			
uniqint = 0

def step(robotId, sensors):
	global uniqint
	translation = 1 # vitesse de translation (entre -1 et +1)
	rotation = 0 # vitesse de rotation (entre -1 et +1)
	sensors = get_extended_sensors(sensors)
	"""
	if sensors["sensor_front_left"]["distance"] < 1 or sensors["sensor_front"]["distance"] < 1:
		rotation = 0.5  # rotation vers la droite
	elif sensors["sensor_front_right"]["distance"] < 1:
		rotation = -0.5  # rotation vers la gauche
        
    
	if sensors["sensor_front"]["isRobot"] == True and sensors["sensor_front"]["isSameTeam"] == False:
		enemy_detected_by_front_sensor = True # exemple de détection d'un robot de l'équipe adversaire (ne sert à rien)
	"""
	uniqint += 1
	if sensors["sensor_front"]["isRobot"] == True and sensors["sensor_front"]["isSameTeam"] == True and (sensors["sensor_front"]["distance_to_robot"] < 0.2 or sensors["sensor_front_right"]["distance_to_robot"] < 0.2 or sensors["sensor_front_left"]["distance_to_robot"] < 0.2): #evite les alliés et les murs
		return 0, 1
	match (robotId%8):
		
		case 0 | 6 : #subsomption, perturbateur				
			if sensors["sensor_front"]["isRobot"] == True and sensors["sensor_front"]["isSameTeam"] == True: #evite les alliés et les murs
				if sensors["sensor_front_right"]["distance_to_robot"] and sensors["sensor_front_left"]["distance_to_robot"]:
					return hateBot(robotId, sensors)
				if sensors["sensor_front_right"]["distance_to_wall"] and sensors["sensor_front_left"]["distance_to_wall"]:
					return hateWall(robotId, sensors)
			if sensors["sensor_front"]["distance_to_wall"]:
				return hateWall(robotId, sensors)	
				
			if sensors["sensor_right"] and sensors["sensor_left"]:
				return 0, -0.7
				
			return base(robotId, sensors)
		
			
			
		case 1 | 4: #aleatoire périodique
			if uniqint % 30 == 0 :
				rotation = random.randint(-1, 1) * sensors["sensor_front_left"]["distance_to_wall"] + random.randint(-1, 1) *sensors["sensor_front_right"]["distance_to_wall"]
				return 1, rotation
			return base(robotId, sensors)
			
			
			
			
		case 3 : #force le passage
			if sensors["sensor_front"]["isRobot"] == True and sensors["sensor_front"]["isSameTeam"] == False:
				return avoider(robotId, sensors)
			elif uniqint % 30 < 5:
				return base(robotId, sensors)
			return hateWall(robotId, sensors)
			
		
			
			
		case 2:
			if (0 == sensors["sensor_front"]["distance"]) and (0 == sensors["sensor_left"]["distance"]):
				return 1, 0.5
			if (0 == sensors["sensor_front"]["distance"]) and (0 == sensors["sensor_right"]["distance"]):
				return 1, -0,5
			if (True == sensors["sensor_back"]["isRobot"]) and (False == sensors["sensor_back"]["isSameTeam"]):
				return 1, 1
			return base(robotId, sensors)
			
			
			
		case 7 : #longeur de mur
			if 0.1 > sensors["sensor_front_left"]["distance_to_wall"] or 0.1 > sensors["sensor_front_right"]["distance_to_wall"]:
				return 1, 1
			if 0.1 > sensors["sensor_left"]["distance_to_wall"] or 0.1 > sensors["sensor_right"]["distance_to_wall"]:
				return 1, 0.25
			if 1 == sensors["sensor_right"]["distance_to_wall"] and 1 == sensors["sensor_front"]["distance_to_wall"]: #si rien devant et a droite, avance
				return 0.9 , 0.5
			
			if 1 > sensors["sensor_front"]["distance_to_wall"]: #si mur devant, tourne a gauche
				return 0.05 , -1

			return 1, 0
			
			
		case 4 | 5:
			return base(robotId, sensors)

