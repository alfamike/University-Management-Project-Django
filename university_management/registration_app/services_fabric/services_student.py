from registration_app.services_fabric.services_fabric import get_fabric_client


def create_student(student_data):
    fabric_client = get_fabric_client()

    # Cargar el canal y la identidad del usuario
    channel = fabric_client.get_channel('mychannel')
    admin_user = fabric_client.get_user('Org1', 'Admin')

    student_id = student_data['id']
    first_name = student_data['first_name']
    last_name = student_data['last_name']
    email = student_data['email']

    response = channel.chaincode_invoke(
        requestor=admin_user,
        channel_name='mychannel',
        chaincode_name='mycc',  # Nombre de tu Chaincode
        fcn='CreateStudent',  # Función en el Chaincode
        args=[student_id, first_name, last_name, email],
        transient_map={},
        wait_for_event=True
    )

    return response


def query_student(student_id):
    fabric_client = get_fabric_client()

    # Cargar el canal y la identidad del usuario
    channel = fabric_client.get_channel('mychannel')
    admin_user = fabric_client.get_user('Org1', 'Admin')

    response = channel.chaincode_query(
        requestor=admin_user,
        channel_name='mychannel',
        chaincode_name='mycc',  # Nombre de tu Chaincode
        fcn='QueryStudent',  # Función en el Chaincode
        args=[student_id]
    )

    return response


def update_student(student_id, new_first_name, new_last_name, new_email):
    fabric_client = get_fabric_client()

    # Cargar el canal y la identidad del usuario
    channel = fabric_client.get_channel('mychannel')
    admin_user = fabric_client.get_user('Org1', 'Admin')

    response = channel.chaincode_invoke(
        requestor=admin_user,
        channel_name='mychannel',
        chaincode_name='mycc',  # Nombre de tu Chaincode
        fcn='UpdateStudent',  # Función en el Chaincode
        args=[student_id, new_first_name, new_last_name, new_email],
        transient_map={},
        wait_for_event=True
    )

    return response


def get_all_students():
    fabric_client = get_fabric_client()

    # Cargar el canal y la identidad del usuario
    channel = fabric_client.get_channel('mychannel')
    admin_user = fabric_client.get_user('Org1', 'Admin')

    response = channel.chaincode_query(
        requestor=admin_user,
        channel_name='mychannel',
        chaincode_name='mycc',  # Nombre de tu Chaincode
        fcn='GetAllStudents',  # Función en el Chaincode
        args=[]  # No es necesario pasar parámetros
    )

    return response


def get_students_by_title(title_id):
    fabric_client = get_fabric_client()

    # Cargar el canal y la identidad del usuario
    channel = fabric_client.get_channel('mychannel')
    admin_user = fabric_client.get_user('Org1', 'Admin')

    response = channel.chaincode_query(
        requestor=admin_user,
        channel_name='mychannel',
        chaincode_name='mycc',  # Nombre de tu Chaincode
        fcn='GetStudentsByTitle',  # Función en el Chaincode
        args=[title_id]
    )

    return response


def get_students_by_course(course_id):
    fabric_client = get_fabric_client()

    # Cargar el canal y la identidad del usuario
    channel = fabric_client.get_channel('mychannel')
    admin_user = fabric_client.get_user('Org1', 'Admin')

    response = channel.chaincode_query(
        requestor=admin_user,
        channel_name='mychannel',
        chaincode_name='mycc',  # Nombre de tu Chaincode
        fcn='GetStudentsByCourse',  # Función en el Chaincode
        args=[course_id]
    )

    return response
