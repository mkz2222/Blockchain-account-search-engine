class SearchRouter:
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label == 'search':
            return 'gosql'
        else:
            return 'default'

        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label == 'search':
            return None

        else:
            return 'default'

        return None

#8/1/18 Not allow to relate
    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'search':
            return False
        # elif objl._meta.app_label == 'keyw':
        #     return False

        return None

#8/1/18 Not allow to migrate
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label == 'search':
            return None

        else:
            return db == 'default'


        return None