class DBRouter:
    """ Para decirle a django que debe usar la base de datos de cada app """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'inv':
            return 'db_inv'
        return 'default'

    """ Para decirle a django que base de datos usar para guardar los datos de nuestra de aplicación """

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'inv':
            return 'db_inv'
        return 'default'

    """ Se especifica una relación entre dos elementos u objetos """

    def allow_relation(self, elem1, elem2, **hints):
        # if elem1._meta.app_label == 'app1' and elem2._meta.app_label == 'inv':
        #     return True
        return True

    """ 
        Se indica que las migraciones se deben ejecutar en la base de datos 'db_inv'
    """

    def allow_migrate(self, db, app_label, model_name, **hints):
        # if app_label == 'inv':
        #     return db == 'db_inv'
        #   return None
        return True
