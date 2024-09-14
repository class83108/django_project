from django.conf import settings


class DatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == "article":
            return "default"
        elif model._meta.app_label == "chat":
            return "second_db"
        else:
            return "default"

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "article":
            return "default"
        elif model._meta.app_label == "chat":
            return "second_db"
        else:
            return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """
        決定是否允許兩個對象之間建立關係。
        對於跨數據庫的關係，我們需要更精確的控制。
        """
        # 如果兩個對象在同一個數據庫，允許關係
        if obj1._state.db == obj2._state.db:
            return True

        # 其他跨數據庫的關係默認不允許
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        表示是否允許模型在指定資料庫上進行遷移操作
        """
        if app_label == "article":
            return db == "default"
        elif app_label == "chat":
            return db == "second_db"
        elif app_label == "auth":
            return db == "default"
        return None
