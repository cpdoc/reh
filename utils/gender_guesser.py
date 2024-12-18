import gender_guesser.detector as gender

def gender_guesser(nome):
    
    if not hasattr(gender_guesser, "_detector"):
        gender_guesser._detector = gender.Detector(case_sensitive=False)
        gender_guesser._mapping = {
            'male': 'Masculino',
            'mostly_male': 'Masculino',
            'unknown': 'Desconhecido',
            'female': 'Feminino',
            'mostly_female': 'Feminino'
        }
    
    d = gender_guesser._detector
    mapping = gender_guesser._mapping

    genero = d.get_gender(nome.split(' ')[0])    
    genero_corrigido = mapping.get(genero)
    
    return genero_corrigido