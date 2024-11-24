from registration_app.models import Title, Course
from registration_app.services_fabric.services_fabric import get_fabric_client


def create_course(course_data):
    fabric_client = get_fabric_client()

    # Cargar el canal y la identidad del usuario
    channel = fabric_client.get_channel('mychannel')
    admin_user = fabric_client.get_user('Org1', 'Admin')

    course_id = course_data['id']
    title_id = course_data['title_id']
    name = course_data['name']
    description = course_data['description']
    start_date = course_data['start_date']
    end_date = course_data['end_date']

    response = channel.chaincode_invoke(
        requestor=admin_user,
        channel_name='mychannel',
        chaincode_name='mycc',  # Nombre de tu Chaincode
        fcn='CreateCourse',  # Función en el Chaincode
        args=[course_id, title_id, name, description, start_date, end_date],
        transient_map={},
        wait_for_event=True
    )

    return response


def query_course(course_id):
    fabric_client = get_fabric_client()

    # Cargar el canal y la identidad del usuario
    channel = fabric_client.get_channel('mychannel')
    admin_user = fabric_client.get_user('Org1', 'Admin')

    response = channel.chaincode_query(
        requestor=admin_user,
        channel_name='mychannel',
        chaincode_name='mycc',  # Nombre de tu Chaincode
        fcn='QueryCourse',  # Función en el Chaincode
        args=[course_id]
    )

    return response


def update_course(course_id, new_title_id, new_name, new_description, new_start_date, new_end_date):
    fabric_client = get_fabric_client()

    # Cargar el canal y la identidad del usuario
    channel = fabric_client.get_channel('mychannel')
    admin_user = fabric_client.get_user('Org1', 'Admin')

    response = channel.chaincode_invoke(
        requestor=admin_user,
        channel_name='mychannel',
        chaincode_name='mycc',  # Nombre de tu Chaincode
        fcn='UpdateCourse',  # Función en el Chaincode
        args=[course_id, new_title_id, new_name, new_description, new_start_date, new_end_date],
        transient_map={},
        wait_for_event=True
    )

    return response


def get_all_courses():
    fabric_client = get_fabric_client()

    # Cargar el canal y la identidad del usuario
    channel = fabric_client.get_channel('mychannel')
    admin_user = fabric_client.get_user('Org1', 'Admin')

    response = channel.chaincode_query(
        requestor=admin_user,
        channel_name='mychannel',
        chaincode_name='mycc',  # Nombre de tu Chaincode
        fcn='GetAllCourses',  # Función en el Chaincode
        args=[]
    )

    return response


def get_courses_by_title(title_id):
    fabric_client = get_fabric_client()

    # Cargar el canal y la identidad del usuario
    channel = fabric_client.get_channel('mychannel')
    admin_user = fabric_client.get_user('Org1', 'Admin')

    response = channel.chaincode_query(
        requestor=admin_user,
        channel_name='mychannel',
        chaincode_name='mycc',  # Nombre de tu Chaincode
        fcn='GetCoursesByTitle',  # Función en el Chaincode
        args=[title_id]
    )

    return response
