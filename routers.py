

class AppDatabaseRouter:
    """
    A router to control all database operations on models
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == "students":
            return "students_db"
        elif model._meta.app_label == "library":
            return "library_db"
        return "default"

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "students":
            return "students_db"
        elif model._meta.app_label == "library":
            return "library_db"
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label in ["students", "library"] and obj2._meta.app_label in ["students", "library"]:
            return obj1._meta.app_label == obj2._meta.app_label
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        if app_label == "students":
            return db == "students_db"
        elif app_label == "library":
            return db == "library_db"

        if db in ["students_db", "library_db"]:
            return False
        return True