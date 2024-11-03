import requests

FABRIC_API_URL = 'http://localhost:port'  # URL de tu API de Hyperledger Fabric


def register_student_in_fabric(student_id, name, grade):
    payload = {
        'student_id': student_id,
        'name': name,
        'grade': grade,
    }
    response = requests.post(f'{FABRIC_API_URL}/register_student', json=payload)
    return response.json()


def get_student_record_from_fabric(student_id):
    response = requests.get(f'{FABRIC_API_URL}/student/{student_id}')
    return response.json()
