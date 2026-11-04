import src.repositories.usuarios as usuarios_repository


def modificar_perfil(id_usuario, datos):

    perfil = usuarios_repository.actualizar_perfil(id_usuario, datos)

    return perfil