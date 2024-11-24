from registration_app.services_fabric.services_fabric import get_fabric_client


def create_title(title_data):
    fabric_client = get_fabric_client()

    # Cargar el canal y la identidad del usuario
    channel = fabric_client.get_channel('mychannel')
    admin_user = fabric_client.get_user('Org1', 'Admin')

    title_id = title_data['id']
    name = title_data['name']
    description = title_data['description']

    response = channel.chaincode_invoke(
        requestor=admin_user,
        channel_name='mychannel',
        chaincode_name='mycc',  # Nombre de tu Chaincode
        fcn='CreateTitle',  # Función en el Chaincode
        args=[title_id, name, description],
        transient_map={},
        wait_for_event=True
    )

    return response


def query_title(title_id):
    fabric_client = get_fabric_client()

    # Cargar el canal y la identidad del usuario
    channel = fabric_client.get_channel('mychannel')
    admin_user = fabric_client.get_user('Org1', 'Admin')

    response = channel.chaincode_query(
        requestor=admin_user,
        channel_name='mychannel',
        chaincode_name='mycc',  # Nombre de tu Chaincode
        fcn='QueryTitle',  # Función en el Chaincode
        args=[title_id]
    )

    return response


def update_title(title_id, new_name, new_description):
    fabric_client = get_fabric_client()

    # Cargar el canal y la identidad del usuario
    channel = fabric_client.get_channel('mychannel')
    admin_user = fabric_client.get_user('Org1', 'Admin')

    response = channel.chaincode_invoke(
        requestor=admin_user,
        channel_name='mychannel',
        chaincode_name='mycc',  # Nombre de tu Chaincode
        fcn='UpdateTitle',  # Función en el Chaincode
        args=[title_id, new_name, new_description],
        transient_map={},
        wait_for_event=True
    )

    return response


def get_all_titles():
    fabric_client = get_fabric_client()

    # Cargar el canal y la identidad del usuario
    channel = fabric_client.get_channel('mychannel')
    admin_user = fabric_client.get_user('Org1', 'Admin')

    response = channel.chaincode_query(
        requestor=admin_user,
        channel_name='mychannel',
        chaincode_name='mycc',  # Nombre de tu Chaincode
        fcn='GetAllTitles',  # Función en el Chaincode
        args=[]
    )

    return response
