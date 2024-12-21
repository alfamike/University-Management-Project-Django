from registration_app.services_fabric.services_fabric import get_fabric_client


def create_student_course_grade(grade_data):
    fabric_client = get_fabric_client()

    # Cargar el canal y la identidad del usuario
    channel = fabric_client.get_channel('mychannel')
    admin_user = fabric_client.get_user('Org1', 'Admin')

    student_id = grade_data['student_id']
    course_id = grade_data['course_id']
    grade = grade_data['grade']

    response = channel.chaincode_invoke(
        requestor=admin_user,
        channel_name='mychannel',
        chaincode_name='mycc',  # Nombre de tu Chaincode
        fcn='CreateStudentCourseGrade',  # Función en el Chaincode
        args=[student_id, course_id, str(grade)],
        transient_map={},
        wait_for_event=True
    )

    return response


def query_student_course_grade(student_id, course_id):
    fabric_client = get_fabric_client()

    # Cargar el canal y la identidad del usuario
    channel = fabric_client.get_channel('mychannel')
    admin_user = fabric_client.get_user('Org1', 'Admin')

    response = channel.chaincode_query(
        requestor=admin_user,
        channel_name='mychannel',
        chaincode_name='mycc',  # Nombre de tu Chaincode
        fcn='QueryStudentActivityGrade',  # Función en el Chaincode
        args=[student_id, course_id]
    )

    return response


def update_student_course_grade(student_id, course_id, new_grade):
    fabric_client = get_fabric_client()

    # Cargar el canal y la identidad del usuario
    channel = fabric_client.get_channel('mychannel')
    admin_user = fabric_client.get_user('Org1', 'Admin')

    response = channel.chaincode_invoke(
        requestor=admin_user,
        channel_name='mychannel',
        chaincode_name='mycc',  # Nombre de tu Chaincode
        fcn='UpdateStudentActivityGrade',  # Función en el Chaincode
        args=[student_id, course_id, str(new_grade)],
        transient_map={},
        wait_for_event=True
    )

    return response


def get_all_student_course_grades(student_id):
    fabric_client = get_fabric_client()

    # Cargar el canal y la identidad del usuario
    channel = fabric_client.get_channel('mychannel')
    admin_user = fabric_client.get_user('Org1', 'Admin')

    response = channel.chaincode_query(
        requestor=admin_user,
        channel_name='mychannel',
        chaincode_name='mycc',  # Nombre de tu Chaincode
        fcn='GetAllStudentCourseGrades',  # Función en el Chaincode
        args=[student_id]
    )

    return response


def get_student_course_grades(student_id):
    fabric_client = get_fabric_client()

    # Cargar el canal y la identidad del usuario
    channel = fabric_client.get_channel('mychannel')
    admin_user = fabric_client.get_user('Org1', 'Admin')

    response = channel.chaincode_query(
        requestor=admin_user,
        channel_name='mychannel',
        chaincode_name='mycc',  # Nombre de tu Chaincode
        fcn='GetStudentCourseGrades',  # Función en el Chaincode
        args=[student_id]
    )

    return response
