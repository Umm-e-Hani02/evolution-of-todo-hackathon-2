"""Authentication API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from src.core.database import get_db
from src.core.security import hash_password, verify_password, create_access_token, get_token_expiry_hours
from src.models.user import User
from src.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from src.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(user_data: UserCreate, db: Session = Depends(get_db)) -> TokenResponse:
    """Register a new user account."""
    try:
        # Check if email already exists
        existing = db.exec(select(User).where(User.email == user_data.email)).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        # Create new user
        hashed_pw = hash_password(user_data.password)
        new_user = User(email=user_data.email, password_hash=hashed_pw)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Generate JWT token
        token = create_access_token(
            data={"sub": new_user.id, "email": new_user.email}
        )

        return TokenResponse(
            token=token,
            user=UserResponse.model_validate(new_user),
        )
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        # Log the error and raise a 500 error for unexpected issues
        print(f"Error in register endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login user",
)
def login(credentials: UserLogin, db: Session = Depends(get_db)) -> TokenResponse:
    """Authenticate user and return JWT token."""
    try:
        # Find user by email
        user = db.exec(select(User).where(User.email == credentials.email)).first()
        if user is None:
            # Generic error message to prevent email enumeration
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # Verify password
        if not verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # Generate JWT token
        token = create_access_token(
            data={"sub": str(user.id), "email": user.email}
        )

        return TokenResponse(
            token=token,
            user=UserResponse.model_validate(user),
        )
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        # Log the error and raise a 500 error for unexpected issues
        print(f"Error in login endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
)
def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    """Get the currently authenticated user's information."""
    try:
        return UserResponse.model_validate(current_user)
    except Exception as e:
        # Log the error and raise a 500 error for unexpected issues
        print(f"Error in get_me endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error retrieving user information"
        )
