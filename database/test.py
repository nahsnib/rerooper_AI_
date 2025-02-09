from Basecharacter import get_Basecharacter_by_id

character = get_Basecharacter_by_id(1)
print(character.anxiety_threshold,character.initial_location)  # BaseCharacter(id=1, name='小明', initial_location='醫院', friendly_abilities=['陰謀', '偵探', '破案'])