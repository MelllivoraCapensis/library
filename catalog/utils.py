def compare_ordered_querysets(qs1, qs2):
	if len(qs1) != len(qs2):
		return False
	for obj1, obj2 in zip(qs1, qs2):
		print(obj1, obj2)
		if(str(obj1) != str(obj2)):
			return False
	return True

def get_unique_name(name_set):
	base_name = 'new_user'
	name = base_name
	i = 0
	while name in name_set:
		name = base_name + '_' + str(i)
		i += 1
	return name




