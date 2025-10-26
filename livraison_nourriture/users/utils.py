import secrets
import string

ALPHANUM=string.ascii_uppercase+string.digits+string.ascii_lowercase

def generate_code(length:int=10) -> str:
    return ''.join(secrets.choice(ALPHANUM) for _ in range(length))
def get_unique_code_for_model(model,field_name: str="code",length: int=10, tries:int=20):
    for _ in range(tries):
        candidate=generate_code(length)
        if not model.objects.filter(**{field_name:candidate}).exists():
            return candidate
    raise ValueError("Impossible de générer un code unique aprés plusieurs essais")
