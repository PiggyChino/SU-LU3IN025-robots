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
    
def hateBot(robotId, sensors): #evite les robots
	translation = 1 * sensors["sensor_front"]["distance_to_robot"]
	mid = (-1) * sensors["sensor_left"]["distance_to_robot"] + (1) * sensors["sensor_right"]["distance_to_robot"]
	front = (-1) * sensors["sensor_front_left"]["distance_to_robot"] + (1) * sensors["sensor_front_right"]["distance_to_robot"]
	counter_perp = (-1) * sensors["sensor_front"]["distance_to_robot"] + (1) * sensors["sensor_back"]["distance_to_robot"]
	rotation =  mid + front + counter_perp

    # limite les valeurs de sortie entre -1 et +1
	translation = max(-1,min(translation,1))
	rotation = max(-1, min(rotation, 1))
    
	return translation, rotation


def avoider(robotId, sensors): #se balade en évitant les murs et robots
	sensors = get_extended_sensors(sensors)
	translation = 1 * sensors["sensor_front"]["distance"]
	rotation = (-1) * sensors["sensor_front_left"]["distance"] + 1 * sensors["sensor_front_right"]["distance"] \
            + (-1) * sensors["sensor_front"]["distance_to_wall"] + 1 * sensors["sensor_front"]["distance_to_robot"] \
            + (-1) * sensors["sensor_left"]["distance"] + 1 * sensors["sensor_right"]["distance"]

    # limite les valeurs de sortie entre -1 et +1
	translation = max(-1,min(translation,1))
	rotation = max(-1, min(rotation, 1))

	return translation, rotation


def hateWall(robotId, sensors): #evite les murs
	sensors = get_extended_sensors(sensors)
	translation = 1 * sensors["sensor_front"]["distance_to_wall"]
	rotation = (-1) * sensors["sensor_front_left"]["distance"] + 1 * sensors["sensor_front_right"]["distance"] \
            + (-1) * sensors["sensor_front"]["distance_to_wall"] + 1 * sensors["sensor_front"]["distance_to_robot"] \
            + (-1) * sensors["sensor_left"]["distance"] + 1 * sensors["sensor_right"]["distance"]

    # limite les valeurs de sortie entre -1 et +1
	translation = max(-1,min(translation,1))
	rotation = max(-1, min(rotation, 1))

	return translation, rotation
	
	
def enemy_around(sensors) : #vérifie si un robot adverse est proche
	if sensors["sensor_front_left"]["distance_to_wall"] < 1 :
		return True
	if sensors["sensor_front_right"]["distance_to_wall"] < 1 :
		return True
	else :
		return False
		


def loveBot(robotId, sensors): #suit les robots adverses
	# comportement: suit les robots ennemis
	if enemy_around(sensors) :
		rotation = (-1) * sensors["sensor_front_right"]["distance_to_robot"] + 1 * sensors["sensor_front_left"]["distance_to_robot"] + \
		1 * sensors["sensor_front_right"]["distance_to_wall"] + (-1) * sensors["sensor_front_left"]["distance_to_wall"]
		return 1, rotation
	for s in sensors :
		if sensors[s]["distance_to_wall"] < 0.05 : #si proche d'un mur, adopte le comportement qui évite les murs
			return hateWall(robotId, sensors)
	else:
		return avoider(robotId, sensors)
	
	
	
def hate_ally(sensors) :
    # comportement : evite les allies
    # renvoie la valeur de rotation : pos -> tourne a droite, neg -> tourne a gauche 
	mid = (-1) * sensors["sensor_left"]["distance_to_robot"] + (1) * sensors["sensor_right"]["distance_to_robot"]
	front = (-1) * sensors["sensor_front_left"]["distance_to_robot"] + (1) * sensors["sensor_front_right"]["distance_to_robot"]
	counter_perp = (-1) * sensors["sensor_front"]["distance_to_robot"] + (1) * sensors["sensor_back"]["distance_to_robot"]
	rotation =  mid + front + counter_perp
	return rotation


def ally_around_left(sensors) :
    # savoir s'il y a un allie a gauche de lui
    # return true s'il y a un mur a gauche de lui, false sinon	
	if sensors["sensor_front"]["isSameTeam"] or sensors["sensor_front_left"]["isSameTeam"] or sensors["sensor_front_right"]["isSameTeam"] :
		if sensors["sensor_front"]["distance_to_robot"] < 0.3 :
			return True
		if sensors["sensor_front_left"]["distance_to_robot"] < 0.5 :
			return True
		if sensors["sensor_left"]["distance_to_robot"] < 0.3 :
			return True
		if sensors["sensor_back_left"]["distance_to_robot"] < 0.5 :
			return True
	return False


"""-----------------------------------------------------"""

def wall_around_right(sensors) : #savoir s'il y a un mur a droite de lui
    # return true s'il y a un mur a droite de lui, false sinon	
    if sensors["sensor_front"]["distance_to_wall"] < 0.3 :
        return True
    if sensors["sensor_front_right"]["distance_to_wall"] < 0.5 :
        return True
    if sensors["sensor_right"]["distance_to_wall"] < 0.3 :
        return True
    return False

def hate_wall_right(sensors) : #evite les murs qui sont a droite
	# renvoie la valeur de rotation : pos -> tourne a droite, neg -> tourne a gauche 
	mid = (-1) * sensors["sensor_left"]["distance_to_wall"] + (1) * sensors["sensor_right"]["distance_to_wall"]
	front = (-1) * sensors["sensor_front_left"]["distance_to_wall"] + (1) * sensors["sensor_front_right"]["distance_to_wall"]
	counter_perp = (1) * sensors["sensor_front"]["distance_to_wall"] + (-1) * sensors["sensor_back"]["distance_to_wall"]
	rotation =  mid + front + counter_perp
	return 0.2 * rotation


def love_wall(sensors) : #se dirige vers les murs
	# renvoie la valeur de rotation : pos -> tourne a droite, neg -> tourne a gauche
	mid = (1) * sensors["sensor_left"]["distance_to_wall"] + (-1) * sensors["sensor_right"]["distance_to_wall"]
	back = (1) * sensors["sensor_back_left"]["distance_to_wall"] + (-1) * sensors["sensor_back_right"]["distance_to_wall"]
	rotation =  mid + back
	return 2*rotation

def follow_wall_right(sensors) : #longe les murs du cote droit
	# renvoie la valeur de rotation : pos -> tourne a droite, neg -> tourne a gauche
	if not wall_around_right(sensors) :
		rotation = love_wall(sensors)
	else :
		rotation = hate_wall_right(sensors)
	return rotation

def right_wall_follower(robotId, sensors) : #longer les murs a droite de lui
    # renvoie la valeur de rotation : pos -> tourne a droite, neg -> tourne a gauche
	if ally_around_left(sensors) :
		rotation = hate_ally(sensors)
		rotation = max(-1, min(rotation, 1))
		return 1, rotation
	rotation = follow_wall_right(sensors)
	return 1, rotation
	
"""----------------------------------------------------------------"""	
	
	
def perturbateur(robotId, sensors): #evite tous sauf les adverses
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


def aleatoire(robotId, sensors): #aleatoire
	if uniqint % 30 == 0 :
		rotation = random.randint(-1, 1) * sensors["sensor_front_left"]["distance_to_wall"] + random.randint(-1, 1) *sensors["sensor_front_right"]["distance_to_wall"]
		return 1, rotation
	return avoider(robotId, sensors)
	
	
def force(robotId, sensors): #force le passage
	#Si un robot adverse se trouve devant lui, il continue d'avancer et ne fait aucune rotation
	if sensors["sensor_front"]["isRobot"] == True and sensors["sensor_front"]["isSameTeam"] == False:
		return 1, 0 
	if uniqint % 30 < 5:
		return base(robotId, sensors)
	return hateWall(robotId, sensors)
    
	


def base(robotId, sensors): #robot de base
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

	match (robotId %8):
		
		case 0 : #perturbateur
		
			return perturbateur(robotId, sensors)
		
		case 7 | 4 : #stalker
			return loveBot(robotId, sensors)
				
		case 2 | 3 | 6: #force le passage
			if robotId == 2 and uniqint > 3000:
				return perturbateur(robotId, sensors)
			return force(robotId, sensors)
		
		case 5 : #aleatoire
			return aleatoire(robotId, sensors)
			
		case 1 : #suit le mur droit
			if uniqint > 3000:
				return avoider(robotId, sensors)
			return right_wall_follower(robotId, sensors)
			
