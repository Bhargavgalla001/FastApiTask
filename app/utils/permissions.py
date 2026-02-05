from sqlalchemy.orm import Session
from app.models.role import Role
from app.models.permission import Permission, RoleHasPermission


def seed_roles_permissions(db: Session):
    # ---- ROLES ----
    admin_role = db.query(Role).filter_by(name="admin").first()
    user_role = db.query(Role).filter_by(name="user").first()

    if not admin_role:
        admin_role = Role(name="admin")
        db.add(admin_role)

    if not user_role:
        user_role = Role(name="user")
        db.add(user_role)

    db.commit()
    db.refresh(admin_role)
    db.refresh(user_role)

    # ---- PERMISSIONS ----
    permission_names = [
        "create_user",
        "read_users",
        "delete_user",
        "create_task",
        "update_task",
        "delete_task",
    ]

    permissions = []
    for name in permission_names:
        perm = db.query(Permission).filter_by(name=name).first()
        if not perm:
            perm = Permission(name=name)
            db.add(perm)
        permissions.append(perm)

    db.commit()

    # ---- ROLE ↔ PERMISSIONS ----
    for perm in permissions:
        if not db.query(RoleHasPermission).filter_by(
            role_id=admin_role.id,
            permission_id=perm.id
        ).first():
            db.add(RoleHasPermission(
                role_id=admin_role.id,
                permission_id=perm.id
            ))

        if "task" in perm.name:
            if not db.query(RoleHasPermission).filter_by(
                role_id=user_role.id,
                permission_id=perm.id
            ).first():
                db.add(RoleHasPermission(
                    role_id=user_role.id,
                    permission_id=perm.id
                ))

    db.commit()
