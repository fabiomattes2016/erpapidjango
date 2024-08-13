from rest_framework.exceptions import AuthenticationFailed, APIException
from accounts.models import User
from django.contrib.auth.hashers import check_password, make_password
from companies.models import Enterprise, Employee


class Authentication:
    def signin(self, email=None, password=None) -> User:
        """
        Autentica um usuário com base no email e senha fornecidos.
        Args:
            email (str): O email do usuário.
            password (str): A senha do usuário.
        Returns:
            User: O objeto do usuário autenticado.
        Raises:
            AuthenticationFailed: Caso as credenciais sejam inválidas.
        """
        
        exception_auth: AuthenticationFailed = AuthenticationFailed("Credenciais inválidas!")
        user_exists = User.objects.filter(email=email).exists()
        
        if not user_exists:
            raise exception_auth
        
        user = User.objects.filter(email=email).first()
        
        if not check_password(password, user.password):
            raise exception_auth
        
        return user
        
    def signup(self, name, email, password, type_account='owner', company_id=False) -> User:
        """
        Registra um novo usuário no sistema.
        Args:
            name (str): O nome do usuário.
            email (str): O e-mail do usuário.
            password (str): A senha do usuário.
            type_account (str, opcional): O tipo de conta do usuário. Padrão é 'owner'.
            company_id (bool ou int, opcional): O ID da empresa associada ao usuário. Padrão é False.
        Returns:
            User: O objeto do usuário criado.
        Raises:
            APIException: Se o campo nome, e-mail ou senha forem nulos.
            APIException: Se o tipo de conta for 'employee' e o ID da empresa for nulo.
            APIException: Se o usuário já estiver cadastrado.
        """

        if not name or name == '':
            raise APIException("Campo nome não deve ser nulo")
        
        if not email or email == '':
            raise APIException("Campo e-mail não deve ser nulo")
        
        if not password or password == '':
            raise APIException("Campo senha não deve ser nulo")
        
        if type_account == 'employee' and not company_id:
            raise APIException("ID da empresa não deve ser nulo")
        
        user = User.objects.filter(email=email).first()
        
        if user:
            raise APIException("Este usuário já encontra cadastrado")
        
        password_hashed = make_password(password=password)
        
        created_user = User.objects.create(name=name, email=email, password=password_hashed, is_owner=0 if type_account == 'employee' else 1)
        
        print(created_user.id)
        
        if type_account == 'owner':
            created_enterprise = Enterprise.objects.create(name='Nome da empresa', owner_id=created_user.id)
        
        if type_account == 'employee':
            Employee.objects.create(enterprise_id=company_id or created_enterprise.id, user_id=created_user.id)
            
        return created_user