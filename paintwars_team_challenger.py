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
	rotation = (-1) * sensors["sensor_front_left"]["distance"] + 1 * sensors["sensor_front_right"]["distance"] \
            + (-1) * sensors["sensor_front"]["distance_to_wall"] + 1 * sensors["sensor_front"]["distance_to_robot"] \
            + (-1) * sensors["sensor_left"]["distance"] + 1 * sensors["sensor_right"]["distance"]

    # limite les valeurs de sortie entre -1 et +1
	translation = max(-1,min(translation,1))
	rotation = max(-1, min(rotation, 1))
    
	return translation, rotation


def avoider(robotId, sensors):
	sensors = get_extended_sensors(sensors)
	translation = 1 * sensors["sensor_front"]["distance"]
	rotation = (-1) * sensors["sensor_front_left"]["distance"] + 1 * sensors["sensor_front_right"]["distance"] \
            + (-1) * sensors["sensor_front"]["distance_to_wall"] + 1 * sensors["sensor_front"]["distance_to_robot"] \
            + (-1) * sensors["sensor_left"]["distance"] + 1 * sensors["sensor_right"]["distance"]

    # limite les valeurs de sortie entre -1 et +1
	translation = max(-1,min(translation,1))
	rotation = max(-1, min(rotation, 1))

	return translation, rotation


def hateWall(robotId, sensors):
	sensors = get_extended_sensors(sensors)
	translation = 1 * sensors["sensor_front"]["distance_to_wall"]
	rotation = (-1) * sensors["sensor_front_left"]["distance"] + 1 * sensors["sensor_front_right"]["distance"] \
            + (-1) * sensors["sensor_front"]["distance_to_wall"] + 1 * sensors["sensor_front"]["distance_to_robot"] \
            + (-1) * sensors["sensor_left"]["distance"] + 1 * sensors["sensor_right"]["distance"]

    # limite les valeurs de sortie entre -1 et +1
	translation = max(-1,min(translation,1))
	rotation = max(-1, min(rotation, 1))

	return translation, rotation
	
	
	
def suiveur_mur(robotId, sensors):
	if 0.1 > sensors["sensor_front_left"]["distance_to_wall"] or 0.1 > sensors["sensor_front_right"]["distance_to_wall"]:
		return 1, 1
	if 0.1 > sensors["sensor_left"]["distance_to_wall"] or 0.1 > sensors["sensor_right"]["distance_to_wall"]:
		return 1, 0.25
	if 1 == sensors["sensor_right"]["distance_to_wall"] and 1 == sensors["sensor_front"]["distance_to_wall"]: #si rien devant et a droite, avance
		return 0.9 , 0.5
			
	if 1 > sensors["sensor_front"]["distance_to_wall"]: #si mur devant, tourne a gauche
		return 0.05 , -1

	return 1, 0
	
	
	
def perturbateur(robotId, sensors):
	if sensors["sensor_front"]["isRobot"] == True and sensors["sensor_front"]["isSameTeam"] == True: #evite les alliés et les murs
		if sensors["sensor_front_right"]["distance_to_robot"] and sensors["sensor_front_left"]["distance_to_robot"]:
			return hateBot(robotId, sensors)
		if sensors["sensor_front_right"]["distance_to_wall"] and sensors["sensor_front_left"]["distance_to_wall"]:
			return hateWall(robotId, sensors)
	if sensors["sensor_front"]["distance_to_wall"]:
		return hateWall(robotId, sensors)	
		
	if sensors["sensor_right"] and sensors["sensor_left"]:
		return 0, -0.7			
	return avoider(robotId, sensors)


def aleatoire(robotId, sensors):
	if uniqint % 30 == 0 :
		rotation = random.randint(-1, 1) * sensors["sensor_front_left"]["distance_to_wall"] + random.randint(-1, 1) *sensors["sensor_front_right"]["distance_to_wall"]
		return 1, rotation
	return avoider(robotId, sensors)
	
	
def force(robotId, sensors):
	if sensors["sensor_front"]["isRobot"] == True and sensors["sensor_front"]["isSameTeam"] == False:
		return 1, 0
	if uniqint % 30 < 5:
		return base(robotId, sensors)
	return hateWall(robotId, sensors)
    
	


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

	uniqint += 1
	if sensors["sensor_front"]["isRobot"] == True and sensors["sensor_front"]["isSameTeam"] == True and (sensors["sensor_front"]["distance_to_robot"] < 0.2 or sensors["sensor_front_right"]["distance_to_robot"] < 0.2 or sensors["sensor_front_left"]["distance_to_robot"] < 0.2): #evite les alliés et les murs
		return avoider(robotId, sensors)
	if uniqint % 2000 == 0:
		robotId += 2
	match (robotId %8):
		
		case 0 | 6 : #subsomption, perturbateur				
			return perturbateur(robotId, sensors)
		
		case 1 | 4: #aleatoire périodique
			return aleatoire(robotId, sensors)
				
		case 2 | 3 : #force le passage
			return force(robotId, sensors)
			
		case 7 : 
			return suiveur_mur(robotId, sensors)
			
		case 5:
			return base(robotId, sensors)

