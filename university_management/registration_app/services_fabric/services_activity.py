from registration_app.services_fabric.services_fabric import get_fabric_client


def create_activity(activity_data):
    fabric_client = get_fabric_client()

    # Cargar el canal y la identidad del usuario
    channel = fabric_client.get_channel('mychannel')
    admin_user = fabric_client.get_user('Org1', 'Admin')

    # Preparar los argumentos para invocar el Chaincode
    activity_id = activity_data['id']
    course_id = activity_data['course_id']
    name = activity_data['name']
    description = activity_data['description']
    due_date = activity_data['due_date']

    # Invocar la función 'CreateActivity' del Chaincode
    response = channel.chaincode_invoke(
        requestor=admin_user,
        channel_name='mychannel',
        chaincode_name='mycc',  # Nombre de tu Chaincode
        fcn='CreateActivity',  # Función en el Chaincode
        args=[activity_id, course_id, name, description, due_date],
        transient_map={},
        wait_for_event=True
    )

    return response


def query_activity(activity_id):
    fabric_client = get_fabric_client()

    # Cargar el canal y la identidad del usuario
    channel = fabric_client.get_channel('mychannel')
    admin_user = fabric_client.get_user('Org1', 'Admin')

    # Consultar el Chaincode para obtener una Activity
    response = channel.chaincode_query(
        requestor=admin_user,
        channel_name='mychannel',
        chaincode_name='mycc',  # Nombre de tu Chaincode
        fcn='QueryActivity',  # Función en el Chaincode
        args=[activity_id]
    )

    return response


def update_activity(activity_id, new_name, new_description, new_due_date):
    fabric_client = get_fabric_client()

    # Cargar el canal y la identidad del usuario
    channel = fabric_client.get_channel('mychannel')
    admin_user = fabric_client.get_user('Org1', 'Admin')

    # Invocar la función 'UpdateActivity' del Chaincode
    response = channel.chaincode_invoke(
        requestor=admin_user,
        channel_name='mychannel',
        chaincode_name='mycc',  # Nombre de tu Chaincode
        fcn='UpdateActivity',  # Función en el Chaincode
        args=[activity_id, new_name, new_description, new_due_date],
        transient_map={},
        wait_for_event=True
    )

    return response


def get_all_activities():
    fabric_client = get_fabric_client()

    # Cargar el canal y la identidad del usuario
    channel = fabric_client.get_channel('mychannel')
    admin_user = fabric_client.get_user('Org1', 'Admin')

    # Consultar el Chaincode para obtener todas las actividades
    response = channel.chaincode_query(
        requestor=admin_user,
        channel_name='mychannel',
        chaincode_name='mycc',  # Nombre de tu Chaincode
        fcn='GetAllActivities',  # Función en el Chaincode
        args=[]  # No es necesario pasar parámetros
    )

    # Retornar la respuesta (debe ser una lista de actividades en formato JSON o similar)
    return response
