# Projet "robotique" IA&Jeux 2021
#
# Binome:
#  Gautier Cai: 21100696
#  Aghiles Kahil: 21110119

def get_team_name():
	return "Les binômes" # à compléter (comme vous voulez)

def step(robotId, sensors):
	translation = 1 # vitesse de translation (entre -1 et +1)
	rotation = 0 # vitesse de rotation (entre -1 et +1)

	if sensors["sensor_front_left"]["distance"] < 1 or sensors["sensor_front"]["distance"] < 1:
		rotation = 0.5  # rotation vers la droite
	elif sensors["sensor_front_right"]["distance"] < 1:
		rotation = -0.5  # rotation vers la gauche
        
    
	if sensors["sensor_front"]["isRobot"] == True and sensors["sensor_front"]["isSameTeam"] == False:
		enemy_detected_by_front_sensor = True # exemple de détection d'un robot de l'équipe adversaire (ne sert à rien)
        
	if robotId < 2:
		translation = 1 * sensors["sensor_front"]["distance"]
		rotation = (-1) * sensors["sensor_front_left"]["distance"] + (1) * sensors["sensor_front_right"]["distance"]

		# limite les valeurs de sortie entre -1 et +1
		translation = max(-1,min(translation,1))
		rotation = max(-1, min(rotation, 1))
        
        
	#if sensors["sensor_front_left"]["isRobot"] == True and sensors["sensor_front_left"]["isSameTeam"] == False:
	#	rotation = (1) * sensors["sensor_front_left"]["isRobot"]
	return translation, rotation
