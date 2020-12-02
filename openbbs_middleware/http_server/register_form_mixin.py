# -*- coding: utf-8 -*-
"""
"""

from flask_security.forms import SubmitField, get_form_field_label, inspect, _datastore

from openbbs_middleware import cfg


class RegisterFormMixin(object):

    """RegisterFormMixin for RegisterForm.

    Attributes:
        submit (TYPE): Description
    """

    submit = SubmitField(get_form_field_label("register"))

    def to_dict(self, only_user):
        """
        Return form data as dictionary
        :param only_user: bool, if True then only fields that have
        corresponding members in UserModel are returned
        :return: dict

        Args:
            only_user (TYPE): Description

        Returns:
            TYPE: Description
        """

        def is_field_and_user_attr(member):
            """is_field_and_user_attr

            Args:
                member (TYPE): Description

            Returns:
                TYPE: Description
            """
            # If only fields recorded on UserModel should be returned,
            # perform check on user model, else return True
            if only_user is True:
                return hasattr(_datastore.user_model, getattr(member, 'name', ''))
            else:
                return True

        fields = inspect.getmembers(self, is_field_and_user_attr)
        the_dict = dict((key, getattr(value, 'data', '')) for key, value in fields)

        return the_dict
