from flask import redirect, url_for, current_app, flash
from flask_login import current_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink

# Override Model View to add role permissions
class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

# Overrida Index View to only allow admin access
class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

    # Override Menu Index Link
class MainIndexLink(MenuLink):
    def get_url(self):
        return url_for('dashboard.home')