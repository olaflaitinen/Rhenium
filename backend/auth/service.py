"""
Authentication service for user management and JWT tokens.

Provides:
- Password hashing and verification
- JWT token generation and validation
- User authentication
"""
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from backend.auth.models import User, Role, RoleEnum, TokenData
from backend.config.settings import settings

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_EXPIRE_MINUTES


class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass


class AuthService:
    """Service for authentication operations."""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password for storage."""
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(
        data: dict,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT access token.
        
        Args:
            data: Data to encode in the token
            expires_delta: Token expiration time
            
        Returns:
            Encoded JWT token
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow()
        })
        
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str) -> TokenData:
        """
        Decode and validate a JWT token.
        
        Args:
            token: JWT token string
            
        Returns:
            TokenData with user information
            
        Raises:
            AuthenticationError: If token is invalid
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: int = payload.get("user_id")
            username: str = payload.get("sub")
            roles: list = payload.get("roles", [])
            
            if username is None or user_id is None:
                raise AuthenticationError("Invalid token payload")
            
            return TokenData(
                user_id=user_id,
                username=username,
                roles=roles
            )
        except JWTError as e:
            raise AuthenticationError(f"Could not validate token: {str(e)}")

    @staticmethod
    def authenticate_user(
        db: Session,
        username: str,
        password: str
    ) -> Optional[User]:
        """
        Authenticate a user with username and password.
        
        Args:
            db: Database session
            username: Username or email
            password: Plain text password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        # Try to find user by username or email
        user = db.query(User).filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if not user:
            return None
        
        if not AuthService.verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            return None
        
        return user

    @staticmethod
    def create_user(
        db: Session,
        email: str,
        username: str,
        password: str,
        full_name: Optional[str] = None,
        roles: list[RoleEnum] = None
    ) -> User:
        """
        Create a new user.
        
        Args:
            db: Database session
            email: User email
            username: Username
            password: Plain text password
            full_name: User's full name
            roles: List of roles to assign
            
        Returns:
            Created User object
        """
        if roles is None:
            roles = [RoleEnum.VIEWER]
        
        # Hash password
        hashed_password = AuthService.get_password_hash(password)
        
        # Create user
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            full_name=full_name,
            is_active=True,
            is_superuser=False
        )
        
        # Assign roles
        for role_name in roles:
            role = db.query(Role).filter(Role.name == role_name.value).first()
            if role:
                user.roles.append(role)
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get user by username."""
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email."""
        return db.query(User).filter(User.email == email).first()
