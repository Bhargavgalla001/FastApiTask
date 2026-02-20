from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_db, admin_only, get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.core.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])


# =========================
# Get Current User Profile
# =========================
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user profile"""
    return current_user


# =========================
# Admin: List All Users
# =========================
@router.get("/", response_model=list[UserResponse])
def list_users(
    admin: User = Depends(admin_only),
    db: Session = Depends(get_db)
):
    """Get all users (Admin only)"""
    users = db.query(User).all()
    return users


# =========================
# Admin: Get User by ID
# =========================
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    admin: User = Depends(admin_only),
    db: Session = Depends(get_db)
):
    """Get specific user by ID (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# =========================
# Admin: Update User Role
# =========================
@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    admin: User = Depends(admin_only),
    db: Session = Depends(get_db)
):
    """Update user role or password (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Prevent admin from changing their own role to user
    if admin.id == user_id and data.role == "user":
        raise HTTPException(
            status_code=400,
            detail="Cannot demote yourself from admin role"
        )

    # Update role if provided
    if data.role and data.role in ["user", "admin"]:
        user.role = data.role

    # Update password if provided
    if data.password:
        user.hashed_password = hash_password(data.password)

    db.commit()
    db.refresh(user)
    return user


# =========================
# Admin: Delete User
# =========================
@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    admin: User = Depends(admin_only),
    db: Session = Depends(get_db)
):
    """Delete a user (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Prevent deleting own account
    if admin.id == user_id:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete your own account"
        )

    db.delete(user)
    db.commit()


# =========================
# User: Update Own Password
# =========================
@router.put("/{user_id}/password")
def update_own_password(
    user_id: int,
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update own password (User can only update their own, Admin can update any)"""
    # User can only update their own password, admin can update any
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Can only update your own password")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not data.password:
        raise HTTPException(status_code=400, detail="Password is required")

    user.hashed_password = hash_password(data.password)
    db.commit()
    db.refresh(user)

    return {"message": "Password updated successfully"}
